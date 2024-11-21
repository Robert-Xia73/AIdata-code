def read_asc_file(file_path):
    """
    读取ASC文件并返回文件内容
    :param file_path: ASC文件的路径
    :return: 文件内容
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
        return None
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return None

def main():
    # 指定文件路径
    file_path = 'your file_path'  # 替换为你的文件路径

    # 读取ASC文件
    content = read_asc_file(file_path)

    if content is not None:
        print("文件内容:")
        print(content)

if __name__ == "__main__":
    main()