'''
Compony: NUC
Date: 2026-05-30 09:36:02
LastEditors: Loong2525
LastEditTime: 2026-05-30 09:40:44
'''

def filter_bad_words(text):
    bad_words = ["最优秀"]
    for word in bad_words:
        if text.find(word) != -1:
            text = text.replace(word, "较优秀")
    return text 

if __name__ == "__main__":
    input_text = "我们拥有最优秀且具有远见卓识的设计师，使我们的策略分析严谨，设计充满创意。我们有信心为您缔造最优秀的品牌形象设计服务，将您的企业包装得更富价值。"
    output_text = filter_bad_words(input_text)
    print(output_text)