'''
Compony: NUC
Date: 2026-05-30 09:09:49
LastEditors: Loong2525
LastEditTime: 2026-05-30 09:25:41
'''

def remove_spaces(text):
    """删除所有半角空格"""
    return text.replace(' ', '')

def replace_punctuation(text):
    """将英文标点替换为中文标点"""
    trans_table = str.maketrans({
        ',': '，',
        '.': '。',
        '?': '？',
        '!': '！',
        ';': '；',
        ':': '：'
    })
    return text.translate(trans_table)

def capitalize_words(text):
    """
    将英文单词的首字母大写，其余字母小写。
    使用纯字符串操作，逐字符识别连续的字母序列。
    """
    result = []
    i = 0
    n = len(text)
    while i < n:
        # 如果当前字符不是字母，直接保留
        if not text[i].isalpha():
            result.append(text[i])
            i += 1
        else:
            # 找到连续字母的起始位置
            start = i
            while i < n and text[i].isalpha():
                i += 1
            # 提取单词并转换：首字母大写，其余字母小写
            word = text[start:i]

            new_word = word[0].upper() + word[1:].lower()
            result.append(new_word)

    return ''.join(result)

def main():
    # 步骤1：定义需要处理的原始字符串
    original_text = "hello world! 这是一个测试。   please remove spaces.  i like python."
    
    # 步骤2：打印初始字符串和功能菜单
    current_text = original_text
    print("=" * 50)
    print("文字排版工具")
    print("=" * 50)
    print("原始字符串：")
    print(original_text)
    print("\n功能菜单：")
    print("1 - 删除空格")
    print("2 - 英文标点替换（替换为中文标点）")
    print("3 - 英文单词首字母大写")
    print("4 - 重置为原始文本")
    print("5 - 退出程序")
    print("-" * 50)
    
    # 步骤3：创建无限循环（保证程序持续运行）
    while True:
        # 步骤4：接收用户输入的功能选项
        choice = input("\n请输入功能编号（1-5）：").strip()
        
        # 步骤5：编写多分支判断（if-elif）
        if choice == '1':
            current_text = remove_spaces(current_text)
            print("\n【删除空格后】")
            print(current_text)
        elif choice == '2':
            current_text = replace_punctuation(current_text)
            print("\n【英文标点替换后】")
            print(current_text)
        elif choice == '3':
            current_text = capitalize_words(current_text)
            print("\n【英文单词首字母大写后】")
            print(current_text)
        elif choice == '4':
            current_text = original_text
            print("\n【已重置为原始文本】")
            print(current_text)
        elif choice == '5':
            print("感谢使用文字排版工具，再见！")
            break
        else:
            print("输入无效，请输入1~5之间的数字。")
        

if __name__ == "__main__":
    main()