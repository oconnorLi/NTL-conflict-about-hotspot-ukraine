# =============================================
# 区域统计分析脚本
# 1. 统计各州内 iso 影像中值为1的像元个数
# 2. 计算各州 1月/5月 夜光影像总值及变化率
# 3. JAG投稿风格散点图
# =============================================

import os
import numpy as np
from osgeo import gdal, ogr, osr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ─── 路径配置 ──────────────────────────────────────────────
IMAGE_DIR   = r'D:\Desktop_file\徐南老师\discussion_data\Image'
HOTSPOT_DIR = r'D:\Desktop_file\徐南老师\discussion_data\Image\hotspot'
SHP_DIR     = r'D:\LM_Master\2022ESRI\shp数据'

ISO_IMAGE = os.path.join(HOTSPOT_DIR, 'iso_Band_ave_result_Five_Month_image.dat')
IMG_JAN   = os.path.join(IMAGE_DIR,   'sub_SVDNB_npp_20220101-20220131.dat')
IMG_MAY   = os.path.join(IMAGE_DIR,   'sub_SVDNB_npp_20220501-20220531.dat')

# ─── 冲突数据 ──────────────────────────────────────────────
conflict = np.array([8, 8, 7, 372, 2, 32, 1223, 1465, 13, 113,
                     752, 0, 0, 295, 653, 2, 154, 20, 91, 9,
                     27, 212, 15, 281, 607, 13, 2974])

# =============================================
# 工具函数
# =============================================
def rasterize_shape(shp_path, ref_ds):
    gt   = ref_ds.GetGeoTransform()
    cols = ref_ds.RasterXSize
    rows = ref_ds.RasterYSize
    proj = ref_ds.GetProjection()
    mem_drv = gdal.GetDriverByName('MEM')
    mask_ds = mem_drv.Create('', cols, rows, 1, gdal.GDT_Byte)
    mask_ds.SetGeoTransform(gt)
    mask_ds.SetProjection(proj)
    mask_ds.GetRasterBand(1).Fill(0)
    shp_ds     = ogr.Open(shp_path)
    layer      = shp_ds.GetLayer()
    raster_srs = osr.SpatialReference()
    raster_srs.ImportFromWkt(proj)
    vector_srs = layer.GetSpatialRef()
    if vector_srs and not raster_srs.IsSame(vector_srs):
        mem_vec_drv  = ogr.GetDriverByName('Memory')
        mem_vec_ds   = mem_vec_drv.CreateDataSource('')
        reproj_layer = mem_vec_ds.CreateLayer('reproj', srs=raster_srs)
        transform    = osr.CoordinateTransformation(vector_srs, raster_srs)
        for feat in layer:
            geom = feat.GetGeometryRef().Clone()
            geom.Transform(transform)
            new_feat = ogr.Feature(reproj_layer.GetLayerDefn())
            new_feat.SetGeometry(geom)
            reproj_layer.CreateFeature(new_feat)
        gdal.RasterizeLayer(mask_ds, [1], reproj_layer, burn_values=[1])
    else:
        gdal.RasterizeLayer(mask_ds, [1], layer, burn_values=[1])
    mask   = mask_ds.GetRasterBand(1).ReadAsArray().astype(bool)
    shp_ds = None
    return mask

def read_band(filepath, band=1):
    ds = gdal.Open(filepath, gdal.GA_ReadOnly)
    if ds is None:
        raise FileNotFoundError(f'无法打开影像: {filepath}')
    band_obj = ds.GetRasterBand(band)
    nodata   = band_obj.GetNoDataValue()
    data     = band_obj.ReadAsArray().astype(np.float64)
    if nodata is not None:
        data[data == nodata] = np.nan
    return data, ds, nodata

def get_state_name(shp_path):
    return os.path.splitext(os.path.basename(shp_path))[0]

# =============================================
# 1. 收集 shp 文件
# =============================================
shp_files = []
for root, dirs, files in os.walk(SHP_DIR):
    for f in files:
        if f.endswith('.shp'):
            shp_files.append(os.path.join(root, f))
shp_files.sort()
print(f'找到 {len(shp_files)} 个 shp 文件')

# =============================================
# 2. 读取影像
# =============================================
print('\n正在读取影像...')
iso_data, iso_ds, _ = read_band(ISO_IMAGE)
jan_data, jan_ds, _ = read_band(IMG_JAN)
may_data, may_ds, _ = read_band(IMG_MAY)

# =============================================
# 3. 逐州统计
# =============================================
results = []
#print(f'\n{"州名":<40} {"ISO值=1像元数":>14} {"1月总值":>16} '
     # f'{"5月总值":>16} {"变化率(%)":>12}')
#print('-' * 105)

for shp_path in shp_files:
    state_name = get_state_name(shp_path)
    try:
        mask_iso  = rasterize_shape(shp_path, iso_ds)
        iso_valid = iso_data[mask_iso]
        iso_valid = iso_valid[~np.isnan(iso_valid)]
        count_one = int(np.sum(iso_valid == 1))

        mask_jan  = rasterize_shape(shp_path, jan_ds)
        mask_may  = rasterize_shape(shp_path, may_ds)
        jan_valid = jan_data[mask_jan]
        jan_valid = jan_valid[~np.isnan(jan_valid)]
        may_valid = may_data[mask_may]
        may_valid = may_valid[~np.isnan(may_valid)]
        jan_sum   = float(np.nansum(jan_valid))
        may_sum   = float(np.nansum(may_valid))
        change_pct = ((may_sum - jan_sum) / abs(jan_sum) * 100.0
                      if jan_sum != 0 else float('nan'))

        results.append({'state': state_name, 'iso_count1': count_one,
                        'jan_sum': jan_sum, 'may_sum': may_sum,
                        'change_pct': change_pct})
        change_str = f'{change_pct:+.2f}%' if not np.isnan(change_pct) else 'N/A'
        #print(f'{state_name:<40} {count_one:>14,} {jan_sum:>16.2f} '
             # f'{may_sum:>16.2f} {change_str:>12}')

    except Exception as e:
        print(f'{state_name:<40} 处理失败: {e}')
        results.append({'state': state_name, 'iso_count1': None,
                        'jan_sum': None, 'may_sum': None, 'change_pct': None})

# =============================================
# 4. 保存统计 CSV
# =============================================
output_csv = os.path.join(IMAGE_DIR, 'state_statistics_result.csv')
with open(output_csv, 'w', encoding='utf-8-sig') as f:
    f.write('州名,ISO值=1像元数,1月夜光总值,5月夜光总值,5月相对1月变化率(%)\n')
    for r in results:
        change = (f"{r['change_pct']:+.4f}"
                  if r['change_pct'] is not None
                  and not np.isnan(r['change_pct']) else 'N/A')
        f.write(f"{r['state']},{r['iso_count1']},"
                f"{r['jan_sum']:.4f},{r['may_sum']:.4f},{change}\n")
print(f'\n✅ 统计结果已保存: {output_csv}')

iso_ds = jan_ds = may_ds = None

valid_results = [r for r in results
                 if r['change_pct'] is not None
                 and not np.isnan(r['change_pct'])]
if valid_results:
    changes = [r['change_pct'] for r in valid_results]
    print(f'成功处理州数: {len(valid_results)} / {len(shp_files)}')
    print(f'平均变化率:   {np.mean(changes):+.2f}%')

# =============================================
# 5. JAG 风格散点图
# =============================================

# ── 提取绘图数据 ──────────────────────────────────────────
iso_count   = np.array([r['iso_count1'] if r['iso_count1'] is not None
                        else np.nan for r in results], dtype=float)
change_rate = np.array([r['change_pct'] if r['change_pct'] is not None
                        else np.nan for r in results], dtype=float)
x_conflict  = conflict.astype(float)

# ── 全局字体 Arial ────────────────────────────────────────
plt.rcParams.update({
    'font.family':       'Arial',
    'font.size':         12,
    'axes.linewidth':    0.8,
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
    'xtick.major.size':  4,
    'ytick.major.size':  4,
    'xtick.minor.size':  0,   # 无子刻度
    'ytick.minor.size':  0,
    'axes.grid':         False,
})

# ── 色谱 ──────────────────────────────────────────────────
""" cmap_ref = LinearSegmentedColormap.from_list(
    'ref_style',
    ['#3B4CC0', '#5B8FD4', '#7EC8C8', '#A8D96C',
     '#F0E442', '#F5A623', '#D94F2B', '#8B1A1A'],
    N=256
) """
cmap_ref = LinearSegmentedColormap.from_list(
    'legend_style',
    ['#a8d5a2',   # 浅绿（Chernihiv）
     '#b2dfc8',   # 薄荷绿
     '#a8d4e8',   # 浅青蓝（Ocean/Lake 系）
     '#7ab8d4',   # 中蓝
     '#e8a8a8',   # 浅粉（Kyiv 系）
     '#d46060',   # 中红粉
     '#c0392b'],  # 深红（Hotspot）
    N=256
)
# conflict 着色，LogNorm（冲突=0的点单独处理）
cf_pos  = x_conflict[x_conflict > 0]
vmin_cf = float(np.percentile(cf_pos, 2))
vmax_cf = float(np.percentile(cf_pos, 98))
norm_cf = mcolors.LogNorm(vmin=max(vmin_cf, 1), vmax=vmax_cf)

# ── 拟合函数 ──────────────────────────────────────────────
def fit_loglinear(x, y):
    mask = np.isfinite(x) & np.isfinite(y) & (x > 0)
    xm, ym = x[mask], y[mask]
    lx = np.log10(xm)
    slope, intercept, r, p, _ = stats.linregress(lx, ym)
    x_line = np.linspace(xm.min(), xm.max(), 500)
    y_line = slope * np.log10(x_line) + intercept
    rmse   = np.sqrt(np.mean((slope * lx + intercept - ym) ** 2))
    return x_line, y_line, r**2, rmse, int(mask.sum()), slope, intercept

# ── 统计标注自动避开散点 ──────────────────────────────────
def get_stats_pos(xv, yv, ax):
    disp = ax.transData.transform(np.column_stack([xv, yv]))
    pts  = ax.transAxes.inverted().transform(disp)
    candidates = [
        (0.03, 0.97, 'left',  'top'),
        (0.97, 0.97, 'right', 'top'),
        (0.03, 0.03, 'left',  'bottom'),
        (0.97, 0.03, 'right', 'bottom'),
    ]
    best, best_score = candidates[0], np.inf
    for cand in candidates:
        cx, cy = cand[0], cand[1]
        n = np.sum((np.abs(pts[:, 0] - cx) < 0.30) &
                   (np.abs(pts[:, 1] - cy) < 0.30))
        if n < best_score:
            best_score, best = n, cand
    return best

# ── 单子图绘制函数 ────────────────────────────────────────
def draw_panel(ax, x, y, label_letter, xlabel, ylabel):
    # conflict=0 的点用最低色值单独绘制
    mask_pos  = np.isfinite(x) & np.isfinite(y) & (x > 0)
    mask_zero = np.isfinite(x) & np.isfinite(y) & (x == 0)

    if mask_zero.any():
        ax.scatter(x[mask_zero], y[mask_zero],
                   c=[cmap_ref(0.0)] * mask_zero.sum(),
                   s=42, alpha=0.92, edgecolors='none', zorder=3)

    xv, yv = x[mask_pos], y[mask_pos]
    cv     = xv
    order  = np.argsort(cv)

    sc = ax.scatter(xv[order], yv[order],
                    c=cv[order], cmap=cmap_ref, norm=norm_cf,
                    s=42, alpha=0.92, edgecolors='none', zorder=3)

    # 拟合线
    x_line, y_line, r2, rmse, n, slope, intercept = fit_loglinear(xv, yv)
    ax.plot(x_line, y_line, color='black', lw=1.8, zorder=4)

    # 统计标注
    tx, ty, ha, va = get_stats_pos(xv, yv, ax)
    sign   = '+' if intercept >= 0 else '-'
    eq_str = f'$y$ = {slope:.2f}$x$ {sign} {abs(intercept):.2f}'
    txt    = (f'$N$ = {n}\n'
              f'$R$$^2$ = {r2:.2f}\n'
              f'$RMSE$ = {rmse:.2f}\n'
              f'{eq_str}')
    ax.text(tx, ty, txt,
            transform=ax.transAxes,
            va=va, ha=ha,
            fontsize=12, fontstyle='italic', fontfamily='Arial',
            linespacing=1.65,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='none', alpha=0.80),
            zorder=6)

    # 子图标签（与统计框反侧）
    lx  = 0.06 if ha == 'right' else 0.94
    lha = 'left' if lx == 0.06 else 'right'
    ax.text(lx, 0.94, label_letter,
            transform=ax.transAxes,
            va='top', ha=lha,
            fontsize=16, fontfamily='Arial', zorder=6)

    # 轴设置
    ax.set_xscale('log')
    ax.set_xlabel(xlabel, fontsize=12, fontfamily='Arial', labelpad=4)
    ax.set_ylabel(ylabel, fontsize=12, fontfamily='Arial', labelpad=4)

    # 四轴全部保留，但只有左轴和下轴显示主刻度，朝内，无子刻度
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.8)

    # 下轴：主刻度朝内，无子刻度，无上轴刻度
    ax.tick_params(axis='x', which='major',
                   bottom=True, top=False,
                   direction='in', length=4,
                   width=0.8, labelsize=12)
    ax.tick_params(axis='x', which='minor',
                   bottom=False, top=False)

    # 左轴：主刻度朝内，无子刻度，无右轴刻度
    ax.tick_params(axis='y', which='major',
                   left=True, right=False,
                   direction='in', length=4,
                   width=0.8, labelsize=12)
    ax.tick_params(axis='y', which='minor',
                   left=False, right=False)

    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontfamily('Arial')

    ax.set_box_aspect(1)
    return sc

# ── 画布布局 ──────────────────────────────────────────────
# 两个等大正方形子图 + 底部居中横向 colorbar
PANEL   = 3.8    # 子图边长（英寸）
HGAP    = 0.85   # 两图间距
L_MAR   = 0.65
R_MAR   = 0.25
T_MAR   = 0.25
B_MAR   = 0.94   # 底部留给 colorbar

FIG_W = L_MAR + PANEL * 2 + HGAP + R_MAR
FIG_H = B_MAR + PANEL + T_MAR

fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor='white')

# 两个子图坐标（归一化）
left1  = L_MAR / FIG_W
left2  = (L_MAR + PANEL + HGAP) / FIG_W
bottom = B_MAR / FIG_H
pw     = PANEL / FIG_W
ph     = PANEL / FIG_H

ax1 = fig.add_axes([left1, bottom, pw, ph])
ax2 = fig.add_axes([left2, bottom, pw, ph])

# ── 绘图 ──────────────────────────────────────────────────
sc1 = draw_panel(ax1, x_conflict, iso_count,
                 '(a)', 'Conflict Events', 'ISO Hotspot Pixel Count')
sc2 = draw_panel(ax2, x_conflict, change_rate,
                 '(b)', 'Conflict Events', 'NTL Change Rate (May vs Jan, %)')

# ── 底部居中横向 colorbar ─────────────────────────────────
# 宽度 = 两图总宽的一半，水平居中于两图整体
total_width = PANEL * 2 + HGAP          # 两图总宽（英寸）
cb_width    = (total_width * 0.5) / FIG_W   # 一半宽度，归一化
cb_height   = ph * 0.05                      # 子图高的 5%

# 居中：起始 x = 左图左边 + 总宽的 1/4
cb_left   = left1 + (total_width * 0.25) / FIG_W
cb_bottom = (B_MAR * 0.30) / FIG_H

cax = fig.add_axes([cb_left, cb_bottom, cb_width, cb_height])

cb = fig.colorbar(
    plt.cm.ScalarMappable(norm=norm_cf, cmap=cmap_ref),
    cax=cax,
    orientation='horizontal'
)

# 字体为原来的 1.5 倍：9 × 1.5 = 13.5，标签 8 × 1.5 = 12
#cb.set_label('Conflict Events', fontsize=12,
            # fontfamily='Arial', labelpad=5)

cb.ax.tick_params(
    axis='x', which='major',
    top=False, bottom=True,
    direction='in', length=4,
    width=0.8, labelsize=12
)
cb.ax.tick_params(axis='x', which='minor', bottom=False)
cb.outline.set_linewidth(0.7)

for lbl in cb.ax.get_xticklabels():
    lbl.set_fontfamily('Arial')
    lbl.set_fontsize(12)

# ── 保存 ──────────────────────────────────────────────────
out_fig = os.path.join(IMAGE_DIR, 'conflict_scatter_JAG.png')
plt.savefig(out_fig, dpi=600, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.show()
print(f'✅ JAG风格散点图已保存: {out_fig}')