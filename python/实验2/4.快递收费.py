'''
Compony: NUC
Date: 2026-05-20 16:08:53
LastEditors: Loong2525
LastEditTime: 2026-05-20 16:16:40
'''
address ={"华北":1,"华东":2,"华南":3}

region = str(input("请输入地址(华北/华东/华南):"))
if region in address:
    weight = float(input("请输入重量："))
    if region == "华北":
        if weight <= 2:
            print("快递费用为：12元")
        else:
            value = (weight - 2)*2 + 12
            print("快递费用为：{:.2f}元".format(value))
    elif region == "华东":
        if weight <= 2:
            print("快递费用为：13元")
        else:
            value = (weight - 2)*3 + 13
            print("快递费用为：{:.2f}元".format(value))
    elif region == "华南":
        if weight <= 2:
            print("快递费用为：14元")
        else:
            value = (weight - 2)*3 + 14
            print("快递费用为：{:.2f}元".format(value))
else:
    print("输入的地址无效")

