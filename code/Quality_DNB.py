""" import os
import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt

# 设置输入输出路径
input_folder = "E:\\001-151\\Quailyt_flag\\"  # 替换为你的tif影像文件夹
output_folder = "E:\\001-151\\Quailty_result\\"              # 输出文件夹
os.makedirs(output_folder, exist_ok=True)

# 获取所有tif影像路径
tif_files = sorted([os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".tif")])

# 读取第一幅影像，获取基本信息
sample_ds = gdal.Open(tif_files[0])
cols = sample_ds.RasterXSize
rows = sample_ds.RasterYSize
geotransform = sample_ds.GetGeoTransform()
projection = sample_ds.GetProjection()

# 初始化4个类别的计数数组
count_0 = np.zeros((rows, cols), dtype=np.uint16)
count_1 = np.zeros((rows, cols), dtype=np.uint16)
count_2 = np.zeros((rows, cols), dtype=np.uint16)
count_255 = np.zeros((rows, cols), dtype=np.uint16)

# 遍历每张图像，统计每个类别的次数
print("开始统计每类像元值的次数...")
for i, tif_file in enumerate(tif_files):
    ds = gdal.Open(tif_file)
    band = ds.GetRasterBand(1)
    data = band.ReadAsArray()

    count_0 += (data == 0)
    count_1 += (data == 1)
    count_2 += (data == 2)
    count_255 += (data == 255)

    print(f"处理第 {i+1}/{len(tif_files)} 张影像: {os.path.basename(tif_file)}")

# 保存统计结果为影像
def save_tif(array, out_path):
    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(out_path, cols, rows, 1, gdal.GDT_UInt16)
    out_ds.SetGeoTransform(geotransform)
    out_ds.SetProjection(projection)
    out_ds.GetRasterBand(1).WriteArray(array)
    out_ds.FlushCache()
    out_ds = None

save_tif(count_0, os.path.join(output_folder, "count_0.tif"))
save_tif(count_1, os.path.join(output_folder, "count_1.tif"))
save_tif(count_2, os.path.join(output_folder, "count_2.tif"))
save_tif(count_255, os.path.join(output_folder, "count_255.tif"))
print("四张统计影像保存完成。")

# 生成纬度数组
lat_start = geotransform[3]
pixel_height = geotransform[5]
latitudes = np.array([lat_start + i * pixel_height for i in range(rows)])

# 统计每一纬度（行）上的总像元数（按行求和）
def aggregate_by_latitude(count_array):
    return np.sum(count_array, axis=1)

agg_0 = aggregate_by_latitude(count_0)
agg_1 = aggregate_by_latitude(count_1)
agg_2 = aggregate_by_latitude(count_2)
agg_255 = aggregate_by_latitude(count_255)

# 绘折线图函数
# 新的绘图函数：论文风格折线图
def plot_lat_distribution(latitudes, counts, label, out_filename):
    # 设置字体
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.figure(figsize=(6, 3), dpi=300)  # 适合论文插图：高分辨率
    plt.plot(latitudes, counts, label=label, color='#0072B2', linewidth=1)  # 单色线条，SCI风格

    plt.xlabel("Latitude", fontsize=10)
    plt.ylabel("Pixel Count", fontsize=10)
    #plt.title(f"{label}", fontsize=11)
    
    # 移除网格线
    plt.grid(False)
    # 设置Y轴为科学计数法
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

    # 获取当前坐标轴并设置科学计数法格式
    ax = plt.gca()
    ax.yaxis.get_offset_text().set_fontsize(9)
    # 设置图例
    plt.legend(loc='best', fontsize=9, frameon=False)

    # 设置刻度字体
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, out_filename), dpi=300, bbox_inches='tight')
    plt.close()

# 调用绘图函数：使用论文标准图例名称
plot_lat_distribution(latitudes, agg_0, "Persistent Nighttime Lights", "lat_dist_0.png")
plot_lat_distribution(latitudes, agg_1, "Ephemeral Nighttime Lights", "lat_dist_1.png")
plot_lat_distribution(latitudes, agg_2, "Outlier (Potential Cloud Contamination)", "lat_dist_2.png")
plot_lat_distribution(latitudes, agg_255, "Fill Value", "lat_dist_255.png")
plt.show()
print("折线图保存完成。")
 """
import os
import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt

# 设置输入输出路径
input_folder = "E:\\001-151\\Quailyt_flag\\"  # 替换为你的tif影像文件夹
output_folder = "E:\\001-151\\Quailty_result\\"              # 输出文件夹
os.makedirs(output_folder, exist_ok=True)

# 获取所有tif影像路径
tif_files = sorted([os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".tif")])

# 读取第一幅影像，获取基本信息
sample_ds = gdal.Open(tif_files[0])
cols = sample_ds.RasterXSize
rows = sample_ds.RasterYSize
geotransform = sample_ds.GetGeoTransform()
projection = sample_ds.GetProjection()

# 初始化4个类别的计数数组
count_0 = np.zeros((rows, cols), dtype=np.uint16)
count_1 = np.zeros((rows, cols), dtype=np.uint16)
count_2 = np.zeros((rows, cols), dtype=np.uint16)
count_255 = np.zeros((rows, cols), dtype=np.uint16)

# 遍历每张图像，统计每个类别的次数
print("开始统计每类像元值的次数...")
for i, tif_file in enumerate(tif_files):
    ds = gdal.Open(tif_file)
    band = ds.GetRasterBand(1)
    data = band.ReadAsArray()

    count_0 += (data == 0)
    count_1 += (data == 1)
    count_2 += (data == 2)
    count_255 += (data == 255)

    print(f"处理第 {i+1}/{len(tif_files)} 张影像: {os.path.basename(tif_file)}")

# 保存统计结果为影像
def save_tif(array, out_path):
    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(out_path, cols, rows, 1, gdal.GDT_UInt16)
    out_ds.SetGeoTransform(geotransform)
    out_ds.SetProjection(projection)
    out_ds.GetRasterBand(1).WriteArray(array)
    out_ds.FlushCache()
    out_ds = None

save_tif(count_0, os.path.join(output_folder, "count_0.tif"))
save_tif(count_1, os.path.join(output_folder, "count_1.tif"))
save_tif(count_2, os.path.join(output_folder, "count_2.tif"))
save_tif(count_255, os.path.join(output_folder, "count_255.tif"))
print("四张统计影像保存完成。")

# 生成纬度数组
lat_start = geotransform[3]
pixel_height = geotransform[5]
latitudes = np.array([lat_start + i * pixel_height for i in range(rows)])

# 统计每一纬度（行）上的总像元数（按行求和）
def aggregate_by_latitude(count_array):
    return np.sum(count_array, axis=1)

agg_0 = aggregate_by_latitude(count_0)  # 高质量像元（值为0）
agg_1 = aggregate_by_latitude(count_1)
agg_2 = aggregate_by_latitude(count_2)
agg_255 = aggregate_by_latitude(count_255)

# 计算每行总像元数（所有类别的总和）
total_pixels_per_row = agg_0 + agg_1 + agg_2 + agg_255

# 计算高质量像元百分比（避免除以零）
high_quality_percentage = np.zeros_like(agg_0, dtype=np.float64)
for i in range(len(agg_0)):
    if total_pixels_per_row[i] > 0:
        high_quality_percentage[i] = (agg_0[i] / total_pixels_per_row[i]) * 100
    else:
        high_quality_percentage[i] = 0.0

# 输出X（纬度）和Y（高质量像元百分比）到文件
def save_latitude_percentage_data(latitudes, percentages, output_file):
    """
    保存纬度和高质量像元百分比到文本文件
    """
    with open(output_file, 'w') as f:
        f.write("Latitude,High_Quality_Pixel_Percentage\n")
        for lat, percentage in zip(latitudes, percentages):
            f.write(f"{lat:.6f},{percentage:.6f}\n")
    print(f"纬度百分比数据已保存到: {output_file}")

# 保存高质量像元百分比数据
save_latitude_percentage_data(latitudes, high_quality_percentage, 
                             os.path.join(output_folder, "latitude_high_quality_percentage.csv"))
# 可选：保存其他类别的百分比数据供参考
def calculate_percentage(main_array, total_array):
    """计算百分比"""
    percentage = np.zeros_like(main_array, dtype=np.float64)
    for i in range(len(main_array)):
        if total_array[i] > 0:
            percentage[i] = (main_array[i] / total_array[i]) * 100
        else:
            percentage[i] = 0.0
    return percentage

# 计算并保存其他类别的百分比
ephemeral_percentage = calculate_percentage(agg_1, total_pixels_per_row)
outlier_percentage = calculate_percentage(agg_2, total_pixels_per_row)
fillvalue_percentage = calculate_percentage(agg_255, total_pixels_per_row)

save_latitude_percentage_data(latitudes, ephemeral_percentage, 
                             os.path.join(output_folder, "latitude_ephemeral_percentage.csv"))
save_latitude_percentage_data(latitudes, outlier_percentage, 
                             os.path.join(output_folder, "latitude_outlier_percentage.csv"))
save_latitude_percentage_data(latitudes, fillvalue_percentage, 
                             os.path.join(output_folder, "latitude_fillvalue_percentage.csv"))
plt.show()
print("处理完成！")