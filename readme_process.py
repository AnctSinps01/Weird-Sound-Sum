def replace_double_spaces(input_file, output_file):
    try:
        # 读取文件内容
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 执行替换：将双空格 "  " 替换为反斜杠 "\"
        # 注意：在 Python 字符串字面量中，反斜杠需要转义，所以写为 "\\"
        new_content = content.replace("  ", "\\")
        
        # 写入新文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"处理完成！文件已保存至: {output_file}")
        
    except FileNotFoundError:
        print(f"错误：找不到文件 '{input_file}'，请检查文件名或路径。")
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == "__main__":
    # 配置文件名
    input_filename = "README.md"   # 请确保该文件存在于当前目录
    output_filename = "README.md"  # 替换后的文件将保存到这里
    
    # 如果你想直接覆盖原文件，可以将 output_filename 也设为 input_filename
    # output_filename = input_filename 
    
    replace_double_spaces(input_filename, output_filename)