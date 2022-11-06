from playsound import playsound

"""
0. “마스크와 안경을 착용중이라면, 없는 상태에서 시도해주세요”
1. “카메라를 응시하고, 자막이나 음성 안내에 따라 행동해주세요”
2.  “먼저 왼손을 3초간 들어주세요”
3.  “오른손을 3초간 들어주세요”
4.  “양 손을 3초간 들어주세요”
5.  “카메라를 응시하고, 양쪽 눈을 다섯 번 깜빡여 주세요”
6.  “화면에 보이는 숫자를 크게 읽해주세요” - 랜덤 숫자 1~100중 하나 x 3회
7.  “화면에 보이는 문장을 크게 읽어주세요” - 랜덤 문장 10개중 하나 x 1회
8.  성공 사운드
9.  실패 사운드
"""

folder = 'sounds/'
soundtype = '.mp3'
soundtrack = ['show_face', 'introduce_first',  'left_hand', 'right_hand', 'both_hand', 'eye_blink', 'read_number',
              'read_sentence', 'success', 'fail']

def play(select):
    if select == 2:
        playsound(folder + soundtrack[select] + soundtype)
    elif select == -2:
        playsound(folder + soundtrack[-2] + soundtype)
    else:
        playsound(folder + soundtrack[-2] + soundtype)
        playsound(folder + soundtrack[select] + soundtype)


