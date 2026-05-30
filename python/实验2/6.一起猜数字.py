'''
Compony: NUC
Date: 2026-05-21 12:45:34
LastEditors: Loong2525
LastEditTime: 2026-05-21 14:41:25
'''
goal=int(input("请设置目标数字："))
if goal<0 or goal>100:
    print("请输入0-100之间的数字！")
else:
    print("请开始猜数字：")
    i=5
    while i!=0:
        value=int(input())
        if value>goal:
            print("很遗憾，你猜大了")
        elif value<goal:
            print("很遗憾，你猜小了")
        else:
            print("恭喜你，猜对了！")
            break
        i-=1
    if i==0:
        print("很遗憾，五次机会已用完，正确答案是：",goal)
