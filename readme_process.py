import re

# --- 配置区域 ---
# 在这里修改你的输入和输出文件名
INPUT_FILE = "README.md"
OUTPUT_FILE = "README_for_tex.tex"

# 当标题只有数字时，替换成的字符串
UNTITLED_PLACEHOLDER = "无名-节选"
# --- 配置结束 ---


def latex_escape(text):
    """
    对文本进行转义，以适应LaTeX环境。这是必要的安全步骤。
    """
    conv = {
        '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
        '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}', '\\': '',
    }
    regex = re.compile('|'.join(re.escape(key) for key in sorted(conv.keys(), key=lambda item: -len(item))))
    return regex.sub(lambda match: conv[match.group()], text)


def convert_markdown_to_latex(input_file, output_file):
    """
    根据指定规则解析Markdown诗歌文件并转换为LaTeX格式。
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"错误：找不到输入文件 '{input_file}'，请检查文件名是否正确。")
        return

    tex_output_lines = []
    
    # 增加一个虚拟的空行到末尾，便于统一处理文件的最后一行诗
    lines.append('\n')
    
    num_lines = len(lines)
    # 我们需要“向后看”一行，所以循环到倒数第二行即可
    for i in range(2, num_lines - 1):
        current_line_raw = lines[i]
        current_line = current_line_raw.strip()
        
        next_line = lines[i+1].strip()

        # 当前行是空行
        if current_line == "":
            tex_output_lines.append("\n")  # 保持空行
            continue

        # 规则1：处理特殊标记 <br>，直接转换为段落间距
        if current_line == "<br>":
            tex_output_lines.append("\n\\clearpage\n")  # 使用 \clearpage 来强制分页
            lines[i+1] = ""  # 将下一行设置为空，避免重复处理
            continue

        # 规则2：处理标题行 (以####开头)
        if current_line.startswith('#### '):
            title_content = current_line[5:].strip()
            
            # 判断标题内容是否仅为数字
            if re.fullmatch(r'\d+', title_content):
                section_title = UNTITLED_PLACEHOLDER
            # 判断是否只有标题（去掉数字）
            elif re.match(r'\d+《.*》', title_content) or re.match(r'\d+\s+.*', title_content):
                 # 匹配 "数字《标题》" 或 "数字 标题" 格式，并去掉数字部分
                 section_title = re.sub(r'^\d+\s*?', '', title_content)
            else:
                section_title = title_content
            
            # 使用\section（计入目录），并对标题内容进行安全转义
            tex_output_lines.append(f"\\section{{{latex_escape(section_title)}}}\n\n")
            continue

        # 规则3：处理正文和空行
        
        # 如果当前行是 \，且下一行不是特殊标记，则转换为段落间距
        if current_line == "\\":
            # 只有在下一行不是特殊标记(\或<br>)时，才将这个空行转换为空白
            if next_line != "<br>":
                tex_output_lines.append("\\vspace{1em}\n\n")
            continue
        
        # 判断当前行是否为段落结尾
        # 段落结尾的条件：下一行是 `\` 或 `<br>`
        is_paragraph_end = False
        if next_line == "\\" or next_line == "<br>":
            is_paragraph_end = True
        
        # 对当前行内容进行安全转义
        escaped_line = latex_escape(current_line)
        
        if is_paragraph_end:
            # 是段落结尾，末尾不加 \\
            tex_output_lines.append(f"{escaped_line}\n")
        else:
            # 不是段落结尾，末尾加 \\
            tex_output_lines.append(f"{escaped_line} \\\\\n")
        

    # 写入到输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("% !TEX encoding = UTF-8\n")
        f.write("% 此文件由Python脚本自动生成\n")
        f.write("% 请在您的主.tex文件中使用 \\input{...} 来包含它\n\n")
        f.writelines(tex_output_lines)

    print(f"转换完成！内容已写入到 '{output_file}'")


# --- 主执行逻辑 ---
# 当你运行这个 .py 文件时，下面的函数会被调用
if __name__ == '__main__':
    convert_markdown_to_latex(INPUT_FILE, OUTPUT_FILE)