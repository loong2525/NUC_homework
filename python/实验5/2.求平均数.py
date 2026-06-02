'''
Compony: NUC
Date: 2026-06-02 09:33:34
LastEditors: Loong2525
LastEditTime: 2026-06-02 09:33:38
'''
def calculate_average(*data,precision=2):
    if len(data) == 0:
        return 0
    return round(sum(data) / len(data), precision)

average = calculate_average(1.235, 2.123, 3, precision=2)
print("平均数是:", average)
average = calculate_average(1.125, 2.5, 3.5, precision=3)
print("平均数是:", average)