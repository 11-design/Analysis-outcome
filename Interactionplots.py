import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

# ---------------------------------------------------------
# 1. 数据加载 (如果您有本地文件，请修改 pd.read_csv 的路径)
# 这里为了演示，我直接使用刚才的字符串数据
# ---------------------------------------------------------
csv_content = """时间戳记,Age,vocal type,Select the task,Name (first and second),How mentally demanding was the task?,How physically demanding was the task?,How hurried or rushed was the pace of the task?,How successful were you in accomplishing what you were asked to do?,How hard did you have to work to accomplish your level of performance?,"How insecure, discouraged, irritated, stressed, and annoyed were you?"
2025-12-5 上午10:22:10,25,soft,Digital span memory test,David Masson,4,1,3,3,4,2
2025-12-5 上午10:26:36,25,soft,Symbol search,David Masson,4,1,4,3,4,3
2025-12-5 上午10:59:44,25,hard,Symbol search,David Masson,4,1,4,3,4,3
2025-12-5 上午11:03:28,25,hard,Digital span memory test,David Masson,4,1,4,3,4,3
2025-12-5 上午11:28:24,21,soft,Symbol search,Yue Zhu,3,4,2,5,3,3
2025-12-5 上午11:33:02,21,soft,Digital span memory test,Yue Zhu,4,4,4,4,5,5
2025-12-5 下午12:10:19,23,soft,Digital span memory test,Anna Likhanova,3,1,4,2,4,4
2025-12-5 下午12:10:32,23,soft,Digital span memory test,Jiwoo Lee,3,1,2,1,3,2
2025-12-5 下午12:14:56,23,soft,Symbol search,Anna Likhanova,4,1,4,4,3,2
2025-12-5 下午12:15:05,23,soft,Symbol search,Jiwoo Lee,2,1,3,3,3,2
2025-12-5 下午12:45:03,24,soft,Symbol search,Hao Xin,3,4,4,4,3,2
2025-12-5 下午12:45:23,24,soft,Symbol search,Yu Shin Liou,3,1,3,1,4,1
2025-12-5 下午12:52:03,24,soft,Digital span memory test,Yu Shin Liou,5,1,3,3,4,1
2025-12-5 下午12:54:07,24,soft,Digital span memory test,Hao Xin,4,4,3,3,4,4
2025-12-5 下午01:14:13,25,soft,Digital span memory test,Chen Hsueh,4,2,3,3,4,3
2025-12-5 下午01:14:16,25,soft,Digital span memory test,Wei-Chen Chiu,3,1,2,3,3,2
2025-12-5 下午01:19:21,25,soft,Symbol search,Chen Hsueh,4,3,5,4,5,2
2025-12-5 下午01:19:31,25,soft,Symbol search,Wei-Chen Chiu,2,2,4,4,2,1
2025-12-5 下午01:48:28,25,soft,Digital span memory test,Anna Deinhammer,4,2,4,2,5,4
2025-12-5 下午01:48:57,23,soft,Digital span memory test,Ella Stukenkemper,3,1,3,3,2,2
2025-12-5 下午01:49:10,25,soft,Digital span memory test,Paul Soeser,1,1,3,3,3,1
2025-12-5 下午01:54:31,25,soft,Symbol search,Anna Deinhammer,2,1,3,5,4,2
2025-12-5 下午01:54:39,23,soft,Symbol search,Ella Stukenkemper,3,2,4,4,2,3
2025-12-5 下午01:55:03,25,soft,Symbol search,Paul Soeser,3,1,5,4,4,1
2025-12-5 下午02:16:59,24,soft,Symbol search,Nathan,3,3,4,4,4,2
2025-12-5 下午02:20:57,24,soft,Digital span memory test,Nathan,5,3,5,2,3,4
2025-12-5 下午02:52:14,23,hard,Symbol search,Ella Stukenkemper,2,1,2,4,2,1
2025-12-5 下午02:52:26,25,hard,Symbol search,Anna Deinhammer,2,1,4,4,3,1
2025-12-5 下午02:52:33,25,hard,Symbol search,Paul Soeser,3,2,5,3,4,1
2025-12-5 下午02:55:41,25,hard,Digital span memory test,Anna Deinhammer,5,2,4,2,5,3
2025-12-5 下午02:55:45,23,hard,Digital span memory test,Ella Stukenkemper,3,1,2,3,2,2
2025-12-5 下午02:55:53,25,hard,Digital span memory test,Paul Soeser,2,2,3,3,4,2
2025-12-8 下午12:18:41,25,hard,Symbol search,Chen Hsueh,2,2,3,5,2,1
2025-12-8 下午12:18:46,24,soft,Symbol search,Anna Jaakonaho,2,1,3,4,2,1
2025-12-8 下午12:22:37,24,soft,Digital span memory test,Anna Jaakonaho,3,1,4,3,3,3
2025-12-8 下午12:24:19,25,hard,Digital span memory test,Chen Hsueh,3,2,1,3,3,2
2025-12-8 下午12:48:04,25,hard,Symbol search,Wei-Chen Chiu,1,2,2,4,2,1
2025-12-8 下午12:48:10,23,hard,Symbol search,Anna Likhanova,2,1,3,4,2,1
2025-12-8 下午12:51:21,23,hard,Digital span memory test,Anna Likhanova,5,1,4,2,4,2
2025-12-8 下午12:51:28,25,hard,Digital span memory test,Wei-Chen Chiu,4,3,4,3,5,1
2025-12-8 下午01:07:59,24,hard,Digital span memory test,Anna Jaakonaho,3,1,3,3,4,3
2025-12-8 下午01:08:07,24,soft,Digital span memory test,Kimmy Karlsson Kochar,4,1,3,4,5,2
2025-12-8 下午01:12:22,24,soft,Symbol search,Kimmy Karlsson Kochar,4,3,4,5,4,2
2025-12-8 下午01:12:27,24,hard,Symbol search,Anna Jaakonaho,2,1,2,4,2,1
2025-12-8 下午01:37:02,24,hard,Digital span memory test,Nathan Voss,4,2,4,3,4,3
2025-12-8 下午01:40:17,24,hard,Symbol search,Nathan Voss,4,2,3,3,3,3
2025-12-9 下午12:40:47,24,hard,Digital span memory test,Hao Xin Chen,3,4,2,4,4,2
2025-12-9 下午12:40:57,24,hard,Digital span memory test,Yu Shin Liou,4,1,3,2,4,2
2025-12-9 下午12:44:47,24,hard,Symbol search,Hao Xin Chen,2,4,3,4,4,4
2025-12-9 下午12:44:56,24,hard,Symbol search,Yu Shin Liou,4,1,4,3,4,1
2025-12-9 下午01:18:02,24,hard,Symbol search,Kimmy Karlsson Kochar,3,1,4,3,5,4
2025-12-9 下午01:18:12,23,hard,Symbol search,Jiwoo Lee ,1,1,2,4,2,1
2025-12-9 下午01:21:24,24,hard,Digital span memory test,Kimmy Karlsson Kochar,5,1,4,2,5,3
2025-12-9 下午01:21:29,23,hard,Digital span memory test,Jiwoo Lee,3,1,3,2,3,2"""

# 读取数据
df = pd.read_csv(io.StringIO(csv_content))

# 给列重命名（处理原始的长问题名）
df.columns = ["Timestamp", "Age", "VocalType", "Task", "Name", 
              "Mental", "Physical", "Temporal", "Success", "Effort", "Frustration"]

# ---------------------------------------------------------
# 2. 数据预处理
# ---------------------------------------------------------
# 反转 'Success' 分数，因为 NASA-TLX 中高分通常代表高负荷
# 原始问题是 "How successful were you?" (1=Low success?, 5=High success?)
# 通常 NASA-TLX 都是问 "How Insecure/Discouraged?" (High=Bad).
# 假设 5=非常成功(低负荷)，1=非常失败(高负荷)。
# 为了和其他指标（High=High Workload）一致，我们将其反转为 "Perceived Failure"
df['Perceived Failure'] = 6 - df['Success'] 

# 重命名列以方便绘图显示
plot_df = df.rename(columns={
    "Mental": "Mental Demand",
    "Physical": "Physical Demand",
    "Temporal": "Temporal Demand",
    "Effort": "Effort",
    "Frustration": "Frustration"
})

# 定义要画的 6 个维度
dimensions = ["Mental Demand", "Physical Demand", "Temporal Demand", 
              "Perceived Failure", "Effort", "Frustration"]

# ---------------------------------------------------------
# 3. 绘图 (Interaction Plots)
# ---------------------------------------------------------
# 设置 Seaborn 风格
sns.set(style="whitegrid")

# 创建画布：2行3列
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten() # 展平数组方便循环

# 颜色设置：Hard=红色, Soft=蓝色
palette = {"hard": "#e74c3c", "soft": "#3498db"}

for i, dim in enumerate(dimensions):
    # 使用 pointplot 绘制交互图
    # x轴: 任务类型, y轴: 维度分数, hue: 声音类型
    sns.pointplot(data=plot_df, x="Task", y=dim, hue="VocalType", 
                  markers=["o", "s"],       # 圆点和方块
                  linestyles=["-", "--"],   # 实线和虚线
                  capsize=.1,               # 误差棒帽子大小
                  errorbar="se",            # 误差棒显示标准误
                  ax=axes[i], 
                  palette=palette,
                  dodge=True)               #稍微错开一点，防止重叠
    
    # 图表美化
    axes[i].set_title(dim, fontsize=14, fontweight='bold')
    axes[i].set_xlabel("")      # 去掉X轴标签，因为大家都知道是任务
    axes[i].set_ylabel("Score (1-5)")
    axes[i].set_ylim(0.5, 5.5)  # 固定Y轴范围，方便对比

    # 图例控制：只在第一个图显示图例，其他的关掉
    if i == 0:
        axes[i].legend(title="Vocal Type", loc='upper left')
    else:
        axes[i].get_legend().remove()

# 自动调整布局，防止重叠
plt.tight_layout()

# 保存图片
plt.savefig('interaction_plots_six_dimensions.png', dpi=300)

# 显示图片
plt.show()

print("图表已生成并保存为 'interaction_plots_six_dimensions.png'")