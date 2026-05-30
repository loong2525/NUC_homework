'''
Compony: NUC
Date: 2026-05-20 16:05:25
LastEditors: Loong2525
LastEditTime: 2026-05-20 16:08:04
'''
value = float(input("请输入绩效成绩："))
if value >= 90 and value <= 100:
    print("绩效等级为：A")
elif value >= 80 and value < 90:
    print("绩效等级为：B")
elif value >= 70 and value < 80:
    print("绩效等级为：C")
elif value >= 60 and value < 70:
    print("绩效等级为：D")
else:
    print("输入的绩效成绩无效")