'''
Compony: NUC
Date: 2026-05-30 09:41:27
LastEditors: Loong2525
LastEditTime: 2026-05-30 09:50:29
'''
count=str(input('请输入考勤记录：'))
count=count.upper()

if count.count('P')==22:
    print('考勤记录正常,奖励200元')
elif count.count('A')>2:
    print('处罚500元')
elif count.count('A')==2 and count.count('L')<=2:
    print('处罚200元')
elif count.count('A')==1 and count.count('L')<=2:
    print('处罚100元')
elif count.count('A')==0 and count.count('L')<=2:
    print('没有处罚')
