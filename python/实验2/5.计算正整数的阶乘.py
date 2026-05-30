'''
Compony: NUC
Date: 2026-05-21 12:41:50
LastEditors: Loong2525
LastEditTime: 2026-05-21 12:42:05
'''
value=int(input("请输入一个整数："))
y=1
while value!=0:
    y=value*y
    value-=1
print("阶乘的结果是：",y)