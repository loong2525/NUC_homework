'''
Compony: NUC
Date: 2026-05-20 09:54:13
LastEditors: Loong2525
LastEditTime: 2026-05-20 09:58:39
'''
speed = float(input("请输入速度（单位：km/h）："))
print("速度是{speed:.2f}".format(speed=speed))
if speed-120 > 120*0.1:
    print("已超速,会受到罚款")
elif speed-120 < 120*0.1 and speed-120 > 0:
    print("已超速,但不会受到罚款")
else:
    print("您没有超速")