from random import *

pre_cho = ""
pre_tex = ""

def chosung_test_f():
    global pre_cho, pre_tex

    cho = ['ㅅㄱ', 'ㅍㄷ', 'ㅂㄴㄴ', 'ㅋㅇ', 'ㄱ', 'ㅂ', 'ㅅㅂ']
    tex = ['사과', '포도', '바나나', '키위', '감', '배', '수박']

    if pre_cho in cho:
        if pre_cho != "":
            cho.remove(pre_cho)
            tex.remove(pre_tex)
            print("지워진 초성 리스트 :", cho)

    i = randint(0, len(cho) - 1)

    cho = cho[i]
    tex = tex[i]
    theme = 'f'

    pre_cho = cho
    pre_tex = tex
    print("이전 초성 :" , pre_cho)
    return cho, tex, theme

def chosung_test_a():
    global pre_cho, pre_tex

    cho = ['ㄱㅇㅈ','ㅈ']
    tex = ['강아지', '쥐']
    if pre_cho in cho:
        if pre_cho != "":
            cho.remove(pre_cho)
            tex.remove(pre_tex)
            print("지워진 초성 리스트 :", cho)
    i = randint(0, len(cho) - 1)

    cho = cho[i]
    tex = tex[i]
    theme = 'a'
    pre_cho = cho
    pre_tex = tex
    print("이전 초성 :" , pre_cho)
    return cho, tex, theme

def chosung_test_p():
    global pre_cho, pre_tex

    cho = ['ㅈㄷㄹ', 'ㅈㅁ', 'ㄱㄴㄹ']
    tex = ['진달래', '장미', '개나리']
    if pre_cho in cho:
        if pre_cho != "":
            cho.remove(pre_cho)
            tex.remove(pre_tex)
            print("지워진 초성 리스트 :", cho)
    i = randint(0, len(cho) - 1)

    cho = cho[i]
    tex = tex[i]
    theme = 'p'
    pre_cho = cho
    pre_tex = tex
    print("이전 초성 :" , pre_cho)
    return cho, tex, theme

# def chosung_test_v():
#     cho = ['ㅂㅅ', 'ㅈㅎㅊ', 'ㅂㅎㄱ']
#     tex = ['버스', '지하철', '비행기']
#     i = randint(0, len(cho) - 1)
#
#     cho = cho[i]
#     tex = tex[i]
#     theme = 'v'
#     return cho, tex, theme

def chosung_reset():
    cho_list = []
    tex_list = []
    handwrite_list = []
    check_list = []

    return cho_list, tex_list, handwrite_list, check_list