'''
Compony: NUC
Date: 2026-05-30 09:51:26
LastEditors: Loong2525
LastEditTime: 2026-05-30 09:57:11
'''

def check_password_strength(password):

    length = len(password)
    
    # 统计包含的字符种类
    has_digit = False      # 数字
    has_upper = False      # 大写字母
    has_lower = False      # 小写字母
    has_symbol = False     # 符号（非字母数字的字符）
    
    for ch in password:
        if ch.isdigit():
            has_digit = True
        elif ch.isupper():
            has_upper = True
        elif ch.islower():
            has_lower = True
        else:
            has_symbol = True
    
    categories = sum([has_digit, has_upper, has_lower, has_symbol])

    # 根据长度和种类数判断强度
    if length < 8:
        level = "弱"
        score = 1
    else:
        # 长度 >= 8
        if categories == 1:
            level = "弱"
            score = 1

        elif categories == 2:
            level = "中"
            score = 2

        elif categories == 3:
            level = "强"
            score = 3

        else:  # categories == 4
            level = "极强"
            score = 4

    return level, score


def main():
    print("密码强度分为 弱、中、强、极强 四个等级。")
    print("建议使用长度≥8且包含数字、大小写字母和符号的组合。")

    pwd = input("请输入需要检测的密码：")
    level, score =check_password_strength(pwd)
    print(f"\n检测结果：")
    print(f"密码：{pwd}")
    print(f"强度级别：{level}（分值：{score}）")
    print("-" * 50)


if __name__ == "__main__":
    main()