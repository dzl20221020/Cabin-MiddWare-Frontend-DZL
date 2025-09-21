import os

# 目标文件夹路径
folder_path = r"E:\doing\touchscreen-display\data\data"

# 保存文件路径
output_file = "calibdata.txt"

# 获取目录下所有的jpg文件路径
jpg_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg')]

# 将文件路径写入到calibdata.txt文件中
with open(output_file, 'w') as f:
    for file_path in jpg_files:
        f.write(file_path + '\n')

print(f"已生成 {output_file} 文件，共包含 {len(jpg_files)} 个图像路径。")
