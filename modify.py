import pandas as pd

# 读取数据
df = pd.read_excel('your file_path')

# 检查数据
print(df.head())

# 生成6位数格式的列
df['Date1'] = df['Year'].astype(str).str.zfill(4) + df['Month'].astype(str).str.zfill(2)

# 生成6位数并用 / 分隔的列
df['Date2'] = df['Year'].astype(str).str.zfill(4) + '/' + df['Month'].astype(str).str.zfill(2)

# 检查生成的列
print(df.head())

# 保存处理后的数据到新的Excel文件
df.to_excel('your output_file_path', index=False)

# 检查保存的文件
print("数据已保存到 processed_data.xlsx")