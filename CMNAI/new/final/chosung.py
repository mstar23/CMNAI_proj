from random import *

# def chosung_test():
#     cho = ['ㅅㄱ', 'ㅍㄷ', 'ㅂㄴㄴ', 'ㅋㅇ', 'ㄱ', 'ㅂ', 'ㅅㅂ']
#     tex = ['사과', '포도', '바나나', '키위', '감', '배', '수박']
#     i = randint(0, len(cho) - 1)
#
#     cho = cho[i]
#     tex = tex[i]
#     return cho, tex

def chosung_test_f():
    cho = ['ㅅㄱ', 'ㅍㄷ', 'ㅂㄴㄴ', 'ㅋㅇ', 'ㄱ', 'ㅂ', 'ㅅㅂ']
    tex = ['사과', '포도', '바나나', '키위', '감', '배', '수박']
    i = randint(0, len(cho) - 1)

    cho = cho[i]
    tex = tex[i]
    theme = 'f'
    return cho, tex, theme

def chosung_test_a():
    cho = ['ㄱㅇㅈ', 'ㄱㅇㅇ', 'ㅈ']
    tex = ['강아지', '고양이', '쥐']
    i = randint(0, len(cho) - 1)

    cho = cho[i]
    tex = tex[i]
    theme = 'a'
    return cho, tex, theme

def chosung_test_p():
    cho = ['ㅈㄷㄹ', 'ㅈㅁ', 'ㄱㄴㄹ']
    tex = ['진달래', '장미', '개나리']
    i = randint(0, len(cho) - 1)

    cho = cho[i]
    tex = tex[i]
    theme = 'p'
    return cho, tex, theme

def chosung_test_v():
    cho = ['ㅂㅅ', 'ㅈㅎㅊ', 'ㅂㅎㄱ']
    tex = ['버스', '지하철', '비행기']
    i = randint(0, len(cho) - 1)

    cho = cho[i]
    tex = tex[i]
    theme = 'v'
    return cho, tex, theme

def chosung_reset():
    cho_list = []
    tex_list = []
    handwrite_list = []
    check_list = []

    return cho_list, tex_list, handwrite_list, check_list