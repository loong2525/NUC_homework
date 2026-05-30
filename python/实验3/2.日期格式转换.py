'''
Compony: NUC
Date: 2026-05-30 09:31:40
LastEditors: Loong2525
LastEditTime: 2026-05-30 09:34:54
'''

def convert_date(date_str):
    # 根据内容判断分隔符类型并分割

    if '年' in date_str:
        # 中文格式：2022年2月4日
        parts = date_str.split('年')
        year = parts[0]
        rest = parts[1]                    # 剩余部分如 "2月4日"
        month = rest.split('月')[0]
        day = rest.split('月')[1].split('日')[0]

    elif '-' in date_str:
        # 连字符格式：2022-2-4
        parts = date_str.split('-')
        year, month, day = parts
    elif '/' in date_str:
        # 斜杠格式：2022/2/4
        parts = date_str.split('/')
        year, month, day = parts
    elif '.' in date_str:
        # 点格式：2022.2.4
        parts = date_str.split('.')
        year, month, day = parts
    else:
        return "错误：无法识别的日期格式"

    year = str(int(year))
    month = str(int(month))
    day = str(int(day))

    return "".join([year, "年", month, "月", day, "日"])


def main():
    # 测试各种格式的日期
    test_dates = input("输入日期：")

    result = convert_date(test_dates)
    print("日期格式转换结果：")

    print(f"{test_dates:20} -> {result}")

if __name__ == "__main__":
    main()