'''
Compony: NUC
Date: 2026-05-30 10:09:14
LastEditors: Loong2525
LastEditTime: 2026-05-30 10:09:14
'''
# 考察内容1：创建集合的方式
word_set1 = {"apple:苹果", "hello:你好"}
# 方式二：使用set()函数（可创建空集合）
word_set2 = set()  
word_set = word_set1  # 初始有示例单词

def show_menu():
    print("\n===== 单词记录本 =====")
    print("1. 查看单词本")
    print("2. 背单词")
    print("3. 添加新单词")
    print("4. 删除单词")
    print("5. 清空单词本")
    print("6. 退出")
    print("====================")

def view_words():
    """查看单词本"""
    if len(word_set) == 0:
        print("单词本内容为空")
    else:
        print("当前单词本：")
        for w in word_set:
            print("  " + w)

def recite_words():
    """背单词功能"""
    if len(word_set) == 0:
        print("单词本内容为空，无法背单词")
        return
    print("开始背单词（输入翻译，输入q退出）")
    for item in word_set:
        # item格式："单词:翻译"
        word, meaning = item.split(":", 1)
        user_input = input(f"{word} 的意思是？ (输入q退出): ").strip()
        if user_input.lower() == 'q':
            break
        if user_input == meaning:
            print("太棒了！")
        else:
            print(f"再想想，正确答案是：{meaning}")

def add_word():
    """添加新单词"""
    word = input("请输入要添加的单词: ").strip()
    # 检查是否已存在（按单词部分判断）
    exists = False
    for item in word_set:
        if item.startswith(word + ":"):
            exists = True
            break
    if exists:
        print("添加单词重复")
        return
    meaning = input(f"请输入单词 '{word}' 的翻译: ").strip()
    new_entry = f"{word}:{meaning}"
    # 考察内容2：集合内置方法（add）
    word_set.add(new_entry)
    print(f"单词 '{word}' 添加成功！")

def delete_word():
    """删除单词"""
    if len(word_set) == 0:
        print("单词本为空")
        return
    # 先展示所有单词
    print("当前单词列表：")
    for item in word_set:
        word = item.split(":", 1)[0]
        print("  " + word)
    to_del = input("请输入要删除的单词: ").strip()
    # 查找匹配项
    found = None
    for item in word_set:
        if item.startswith(to_del + ":"):
            found = item
            break
    if found:
        # 考察内容2：discard() 删除集合元素
        word_set.discard(found)
        print(f"单词 '{to_del}' 已删除")
    else:
        print("删除的单词不存在")

def clear_words():
    """清空单词本"""
    if len(word_set) == 0:
        print("单词本为空")
    else:
        # 考察内容2：clear() 清空集合
        word_set.clear()
        print("单词本已清空")

def main():
    while True:
        show_menu()
        choice = input("请选择操作(1-6): ").strip()
        if choice == '1':
            view_words()
        elif choice == '2':
            recite_words()
        elif choice == '3':
            add_word()
        elif choice == '4':
            delete_word()
        elif choice == '5':
            clear_words()
        elif choice == '6':
            print("退出单词记录本，再见！")
            break
        else:
            print("无效输入，请重新选择")

if __name__ == "__main__":
    main()