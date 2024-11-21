import os
import pandas as pd

def read_asc_file(file_path, delimiter):
    """
    读取ASC文件并返回文件内容
    :param file_path: ASC文件的路径
    :param delimiter: 数据之间的分隔符
    :return: 文件内容
    """
    try:
        # 检查文件路径是否存在
        if not os.path.exists(file_path):
            print(f"文件 {file_path} 不存在")
            return None

        # 检查文件路径是否为文件
        if not os.path.isfile(file_path):
            print(f"{file_path} 不是一个文件")
            return None

        # 使用pandas读取文件，指定分隔符
        df = pd.read_csv(file_path, delimiter=delimiter, header=None)
        return df
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
        return None
    except PermissionError:
        print(f"没有权限读取文件 {file_path}")
        return None
    except OSError as e:
        print(f"读取文件时发生错误: {e}")
        return None
    except Exception as e:
        print(f"读取文件时发生未知错误: {e}")
        return None

def convert_to_excel(file_path, output_path, delimiter):
    """
    将ASC文件内容转换为Excel文件
    :param file_path: ASC文件的路径
    :param output_path: 输出Excel文件的路径
    :param delimiter: 数据之间的分隔符
    """
    df = read_asc_file(file_path, delimiter)
    if df is None:
        return

    # 将DataFrame写入Excel文件
    df.to_excel(output_path, index=False, header=False)

    print(f"数据已成功写入 {output_path}")

def main():
    # 指定文件路径
    file_path = r'your file_path'  # 替换为你的文件路径
    output_path = r'your output_file_path'  # 替换为你的输出文件路径
    delimiter = '|'  # 替换为你的分隔符

    # 将ASC文件内容转换为Excel文件
    convert_to_excel(file_path, output_path, delimiter)

if __name__ == "__main__":
    main()