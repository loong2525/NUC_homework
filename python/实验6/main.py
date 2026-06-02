'''
Compony: NUC
Date: 2026-06-02 09:45:48
LastEditors: Loong2525
LastEditTime: 2026-06-02 10:27:15
'''

'''
	 所有的考题存储在“试卷.txt”文件中。
	 程序加载完“试卷.txt”文件后，每次只会显示一道题，只有当考生作答后，才会显示下一题，直到答完所有的题目为止。
	 考题答案存储在“答案.txt”文件中。
	 程序自动评卷后，会将考试结果以“结果.txt”文件的形式反馈给考生。
'''

import os

class EXAM:
    def __init__(self, questions_file="试卷.txt", answers_file="答案.txt", results_file="结果.txt"):
        self.questions_file = questions_file
        self.answers_file = answers_file
        self.results_file = results_file
        self.questions = []
        self.answers = []
        self.ask_info = []

    def test_paper(self):
        # 读取试卷
        with open(self.questions_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.questions = content.strip().split('\n\n')   # 每道题是一个字符串

        # 读取标准答案
        with open(self.answers_file, 'r', encoding='utf-8') as f:
            self.answers = [line.strip() for line in f.readlines()]

        # 考生信息
        name = input("请输入你的姓名：")
        stu_id = input("请输入你的学号：")
        self.ask_info = {
            'name': name,
            'stu_id': stu_id,
            'user_answers': []   # 存储每道题的答案
        }

    # 逐题显示并记录答案
        for idx, q in enumerate(self.questions):
            print(f"\n第{idx+1}题：")
            print(q.strip())
            while True:
                ans = input("你的答案（A/B/C/D）：").strip().upper()
                if ans in ['A','B','C','D']:
                    self.ask_info['user_answers'].append(ans)
                    break
                else:
                    print("输入无效，请重新输入 A、B、C 或 D")

    def answer_info(self):
        user_ans = self.ask_info['user_answers']
        correct = 0
        wrong_list = []
        for i, (u, std) in enumerate(zip(user_ans, self.answers)):
            if u == std:
                correct += 1
            else:
                wrong_list.append(i+1)   # 题号从1开始

        wrong_count = len(wrong_list)
        # 准备输出内容
        result = f"""
        姓名：{self.ask_info['name']}
        学号：{self.ask_info['stu_id']}
        提交答案：{' '.join(user_ans)}
        正确个数：{correct}
        错误个数：{wrong_count}
        错题序号：{' '.join(map(str, wrong_list)) if wrong_list else '无'}
        """
        # 写入文件
        with open(self.results_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print("\n考试结束，结果已保存到 结果.txt")
        print(result)

if __name__ == "__main__":
    exam = EXAM("D:/Desktop/NUC/NUC_homework/python/实验6/试卷.txt", "D:/Desktop/NUC/NUC_homework/python/实验6/答案.txt", "D:/Desktop/NUC/NUC_homework/python/实验6/结果.txt")
    exam.test_paper()
    exam.answer_info()  
    



