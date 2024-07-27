import re
import sys

def replace_markdown_links(content):
    # 正则表达式匹配 [ ](static/{path}) 的格式
    pattern = r'\[\]\(static/(.*?)\)'
    # 定义替换模板
    replacement_template = r'<div class="row mt-3">\n    {% include figure.html path="assets/img/feishu_docs_static/\1" class="img-fluid rounded z-depth-1" %}\n</div>\n'
    
    # 使用 re.sub 进行替换
    replaced_content = re.sub(pattern, replacement_template, content)
    return replaced_content

def process_file(input_filename, output_filename=None):
    with open(input_filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    new_content = replace_markdown_links(content)
    
    # 如果没有指定输出文件名，则默认覆盖原文件
    if output_filename is None:
        output_filename = input_filename
    
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(new_content)
        print(f"File '{input_filename}' has been processed and saved as '{output_filename}'.")

if __name__ == "__main__":
     # 从命令行获取输入文件名
    if len(sys.argv) < 1:
        print("Usage: python script_name.py input_filename [output_filename]")
        sys.exit(1)

    input_filename = sys.argv[1]
    # 可选：指定输出文件名，如果不指定则覆盖原文件
    output_filename = input_filename

    process_file(input_filename, output_filename)