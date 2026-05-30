'''
Compony: NUC
Date: 2026-05-30 10:05:10
LastEditors: Loong2525
LastEditTime: 2026-05-30 10:08:03
'''

def idiom_dragon(idioms, start):
    # 验证起始成语
    if not idioms or start not in idioms:
        return None
    result = [start]
    remaining = [i for i in idioms if i != start]
    # 外层循环控制查找次数
    for _ in range(len(remaining)):
        last_word = result[-1][-1]  # 最后一个字
        found = False
        # 内层循环遍历剩余成语
        for i, idiom in enumerate(remaining):
            if idiom[0] == last_word:
                result.append(idiom)
                remaining.pop(i)
                found = True
                break
        if not found:
            print("接龙失败，无法继续")
            return None
    return result

if __name__ == "__main__":
    idioms = ["万事如意", "发愤图强", "笑容满面", "意气风发", "强颜欢笑"]
    start = "万事如意"
    dragon = idiom_dragon(idioms, start)
    if dragon:
        print("接龙成功：")
        print(" -> ".join(dragon))
    else:
        print("无法完成接龙")