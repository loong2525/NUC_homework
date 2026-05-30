'''
Compony: NUC
Date: 2026-05-20 09:45:33
LastEditors: Loong2525
LastEditTime: 2026-05-20 09:45:37
'''

values = [0, "0", 0.0, 0j]
for v in values:
    print(f"{repr(v)} -> 类型: {type(v).__name__}")