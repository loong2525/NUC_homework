'''
Compony: NUC
Date: 2026-05-20 10:01:30
LastEditors: Loong2525
LastEditTime: 2026-05-20 10:01:33
'''
#体质指数（BMI）= 体重（kg）÷（身高×身高）（m）
weight = float(input("请输入体重（单位：kg）："))
height = float(input("请输入身高（单位：m）："))
bmi = weight / (height * height)
print("您的BMI指数为：{bmi:.2f}".format(bmi=bmi))