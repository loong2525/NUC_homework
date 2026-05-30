'''
Compony: NUC
Date: 2026-05-20 16:03:08
LastEditors: Loong2525
LastEditTime: 2026-05-20 16:03:11
'''
user = "admin"
password ="admin-1234"
user_input = input("请输入用户名：")
password_input = input("请输入密码：")
if user_input == user and password_input == password:
    print("登录成功！")
else:
    print("登录失败！")
