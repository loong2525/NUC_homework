'''
Compony: NUC
Date: 2026-06-02 09:10:50
LastEditors: Loong2525
LastEditTime: 2026-06-02 10:24:28
'''
def find_missing_number(nums):  
    list1=[0,0,0,0,0,0,0,0,0,0]
    list2=[]
    for i in nums:
        list1[i-1]=1
    for _ in range(len(list1)):
        if list1[_] == 0:
            list2.append(_ + 1)
    return list2


nums = (6,7,9,10)
missing_number = find_missing_number(nums)
print("缺失的数字是:", missing_number)
            
            