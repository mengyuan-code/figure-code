import matplotlib.colors as mc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.cm import ScalarMappable

# File paths
file_paths = [
    r"F:\Results\ssp126\4\2020\CHN\chn\osm_id_4352781_2020.csv",
    r"F:\Results\ssp126\4\2030\CHN\chn\osm_id_4352781_2030.csv",
    r"F:\Results\ssp126\4\2040\CHN\chn\osm_id_4352781_2040.csv",
    r"F:\Results\ssp126\4\2050\CHN\chn\osm_id_4352781_2050.csv",
    r"F:\Results\ssp126\4\2060\CHN\chn\osm_id_4352781_2060.csv",
    r"F:\Results\ssp126\4\2070\CHN\chn\osm_id_4352781_2070.csv",
    r"F:\Results\ssp126\4\2080\CHN\chn\osm_id_4352781_2080.csv",
    r"F:\Results\ssp126\4\2090\CHN\chn\osm_id_4352781_2090.csv",
    r"F:\Results\ssp126\4\2100\CHN\chn\osm_id_4352781_2100.csv",
]

# Load data
dfs = []
for path in file_paths:
    year = int(path.split("_")[-1].split(".")[0])  # Extract year from filename
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["datetime"])
    df["year"] = year
    dfs.append(df)

# Combine all data into one DataFrame
data = pd.concat(dfs)

# Set temperature range
MIN_TEMP = data["Surface_temperature"].min()
MAX_TEMP = data["Surface_temperature"].max()

def single_plot(data, month, year, ax):
    # 确保列是 datetime 类型
    if not pd.api.types.is_datetime64_any_dtype(data["date"]):
        data["date"] = pd.to_datetime(data["date"])

    # 筛选指定年份和月份的数据
    data = data[(data["date"].dt.year == year) & (data["date"].dt.month == month)]

    # 提取小时、日期和温度
    hour = data["date"].dt.hour
    day = data["date"].dt.day
    temp = data["Surface_temperature"]

    # 验证数据完整性并重塑温度矩阵
    try:
        temp = temp.values.reshape(24, len(day.unique()), order="F")
    except ValueError as e:
        print(f"Error reshaping data for year {year}, month {month}: {e}")
        return

    # 生成网格
    xgrid = np.arange(day.min(), day.max() + 2)
    ygrid = np.arange(25)

    # 绘制热图
    ax.pcolormesh(xgrid, ygrid, temp, cmap="magma", vmin=MIN_TEMP, vmax=MAX_TEMP)
    # Invert the vertical axis
    ax.set_ylim(24, 0)
    # Set tick positions for both axes
    ax.yaxis.set_ticks([i for i in range(24)])
    ax.xaxis.set_ticks([10, 20, 30])
    # Remove ticks by setting their length to 0
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    
    # Remove all spines
    ax.set_frame_on(False)

fig, axes = plt.subplots(2, 12, figsize=(20, 12), sharey=True)

years = sorted(data["year"].unique())  # 从数据中提取所有年份
months = range(1, 13)

n_years = len(years)
# adjust layout
fig, axes = plt.subplots(n_years, 12, figsize=(24, n_years * 3.5), sharey=True)
axes = np.atleast_2d(axes)

#yearly_stats = data.groupby("year")["Surface_temperature"].agg(["min", "max", "mean"])
#print(yearly_stats)
#yearly_stats.plot(y=["min", "max", "mean"], title="Yearly Temperature Range")


for i, year in enumerate(years):
    for j, month in enumerate(months):
        single_plot(data, month, year, axes[i, j])

# 调整子图间距
fig.subplots_adjust(left=0.05, right=0.98, top=0.88, bottom=0.12, hspace=0.3, wspace=0.1)

# 创建颜色条（放在底部，完整对齐图像）
cbar_ax = fig.add_axes([0.2, 0.06, 0.6, 0.02])  # x起点, y起点, 宽度, 高度
norm = mc.Normalize(MIN_TEMP, MAX_TEMP)
cb = fig.colorbar(
    ScalarMappable(norm=norm, cmap="magma"),
    cax=cbar_ax,
    orientation="horizontal"
)
cb.ax.xaxis.set_tick_params(size=0)
cb.set_label("Temperature (°C)", size=14)  # 增大字体

# 设置全局标签
#fig.text(0.5, 0.05, "Day", ha="center", fontsize=16)  # 调整到更低的位置
fig.text(0.02, 0.5, "Hour Commencing", va="center", rotation="vertical", fontsize=16)

# 设置标题，调整到更高位置
fig.suptitle("Hourly Surface Temperatures - road 4352781", fontsize=24, y=0.94)  # 将标题抬高

# 保存图像
fig.set_facecolor("white")
fig.savefig(r"E:\组会\文献汇报\图\Heatmap\10_years_plot.png", dpi=800)
