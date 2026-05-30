'''
Compony: NUC
Date: 2026-05-30 09:58:18
LastEditors: Loong2525
LastEditTime: 2026-05-30 10:51:35
'''

def split_poem_lines(text):
    # 定义分隔符集合
    delimiters = {'。', '！', '？', '；', '.', '!', '?', ';'}
    lines = []
    start = 0
    for i, ch in enumerate(text):
        if ch in delimiters:
            # 提取从start到i（包含标点）的子串
            sentence = text[start:i+1].strip()
            if sentence:
                lines.append(sentence)
            start = i + 1
    # 处理最后可能没有标点结尾的内容
    if start < len(text):
        remaining = text[start:].strip()
        if remaining:
            lines.append(remaining)
    return lines

def main():

    # 输入标题（使用strip删除首尾空白）
    title = input("请输入古诗标题：").strip()
    if not title:
        title = "无题"
    
    # 输入作者（使用strip）
    author = input("请输入作者（如 唐·李白 或 先秦*佚名）：").strip()
    if not author:
        author = "佚名"
    
    # 输入诗句（一整行）
    print("请输入诗句（一整行，句子间用句号、感叹号等分隔）：")
    poem_line = input()
    poem_line = poem_line.lstrip().rstrip()
    
    if not poem_line:
        print("未输入诗句，程序结束。")
        return
    
    # 自动分割成单句列表
    poem_lines = split_poem_lines(poem_line)
    
    if not poem_lines:
        print("无法识别诗句，请使用句号、感叹号、问号或分号分隔。")
        return
    
    # 输出排版结果
    print("\n" + "=" * 40)
    print("排版结果：")
    print("=" * 40)
    print(title.center(40))   # 标题居中
    print(author.center(40))  # 作者居中
    # 每个单句占一行
    for line in poem_lines:
        print(line.center(40))

if __name__ == "__main__":
    main()