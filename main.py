import argparse
import sys
import logging
import numpy as np
from cube import *

def Judge_bool(b):
    if b.lower() in ["true", "t", "1"]: return True
    elif b.lower() in ["false", "f", "0"]:return False
    else:raise argparse.ArgumentTypeError("Not Boolean value; 참/거짓 형태가 아닙니다.")
#본 자료형이 불리안형이 아닐 때에는 에러를 반환한다.
#리스트 내의 원소가 존재하면 잘 알아듣고 그에 따른 참이나 거짓을 반환

#인자에 따라서 어떠한 실행을 할지 결정해준다. 
parser = argparse.ArgumentParser()

parser.add_argument("-dl","--debug-level", type=int, choices=[0,1,2], default=1,
        help = "Debug: Change Debug Message Level, 0=Off, 1=Basic, 2=Commands \n 디버그: 디버그 메시지의 레벨을 바꿉니다 0=끔(간단출력), 1=일반, 2=커맨드 나열")
parser.add_argument("-dc","--debug-cube", type=Judge_bool, default=False,
        help = "Debug: Show cube at every step True to enable \n 디버그: 매 모습을 큐브의 전개도 형식으로 나타냅니다." )
parser.add_argument("-ds","--debug-step", type=Judge_bool, default=False,
        help = "Debug: Pause at every step. True to enable \n 매 모습을 코드 하나하나로 나타냅니다.")
parser.add_argument("-s","--script", type=str, default = "",
        help = "Input script's directory. If this is Null, you can input your code \n 코드를 입력합니다. 만약 파일명 뒤가 빈 채라면 직접 입력받습니다.")
parser.add_argument("-a","--ascii", type=Judge_bool, default=True,
        help = "Set true to Print as ascii. False to print at number \n False로 설정할 시 출력이 아스키코드 형태로 나옵니다.")
parser.add_argument("-g","--gui", type=Judge_bool, default=False,
        help = "Set true to show as 3d gui. \n True로 설정하면 3d gui 환경으로 확인할 수 있습니다. ")

args = parser.parse_args() #파서의 변수 지정

c_list = []

if args.debug_level == 0:
    logging.basicConfig(level=logging.WARNING, \
        format='[%(asctime)s]%(message)s',\
        datefmt='%Y-%m-%d %H:%M:%S')
else:
    logging.basicConfig(level=logging.INFO, \
        format='[%(asctime)s] %(message)s',\
        datefmt='%Y-%m-%d %H:%M:%S', \
        stream=sys.stdout)


def Re_input():
    global str_input
    if str_input == '':
        logging.warning("Input your script")
        str_input = input()
        Re_input()
        #빈 입력을 받으면 계속해서 되물음(재귀함수)
        

if __name__ == "__main__":
    str_input = ""
    if args.script != "":
        logging.info("Reading From File: %s"%args.script)
        f = open(args.script, 'r')
        str_input = f.read()
        f.close()
    else:
        logging.warning("Input your script")
        str_input = input()
        Re_input()


    logging.info("Script Loaded with Length %d"%len(str_input))
    logging.info(str_input)
    
    c = Cubes(args.debug_level, args.ascii, args.debug_cube, args.debug_step)
    logging.info("*"*50)
    logging.info("%30s"%"Result")
    logging.warning("*"*50)
    print(c.execute(str_input))
