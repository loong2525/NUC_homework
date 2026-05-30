'''
Compony: NUC
Date: 2026-05-30 10:05:10
LastEditors: Loong2525
LastEditTime: 2026-05-30 10:08:03
'''

recyclable = ("废纸", "塑料瓶", "塑料桶", "易拉罐", "金属元件", "玻璃瓶", 
              "废旧衣物", "废弃家具", "旧数码产品", "旧家电")
kitchen = ("食材废料", "菜帮菜叶", "剩菜", "剩饭", "蔬菜水果", "瓜果皮核", 
           "蛋壳", "鸡骨", "鱼骨", "过期食品")
harmful = ("废电池", "废灯管", "消毒棉棒", "废油漆", "废杀虫剂")
other = ("砖瓦灰土", "餐巾纸", "保鲜膜")


# 考察内容2：访问元组元素
print("可回收垃圾示例（前三个）:", recyclable[:3])   # 切片
print("有害垃圾第一个:", harmful[0])                # 索引

def classify_garbage(garbage_name):
    """
    根据垃圾名称返回其类别
    """
    # 使用in运算符判断是否在元组中
    if garbage_name in recyclable:
        return "可回收垃圾"
    elif garbage_name in kitchen:
        return "厨余垃圾"
    elif garbage_name in harmful:
        return "有害垃圾"
    elif garbage_name in other:
        return "其他垃圾"
    else:
        return "未知垃圾"

# 小明聚餐后的垃圾
garbage_list = ["废纸", "塑料瓶", "食材废料", "餐巾纸", "旧家电", "废电池"]

print("\n垃圾分类结果：")
for g in garbage_list:
    category = classify_garbage(g)
    print(f"{g} -> {category}")