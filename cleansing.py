import pandas as pd
import os

# 定义文件夹路径
folder_path = 'your file_path'  # 替换为你的文件夹路径

# 定义输出文件路径
output_path = 'your output_file_path'  # 替换为你的输出文件路径

# 获取文件夹中的所有Excel文件
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# 创建一个空的DataFrame来存储筛选后的数据
filtered_data = pd.DataFrame()

# 遍历每个Excel文件
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path)

    # 筛选出目的地机场代号为ANC的行
    filtered_df = df[df['DAC'] == 'ANC']

    # 将筛选后的数据添加到总的DataFrame中
    filtered_data = pd.concat([filtered_data, filtered_df], ignore_index=True)

# 保存筛选后的数据到新的Excel文件
filtered_data.to_excel(output_path, index=False)

print(f"筛选后的数据已保存到 {output_path}")