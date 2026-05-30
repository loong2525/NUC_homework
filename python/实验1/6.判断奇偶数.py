'''
Compony: NUC
Date: 2026-05-20 10:03:53
LastEditors: Loong2525
LastEditTime: 2026-05-20 10:04:56
'''
#通过位运算判断奇数偶数
number = int(input("请输入一个整数："))
if number & 1 == 0:
    print(f"{number}是偶数")
else:
    print(f"{number}是奇数")