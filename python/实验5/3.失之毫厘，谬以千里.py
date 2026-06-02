'''
Compony: NUC
Date: 2026-06-02 09:40:04
LastEditors: Loong2525
LastEditTime: 2026-06-02 09:43:10
'''
def calculate_power(base, exponent):
    return base ** exponent

print("输入两个数及其幂次，用逗号分隔:")
input_str = input()
a,b, exponent = map(float, input_str.split(','))
result = abs(calculate_power(a, exponent)-calculate_power(b, exponent))
print(f"{a}的{exponent}次幂减去{b}的{exponent}次幂的结果是: {result}")