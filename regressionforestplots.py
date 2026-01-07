import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import io

# ==========================================
# 1. 数据准备 (Data Preparation)
# ==========================================
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

df = pd.read_csv(io.StringIO(csv_content))
df.columns = ["Timestamp", "Age", "VocalType", "Task", "Name", "Mental", "Physical", "Temporal", "Success", "Effort", "Frustration"]

df['Failure'] = 6 - df['Success']

df['Vocal_Code'] = df['VocalType'].map({'soft': 0, 'hard': 1})
df['Task_Code'] = df['Task'].map({'Symbol search': 0, 'Digital span memory test': 1})

targets = ['Mental', 'Physical', 'Temporal', 'Failure', 'Effort', 'Frustration']

for col in targets:
    df[f'Z_{col}'] = (df[col] - df[col].mean()) / df[col].std()

results_data = []


predictors_list = ['Task_Code', 'Vocal_Code'] 

names_map = {
    'Vocal_Code': 'Vocal Type (Hard)',
    'Task_Code': 'Task Type (Memory)'
}

for target in targets:
    X = df[['Vocal_Code', 'Task_Code']] 
    X = sm.add_constant(X)
    
    y = df[f'Z_{target}']
    
    model = sm.OLS(y, X).fit()
    params = model.params
    conf = model.conf_int()
    conf.columns = ['Lower', 'Upper']
    
    for predictor in predictors_list:
        results_data.append({
            'Target': target,
            'Predictor': names_map[predictor],
            'Coef': params[predictor],
            'Lower': conf.loc[predictor, 'Lower'],
            'Upper': conf.loc[predictor, 'Upper']
        })

res_df = pd.DataFrame(results_data)

fig, ax = plt.subplots(figsize=(10, 8)) 

colors = {'Vocal Type (Hard)': '#e74c3c', 'Task Type (Memory)': '#3498db'}
markers = {'Vocal Type (Hard)': 's', 'Task Type (Memory)': 'o'}

y_positions = np.arange(len(targets))
height = 0.3 

for i, target in enumerate(targets):
    subset = res_df[res_df['Target'] == target]
    
    for j, predictor in enumerate(['Task Type (Memory)', 'Vocal Type (Hard)']):
        row = subset[subset['Predictor'] == predictor]
        if not row.empty:
            y_pos = i + (j - 0.5) * height 
            
            coef = row['Coef'].values[0]
            lower = row['Lower'].values[0]
            upper = row['Upper'].values[0]
            err = [[coef - lower], [upper - coef]]
            
            ax.errorbar(coef, y_pos, xerr=err, fmt=markers[predictor], color=colors[predictor], 
                        capsize=5, elinewidth=2, markersize=8, label=predictor if i == 0 else "")
            
            if (lower > 0) or (upper < 0):
                ax.text(coef, y_pos + 0.08, "*", ha='center', va='bottom', fontsize=16, fontweight='bold', color='black')

ax.set_yticks(y_positions)
ax.set_yticklabels([t.replace('Failure', 'Perceived Failure') for t in targets], fontsize=12, fontweight='bold')
ax.set_xlabel("Standardized Beta Coefficient (Std. Error)", fontsize=12)
ax.axvline(0, color='black', linestyle='--', linewidth=1) 
ax.set_title("Regression Forest Plot (Main Effects Only)", fontsize=14, fontweight='bold')
ax.legend(title="Predictors", loc='lower right')
ax.grid(axis='x', linestyle=':', alpha=0.7)

plt.tight_layout()
plt.savefig('regression_forest_no_interaction.png', dpi=300)
plt.show()

print("无交互项的森林图已生成！")