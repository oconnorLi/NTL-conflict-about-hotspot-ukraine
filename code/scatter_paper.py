""" import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 读取数据
file_path = r'D:\Desktop_file\徐南老师\add_data\six_index_T.csv'
df = pd.read_csv(file_path)

# 确保列名正确（去掉可能的空格）
df.columns = df.columns.str.strip()

# 提取需要的7列数据
target_cols = ['Sum_Area', 'BTSM', 'road', 'water', 'pop_SUM', 'ndvi_MEAN', 'slope_MEAN']
data = df[target_cols].copy()

# 数据归一化
def normalize(x):
    return (x - x.min()) / (x.max() - x.min())

data_norm = data.apply(normalize)

# 创建图形
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Sum_Area vs Other Variables (Normalized)', fontsize=16, y=1.02)

y_vars = ['BTSM', 'road', 'water', 'pop_SUM', 'ndvi_MEAN', 'slope_MEAN']
titles = ['BTSM', 'Road', 'Water', 'Population', 'NDVI', 'Slope']

# 绘制散点图
for i, (ax, y_var, title) in enumerate(zip(axes.flat, y_vars, titles)):
    x = data_norm['Sum_Area']
    y = data_norm[y_var]
    
    # 散点
    ax.scatter(x, y, alpha=0.6, s=50, edgecolor='k', linewidth=0.5)
    
    # 趋势线
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x), 'r--', linewidth=2, alpha=0.8)
    
    # 计算相关系数
    corr = np.corrcoef(x, y)[0, 1]
    
    # 标签和标题
    ax.set_xlabel('Normalized Sum_Area', fontsize=11)
    ax.set_ylabel(f'Normalized {title}', fontsize=11)
    ax.set_title(f'{title} (r = {corr:.3f})', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 保存图片
output_path = r'D:\Desktop_file\徐南老师\add_data\scatter_plots.png'
#fig.savefig(output_path, dpi=300, bbox_inches='tight')
#print(f'图形已保存至: {output_path}')

# 显示基本信息
print(f'数据样本数: {len(data)}')
print('\n原始数据范围:')
for col in data.columns:
    print(f'{col}: [{data[col].min():.6f}, {data[col].max():.6f}]') 
 """
""" import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 设置字体和样式
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.labelsize'] = 7
plt.rcParams['axes.titlesize'] = 8
plt.rcParams['xtick.labelsize'] = 6
plt.rcParams['ytick.labelsize'] = 6

# 读取数据
df = pd.read_csv(r'D:\Desktop_file\徐南老师\add_data\six_index_T.csv')
df.columns = df.columns.str.strip()

# 提取数据
target_cols = ['Sum_Area', 'BTSM', 'road', 'water', 'pop_SUM', 'ndvi_MEAN', 'slope_MEAN']
data = df[target_cols].copy()

# 归一化Sum_Area
data_norm = data.copy()
data_norm['Sum_Area'] = (data['Sum_Area'] - data['Sum_Area'].min()) / (data['Sum_Area'].max() - data['Sum_Area'].min())

# 图变量设置
y_vars = ['BTSM', 'road', 'water', 'pop_SUM', 'ndvi_MEAN', 'slope_MEAN']
titles = ['ISA', 'RD', 'WA', 'Pop', 'NDVI', 'Slope']

# 创建子图（使用 constrained_layout 自动优化布局）
fig, axes = plt.subplots(2, 3, figsize=(24, 15), dpi=300, constrained_layout=True)

for i, (ax, y_var, title) in enumerate(zip(axes.flat, y_vars, titles)):
    x = data_norm['Sum_Area']
    y = data[y_var]

    # 绘制散点图
    ax.scatter(x, y, alpha=0.6, s=30, c='steelblue', edgecolors='k', linewidth=0.3, label='Data')

    # 拟合趋势线
    z = np.polyfit(x, y, 1)
    ax.plot(x, np.poly1d(z)(x), 'r-', linewidth=1.8, label='Trend')

    # 计算相关系数
    corr, p_value = stats.pearsonr(x, y)

    # 显著性标记
    if p_value < 0.001:
        sig_mark, p_text = "***", "p < 0.001"
    elif p_value < 0.01:
        sig_mark, p_text = "**", "p < 0.01"
    elif p_value < 0.05:
        sig_mark, p_text = "*", f"p = {p_value:.3f}"
    else:
        sig_mark, p_text = "", f"p = {p_value:.3f}"

    # 添加统计文本框
    ax.text(0.98, 0.98,
            f"r = {corr:.3f}{sig_mark}\n{p_text}",
            transform=ax.transAxes,
            fontsize=9,
            ha='right', va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.7, edgecolor='gray'))

    # 设置标签和标题
    ax.set_xlabel('Hotspot area')
    ax.set_ylabel(title)
    ax.set_title(title, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.3)

# 添加统一图例（右上角，使用 bbox_to_anchor 放置在图外）
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels,
           loc='upper right',
           bbox_to_anchor=(0.98, 0.98),
           fontsize=11, frameon=True)

# 最终显示
plt.show()

# 输出统计结果
print("相关系数分析结果:")
print("-" * 40)
for y_var, title in zip(y_vars, titles):
    x = data_norm['Sum_Area']
    y = data[y_var]
    corr, p_value = stats.pearsonr(x, y)
    
    if p_value < 0.001:
        sig = "***"
    elif p_value < 0.01:
        sig = "**"
    elif p_value < 0.05:
        sig = "*"
    else:
        sig = ""
    
    print(f"{title:10} r = {corr:6.3f}{sig:3} (p = {p_value:.4f})")

print(f"\n样本数: {len(data)}") """

""" import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.ticker import ScalarFormatter

# ================== 全局样式 ==================
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.labelsize'] = 7
plt.rcParams['axes.titlesize'] = 8
plt.rcParams['xtick.labelsize'] = 6
plt.rcParams['ytick.labelsize'] = 6

# ================== 读取数据 ==================
df = pd.read_csv(r'D:\Desktop_file\徐南老师\add_data\six_index_T.csv')
df.columns = df.columns.str.strip()

target_cols = ['Sum_Area', 'BTSM', 'road', 'water', 'pop_SUM', 'ndvi_MEAN', 'slope_MEAN']
data = df[target_cols].copy()

# 归一化 Sum_Area
data_norm = data.copy()
data_norm['Sum_Area'] = (
    (data['Sum_Area'] - data['Sum_Area'].min()) /
    (data['Sum_Area'].max() - data['Sum_Area'].min())
)

# ================== 作图变量 ==================
y_vars = ['BTSM', 'road', 'water', 'pop_SUM', 'ndvi_MEAN', 'slope_MEAN']
titles = ['ISA', 'RD', 'WA', 'Pop', 'NDVI', 'Slope']

fig, axes = plt.subplots(2, 3, figsize=(24, 15), dpi=300, constrained_layout=True)

for ax, y_var, title in zip(axes.flat, y_vars, titles):
    x = data_norm['Sum_Area']
    y = data[y_var]

    # -------- 散点 --------
    ax.scatter(
        x, y,
        alpha=0.6, s=30,
        c='steelblue',
        edgecolors='k',
        linewidth=0.3,
        label='Data'
    )

    # -------- 拟合 --------
    a, b = np.polyfit(x, y, 1)
    ax.plot(x, a * x + b, 'r-', lw=1.8, label='Trend')

    # -------- 相关系数 --------
    r, p = stats.pearsonr(x, y)

    if p < 0.001:
        sig, p_txt = "***", "p < 0.001"
    elif p < 0.01:
        sig, p_txt = "**", "p < 0.01"
    elif p < 0.05:
        sig, p_txt = "*", f"p = {p:.3f}"
    else:
        sig, p_txt = "", f"p = {p:.3f}"

    # -------- 统计框（含函数公式） --------
    ax.text(
        0.97, 0.97,
        f"y = {a:.3f}x + {b:.3f}\n"
        f"r = {r:.3f}{sig}\n{p_txt}",
        transform=ax.transAxes,
        fontsize=8,
        ha='right', va='top',
        bbox=dict(
            boxstyle='round,pad=0.25',
            facecolor='wheat',
            edgecolor='gray',
            alpha=0.7
        )
    )

    # -------- 坐标轴设置 --------
    ax.set_xlabel('Hotspot area')
    ax.set_ylabel(title)
    ax.set_title(title, fontweight='bold')

    # 缩短轴突（刻度长度 & 与轴线距离）
    ax.tick_params(axis='both', which='major', length=3, pad=2)

    # Pop 使用科学计数法
    if title == 'Pop':
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

# ================== 缩小后的统一图例 ==================
handles, labels = axes.flat[0].get_legend_handles_labels()
fig.legend(
    handles, labels,
    loc='upper right',
    bbox_to_anchor=(0.98, 0.98),
    fontsize=7,           # 原来 11 → 缩小
    markerscale=0.7,      # 点大小缩小
    frameon=True
)

plt.show()

# ================== 输出统计结果 ==================
print("相关系数分析结果:")
print("-" * 40)
for y_var, title in zip(y_vars, titles):
    x = data_norm['Sum_Area']
    y = data[y_var]
    r, p = stats.pearsonr(x, y)

    sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
    print(f"{title:10} r = {r:6.3f}{sig:3} (p = {p:.4f})")

print(f"\n样本数: {len(data)}") """
""" import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.ticker import ScalarFormatter

# ================== 全局样式 ==================
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.labelsize'] = 7
plt.rcParams['axes.titlesize'] = 8
plt.rcParams['xtick.labelsize'] = 6
plt.rcParams['ytick.labelsize'] = 6

# ================== 读取数据 ==================
df = pd.read_csv(r'D:\Desktop_file\徐南老师\add_data\six_index_T.csv')
df.columns = df.columns.str.strip()

target_cols = [
    'Sum_Area', 'BTSM', 'road', 'water',
    'pop_SUM', 'ndvi_MEAN', 'slope_MEAN'
]
data = df[target_cols].copy()

# ================== 归一化 Hotspot Area ==================
data_norm = data.copy()
data_norm['Sum_Area'] = (
    (data['Sum_Area'] - data['Sum_Area'].min()) /
    (data['Sum_Area'].max() - data['Sum_Area'].min())
)

# ================== 作图变量 ==================
y_vars = ['BTSM', 'road', 'water', 'pop_SUM', 'ndvi_MEAN', 'slope_MEAN']
titles = ['ISA', 'RD', 'WA', 'Pop', 'NDVI', 'Slope']

fig, axes = plt.subplots(
    2, 3,
    figsize=(24, 15),
    dpi=300,
    constrained_layout=True
)

# ================== 绘图循环 ==================
for ax, y_var, title in zip(axes.flat, y_vars, titles):

    x = data_norm['Sum_Area']
    y = data[y_var]

    # ---- 散点 ----
    ax.scatter(
        x, y,
        s=30,
        alpha=0.6,
        c='steelblue',
        edgecolors='k',
        linewidth=0.3,
        label='Data'
    )

    # ---- 拟合线 ----
    a, b = np.polyfit(x, y, 1)
    x_sorted = np.sort(x)
    ax.plot(
        x_sorted,
        a * x_sorted + b,
        'r-',
        lw=1.8,
        label='Trend'
    )

    # ---- 相关系数 ----
    r, p = stats.pearsonr(x, y)
    if p < 0.001:
        sig, p_txt = "***", "p < 0.001"
    elif p < 0.01:
        sig, p_txt = "**", "p < 0.01"
    elif p < 0.05:
        sig, p_txt = "*", f"p = {p:.3f}"
    else:
        sig, p_txt = "", f"p = {p:.3f}"

    # ---- 统计文本（含回归公式） ----
    ax.text(
        0.97, 0.97,
        f"y = {a:.3f}x + {b:.3f}\n"
        f"r = {r:.3f}{sig}\n{p_txt}",
        transform=ax.transAxes,
        fontsize=8,
        ha='right',
        va='top',
        bbox=dict(
            boxstyle='round,pad=0.25',
            facecolor='wheat',
            edgecolor='gray',
            alpha=0.7
        )
    )

    # ---- 坐标轴 ----
    ax.set_xlabel('Hotspot area')
    ax.set_ylabel(title)
    ax.set_title(title, fontweight='bold')

    # 短轴突 & 紧凑刻度
    ax.tick_params(
        axis='both',
        which='major',
        length=2,
        pad=1
    )

    # ================== Pop 科学计数法（Nature 风格） ==================
    if title == 'Pop':
        formatter = ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((0, 0))
        ax.yaxis.set_major_formatter(formatter)

        # 把 ×10ⁿ 移到右上角
        ax.yaxis.get_offset_text().set_fontsize(7)
        ax.yaxis.get_offset_text().set_x(0.02)
        ax.yaxis.get_offset_text().set_y(0.02)

# ================== 缩小后的统一图例 ==================
handles, labels = axes.flat[0].get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    loc='upper right',
    bbox_to_anchor=(0.98, 0.98),
    fontsize=7,
    markerscale=0.7,
    frameon=True
)

plt.show()

# ================== 输出统计结果 ==================
print("相关系数分析结果:")
print("-" * 40)
for y_var, title in zip(y_vars, titles):
    x = data_norm['Sum_Area']
    y = data[y_var]
    r, p = stats.pearsonr(x, y)
    sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
    print(f"{title:10} r = {r:6.3f}{sig:3} (p = {p:.4f})")

print(f"\n样本数: {len(data)}")
 """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.ticker import ScalarFormatter
import string
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt

# ================== 全局样式 ==================
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.labelsize'] = 7
plt.rcParams['axes.titlesize'] = 8
plt.rcParams['xtick.labelsize'] = 6
plt.rcParams['ytick.labelsize'] = 6

# ================== 读取数据 ==================
df = pd.read_csv(r'D:\Desktop_file\徐南老师\add_data\six_index_T.csv')
df.columns = df.columns.str.strip()

target_cols = [
    'Sum_Area', 'BTSM', 'road', 'water',
    'pop_SUM', 'ndvi_MEAN', 'slope_MEAN'
]
data = df[target_cols].copy()

# ================== 归一化 Hotspot Area ==================
data_norm = data.copy()
data_norm['Sum_Area'] = (
    (data['Sum_Area'] - data['Sum_Area'].min()) /
    (data['Sum_Area'].max() - data['Sum_Area'].min())
)

# ================== 作图变量 ==================
y_vars = ['BTSM', 'road', 'water', 'pop_SUM', 'ndvi_MEAN', 'slope_MEAN']
titles = ['ISA', 'RD', 'WA', 'Pop', 'NDVI', 'Slope']
panel_labels = list(string.ascii_lowercase)  # a–f

fig, axes = plt.subplots(
    2, 3,
    figsize=(24, 20),
    dpi=300,
    constrained_layout=True
)

# ================== 绘图循环 ==================
for i, (ax, y_var, title) in enumerate(zip(axes.flat, y_vars, titles)):

    x = data_norm['Sum_Area']
    y = data[y_var]

    # ---- 散点 ----
    ax.scatter(
        x, y,
        s=30,
        alpha=0.6,
        c='steelblue',
        edgecolors='k',
        linewidth=0.3,
        #label='Data'
    )

    # ---- 回归拟合 ----
    a, b = np.polyfit(x, y, 1)
    x_sorted = np.sort(x)
    ax.plot(
        x_sorted,
        a * x_sorted + b,
        'r-',
        lw=1.8,
        #label='Trend'
    )

    # ---- Pearson 相关 ----
    r, p = stats.pearsonr(x, y)
    if p < 0.001:
        sig, p_txt = "***", "p < 0.001"
    elif p < 0.01:
        sig, p_txt = "**", "p < 0.01"
    elif p < 0.05:
        sig, p_txt = "*", f"p = {p:.3f}"
    else:
        sig, p_txt = "", f"p = {p:.3f}"

    # ---- 统计文本（2 位有效数字） ----
    ax.text(
        0.97, 0.97,
        f"y = {a:.2g}x + {b:.2g}\n"
        f"r = {r:.2f}{sig}\n{p_txt}",
        transform=ax.transAxes,
        fontsize=8,
        ha='right',
        va='top',
        #bbox=dict(
        #    boxstyle='round,pad=0.25',
        #   facecolor='wheat',
        #   edgecolor='gray',
        #   alpha=0.7
        )
    

    # ---- 子图编号 Fig. 10a–f ----
    ax.text(
        0.02, 1.15,
        f"({panel_labels[i]})",
        transform=ax.transAxes,
        fontsize=9,
        fontweight='bold',
        va='top',
        ha='left'
    )

    # ---- 坐标轴 ----
    ax.set_xlabel('Hotspot area')
    ax.set_ylabel(title)
    ax.set_title(title, fontweight='bold')

    ax.tick_params(axis='both', which='major', length=3, pad=2)

    # ---- Pop 科学计数法（RSE / Nature 风格） ----
    if title == 'Pop':
        formatter = ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((0, 0))
        ax.yaxis.set_major_formatter(formatter)

        ax.yaxis.get_offset_text().set_fontsize(7)
        ax.yaxis.get_offset_text().set_x(0.90)
        ax.yaxis.get_offset_text().set_y(1.02)

# ================== 统一图例（缩小） ==================
""" handles, labels = axes.flat[0].get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    loc='upper right',
    bbox_to_anchor=(0.98, 0.98),
    fontsize=7,
    markerscale=0.7,
    frameon=True
) """

# ================== RSE 推荐导出 ==================
""" plt.savefig(
    r'D:\Desktop_file\徐南老师\PPT\Fig10_HotspotDrivers.jpg',
    dpi=300,
    format='jpg',
    bbox_inches='tight'
) """
# ================== 读取数据 ==================
""" df = pd.read_csv(r'D:\Desktop_file\徐南老师\add_data\six_index_T.csv')
df.columns = df.columns.str.strip()

target_cols = [
    'Sum_Area', 'BTSM', 'road', 'water',
    'pop_SUM', 'ndvi_MEAN', 'slope_MEAN'
]
data = df[target_cols].copy()

# 仅 Hotspot
hotspot_data = data[data['Sum_Area'] > 0].copy()

# ================== 作图变量 ==================
y_vars = ['BTSM', 'road', 'water', 'pop_SUM', 'ndvi_MEAN', 'slope_MEAN']
titles = ['ISA', 'RD', 'WA', 'Pop', 'NDVI', 'Slope']

# ================== 画布：1 × 6 ==================
fig, axes = plt.subplots(
    1, 6,
    figsize=(30, 6),
    dpi=300,
    constrained_layout=True
)
fig.text(0.01, 0.99, '(g)', fontsize=9, fontweight='bold',
         ha='left', va='top', transform=fig.transFigure)
# ================== 绘图 ==================
for i, (ax, y_var, title) in enumerate(zip(axes, y_vars, titles)):

    values = hotspot_data[y_var].dropna().values

    # ---- 小提琴主体 ----
    violin = ax.violinplot(
        values,
        showmeans=False,
        showmedians=False,
        showextrema=False
    )

    for body in violin['bodies']:
        body.set_facecolor('lightcoral')
        body.set_edgecolor('black')
        body.set_alpha(0.8)
        body.set_linewidth(0.5)

    # ---- 统计量 ----
    q1, q2, q3, q975 = np.percentile(values, [25, 50, 75, 97.5])

    x_center = 1
    w = 0.18

    # Q1 / Q3
    ax.hlines([q1, q3],
              x_center - w, x_center + w,
              colors='black', linewidth=0.6)

    # Median
    ax.hlines(q2,
              x_center - w * 1.2, x_center + w * 1.2,
              colors='black', linewidth=1.0)

    # 97.5% 分位线
    ax.hlines(q975,
              x_center - w * 0.8, x_center + w * 0.8,
              colors='red', linestyles='--', linewidth=0.6)
    
    # ---- 标注97.5%的值 ----
    # 格式化数值显示
    if title == 'Pop':
        # 人口数据使用科学计数法
        label_text = f'{q975:.2e}'
    elif title == 'ISA' or title == 'RD':
        # ISA和RD数据保留1位小数
        label_text = f'{q975:.1f}'
    else:
        # 其他数据保留2位小数
        label_text = f'{q975:.2f}'
    
    # 添加标注
    ax.text(x_center+w*0.5, q975*1.1, label_text,
            fontsize=6, color='red', ha='left', va='bottom',)
          #  bbox=dict(boxstyle='round,pad=0.2', facecolor='white'))

    # ---- 坐标轴 ----
    ax.set_xticks([1])
    ax.set_xticklabels([title])
    # 移除y轴标签
    ax.set_ylabel('')
    ax.set_title(title, fontweight='bold')

    ax.tick_params(axis='both', which='major', length=3, pad=2)

    # ---- Pop 科学计数法 ----
    if title == 'Pop':
        formatter = ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((0, 0))
        ax.yaxis.set_major_formatter(formatter)

        ax.yaxis.get_offset_text().set_fontsize(7)
        ax.yaxis.get_offset_text().set_x(0.95)
        ax.yaxis.get_offset_text().set_y(1.02)

plt.savefig(
    r'D:\Desktop_file\徐南老师\PPT\FigXX_Hotspot_Violin.jpg',
    dpi=300,
    bbox_inches='tight',
    pad_inches=0.1
)

plt.show() """

# 数据读取
df = pd.read_csv(r'D:\Desktop_file\徐南老师\add_data\six_index_T.csv')
df.columns = df.columns.str.strip()

# 选择目标列
target_cols = ['Sum_Area', 'BTSM', 'road', 'water', 'pop_SUM', 'ndvi_MEAN', 'slope_MEAN']
data = df[target_cols].copy()

# Hotspot 区域
hotspot_data = data[data['Sum_Area'] > 0].copy()

# 图变量
y_vars = ['BTSM', 'road', 'water', 'pop_SUM', 'ndvi_MEAN', 'slope_MEAN']
titles = ['ISA', 'RD', 'WA', 'POP', 'NDVI', 'Slope']

# 画布设置
fig, axes = plt.subplots(1, 6, figsize=(30, 6), dpi=300, constrained_layout=True)
fig.text(0.01, 0.99, '(g)', fontsize=9, fontweight='bold',
         ha='left', va='top', transform=fig.transFigure)
# 主标题（可选）
#fig.suptitle('Variable Distributions in Hotspot Areas', fontsize=16, fontweight='bold', y=1.02)

# 绘图
for ax, y_var, title in zip(axes, y_vars, titles):
    values = hotspot_data[y_var].dropna().values
    x_center = 1

    # 小提琴图（无边框）
    violin = ax.violinplot(
        values,
        positions=[x_center],
        showmeans=False,
        showmedians=False,
        showextrema=False,
        widths=0.7
    )

    for body in violin['bodies']:
        body.set_facecolor('steelblue')  # 柔和红色
        body.set_alpha(0.7)
        body.set_linewidth(0)          # 去边框

    # 箱线图嵌入（使用 matplotlib boxplot）
        # 箱线图嵌入（不显示异常值，只显示箱图）
    box = ax.boxplot(
        values,
        positions=[x_center],
        widths=0.2,
        patch_artist=True,
        showfliers=False,   # ⭐ 关键：不画异常值
        boxprops=dict(facecolor='white', color='black', linewidth=0.5),
        medianprops=dict(color='black', linewidth=1.2),
        whiskerprops=dict(color='black', linewidth=0.5),
        capprops=dict(color='black', linewidth=0.5)
    )
    

    # 97.5% 标注（可选保留）
    q975 = np.percentile(values, 97.5)
    ax.hlines(q975,x_center+0.20, x_center * 0.8, colors='red', linestyles='--', linewidth=0.6)
    if title == 'Pop':
        label_text = f'{q975:.2e}'
    elif title in ['ISA', 'RD']:
        label_text = f'{q975:.1f}'
    else:
        label_text = f'{q975:.2f}'

    ax.text(x_center + 0.1, q975 * 1.1, label_text,
            fontsize=8, color='red', ha='left', va='bottom',
            fontweight='bold')

    # 轴设置
    ax.set_xticks([x_center])
    ax.set_xticklabels([title], fontsize=10)
    ax.set_title(title, fontweight='bold', fontsize=11)
    ax.tick_params(axis='both', which='major', labelsize=9, length=3, pad=1)

    # Pop 使用科学计数法
    if title == 'POP':
        formatter = ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((0, 0))
        ax.yaxis.set_major_formatter(formatter)
        offset_text = ax.yaxis.get_offset_text()
        offset_text.set_fontsize(8)
        offset_text.set_x(-0.4)

    ax.set_ylabel('')

    # 去除 top 和 right 图框线
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# 保存图像
plt.savefig(
    r'D:\Desktop_file\徐南老师\PPT\FigXX_Hotspot_Violin_Final.jpg',
    dpi=300,
    bbox_inches='tight',
    pad_inches=0.1
)

plt.show()
