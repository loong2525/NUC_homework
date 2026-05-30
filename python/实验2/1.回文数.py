'''
Compony: NUC
Date: 2026-05-20 11:33:38
LastEditors: Loong2525
LastEditTime: 2026-05-20 16:00:36
'''
#获取用户输入的四位整数；获取原来四位数的各位数字；组合新四位数，与原来的四位数比较是否相等。
print("输入一个四位数：")
value = int(input())
if value//1000 == value%10 and (value//100)%10 == (value%100)//10:
    print("是回文数")
else:
    print("不是回文数")
