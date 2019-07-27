import logging
from setup_file_io import LoadCfg

# 0: up, 1: front, 2: right, 3: left, 4: back, 5: down

# 각 Plane의 default function을 저장한 list입니다.
DEF_FUNC = ["Input", "One", "Not", "Or", "And", "Output"]

# 각 Bit Cell의 absolute position에 대응하는 default place value를 저장한 list입니다.
# [[up], [front], [right], [left], [back], [down]]
DEF_BIT_PLVAL = [[1, 2, 4, 8, 16, 32, 64, 128]] *6

# 회전 기호를 모아 둔 list입니다.
one_layer_rot_list =    ["U", "D", "L", "R", "F", "B"]                          # 한 줄 회전
two_layers_rot_list =   ["u", "d", "l", "r", "f", "b"]                          # 두 줄 회전
center_layer_rot_list = ["M", "S", "E"]                                         # 가운데 줄 회전

rotate_list = one_layer_rot_list + two_layers_rot_list + center_layer_rot_list  # 회전 기호

# 명령 확장용으로, Load, Save, Clear, Execute를 특정 Plane에서만 실행할 때 각 Plane을 지칭하기 위해 만든 list입니다.
index_list = ["0", "1", "2", "3", "4", "5", "6"]                                # 6: 모든 면


class Cube:

    # Cube initialization: Cube의 initial state를 설정합니다. =========================================================================
    def __init__(self, cell_func=DEF_FUNC, cell_bit_plval=DEF_BIT_PLVAL):
        self.hyper_in  = None                                                   #
        self.hyper_out = None                                                   #

        self.cell_func      = cell_func                                         # list: 각 Plane의 역할
        self.cell_bit_plval = cell_bit_plval                                    # list: Bit Cell의 자릿값

        self.cell_data =  [0]     *6                                            # list: Data Cell의 값
        self.cell_bit  = [[0] *8] *6                                            # list: Bit Cell의 값
        self.cell_core =   0                                                    # variable: Core Cell의 값

    # Sub Function: Input, Output, Load, Save, Clear, Execute, Rotate를 수행하는 데 사용하는 function입니다. ================================

    # Bin2Dec: Bit Cell의 Binary를 Data Cell에 저장할 Demical로 바꿉니다.       ===== BIn2Dec 함수 =====
    def Bin2Dec(self, planenum):                                                # planenum: 연산을 수행할 plane의 번호
        dec = 0                                                                 # demical을 저장하여 return할 variable
        for i in range(8):                                                      # 8개의 Bit Cell에 대하여 반복 수행
            dec += self.cell_bit[planenum][i] * self.cell_bit_plval             # Bit 값과 자릿값을 곱한 값을 dec에 저장
        return dec                                                              # dec 값 반환

    # Dec2Bin: Data Cell의 Demical을 Bit Cell에 저장할 Binary로 바꿉니다.         ===== Dec2Bin 함수 =====
    def Dec2Bin(self, planenum):                                                # planenum: 연산을 수행할 plane의 번호
        raw_bin = [0, 0, 0, 0, 0, 0, 0, 0]                                      # raw_bin: 순서대로 이진수를 저장할 list
        for i in range(8):                                                      # 8개의 Bit Cell에 대하여 반복 수행
            raw_bin[i] = self.cell_data[planenum] >> i & 1                      # raw_bin list의 i번째 원소에 값 저장
        bin = self.Raw2Plval(planenum, raw_bin)                                 # 사전 설정한 자릿값 순서에 맞게 Bit 값 순서 변경
        return bin                                                              # bin list 반환

    # Raw2Plval: 2진수 list의 Bit 값이 자릿값 순서대로 정렬되어 있는 것을 설정된 대로 바꿉니다. ===== Raw2Plval 함수 =====
    def Raw2Plval(self, planenum, raw_bin):                                     # planenum: 자릿값 순서를 찾을 면, raw_bin: 순서를 바꿀 Bit 값 list
        bin = [0, 0, 0, 0, 0, 0, 0, 0]                                          # bin: 정렬된 2진수 list

        for ind, plval in enumerate(self.cell_bit_plval[planenum]):             # ind: 인덱스, plval: 자릿값
            if   plval == 1:   bin[ind] = raw_bin[0]                            # 자릿값이   1일 때
            elif plval == 2:   bin[ind] = raw_bin[1]                            # 자릿값이   2일 때
            elif plval == 4:   bin[ind] = raw_bin[2]                            # 자릿값이   4일 때
            elif plval == 8:   bin[ind] = raw_bin[3]                            # 자릿값이   8일 떄
            elif plval == 16:  bin[ind] = raw_bin[4]                            # 자릿값이  16일 때
            elif plval == 32:  bin[ind] = raw_bin[5]                            # 자릿값이  32일 때
            elif plval == 64:  bin[ind] = raw_bin[6]                            # 자릿값이  64일 때
            elif plval == 128: bin[ind] = raw_bin[7]                            # 자릿값이 128일 때

        return bin                                                              # bin list 반환

    # Plval2Raw: 2진수 list의 Bit 값이 설정된 대로 있는 것을 자릿값 순서대로 정렬합니다. ===== Plval2Raw 함수 =====
    def Plval2Raw(self, planenum, bin):                                         # planenum: 자릿값 순서를 찾을 면, bin: 순서를 바꿀 Bit 값 list
        raw_bin = [0, 0, 0, 0, 0, 0, 0, 0]                                      # raw_bin: 정렬된 2진수 list

        for ind, plval in enumerate(self.cell_bit_plval[planenum]):             # ind: 인덱스, plval: 자릿값
            if   plval == 1:   raw_bin[0] = bin[ind]                            # 자릿값이   1일 때
            elif plval == 2:   raw_bin[1] = bin[ind]                            # 자릿값이   2일 때
            elif plval == 4:   raw_bin[2] = bin[ind]                            # 자릿값이   4일 때
            elif plval == 8:   raw_bin[3] = bin[ind]                            # 자릿값이   8일 때
            elif plval == 16:  raw_bin[4] = bin[ind]                            # 자릿값이  16일 때
            elif plval == 32:  raw_bin[5] = bin[ind]                            # 자릿값이  32일 때
            elif plval == 64:  raw_bin[6] = bin[ind]                            # 자릿값이  64일 때
            elif plval == 128: raw_bin[7] = bin[ind]                            # 자릿값이 128일 때

        return raw_bin                                                          # raw_bin list 반환

    # FindPlane: 입력한 function을 가지고 있는 plane을 모두 찾아 list를 만듭니다.   ===== FindPlane 함수 =====
    def FindPlane(self, planefunc):                                             # planefunc: 찾을 plane의 function
        planenum = list()                                                       # planenum: 결과를 찾아 저장할 list
        for ind, func in enumerate(self.cell_func):                             # ind: 인덱스, func: 역할
            planenum.append(ind) if func == planefunc else pass                 # func와 planefunc가 같으면 ind를 planenum에 추가
        return planenum                                                         # planenum list 반환

    # And: Data Cell과 Bit Cell 사이에 AND 연산을 수행합니다.                     ===== And 함수 =====
    def And(self, planenum):                                                    # planenum: AND 연산을 수행할 Plane 번호
        and_val1 = self.cell_data[planenum]                                     # and_val1: AND 연산을 수행할 값 1(Data Cell)
        and_val2 = self.Bin2Dec(planenum)                                       # and_val2: AND 연산을 수행할 값 2(Bit Cell)
        and_result = and_val1 & and_val2                                        # and_result: AND 연산 수행 결과
        self.cell_data[planenum] = and_result                                   # Data Cell에 and_result 저장
        return and_result                                                       # Nand()를 위해 and_result 반환

    # Nand: Data Cell과 Bit Cell 사이에 NAND 연산을 수행합니다.                   ===== Nand 함수 =====
    def Nand(self, planenum):                                                   # planenum: NAND 연산을 수행할 Plane 번호
        nand_result = ~self.And(planenum)                                       # And()의 결과에 not 연산 수행
        self.cell_data[planenum] = nand_result                                  # Data Cell에 nand_result 저장

    # Or: Data Cell과 Bit Cell 사이에 OR 연산을 수행합니다.                       ===== Or 함수 =====
    def Or(self, planenum):                                                     # planenum: OR 연산을 수행할 Plane 번호
        or_val1 = self.cell_data[planenum]                                      # or_val1: OR 연산을 수행할 값 1(Data Cell)
        or_val2 = self.Bin2Dec(planenum)                                        # or_val2: OR 연산을 수행할 값 2(Bit Cell)
        or_result = or_val1 | or_val2                                           # or_result: OR 연산 수행 결과
        self.cell_data[planenum] = or_result                                    # Data Cell에 or_result 저장
        return or_result                                                        # Nor()를 위해 or_result 반환

    # Nor: Data Cell과 Bit Cell 사이에 NOR 연산을 수행합니다.                     ===== Nor 함수 =====
    def Nor(Self, planenum):                                                    # planenum: NOR 연산을 수행할 Plane 번호
        nor_result = ~self.Or(planenum)                                         # Or()의 결과에 not 연산 수행
        self.cell_data[planenum] = nor_result                                   # Data Cell에 nor_result 저장

    # Xor: Data Cell과 Bit Cell 사이에 XOR 연산을 수행합니다.                     ===== Xor 함수 =====
    def Xor(self, planenum):                                                    # planenum: XOR 연산을 수행할 Plane 번호
        xor_val1 = self.cell_data[planenum]                                     # xor_val1: XOR 연산을 수행할 값 1(Data Cell)
        xor_val2 = self.Bin2Dec(planenum)                                       # xor_val2: XOR 연산을 수행할 값 2(Bit Cell)
        xor_result = xor_val1 ^ xor_val2                                        # xor_result: XOR 연산 수행 결과
        self.cell_data[planenum] = xor_result                                   # Data Cell에 xor_result 저장
        return xor_result                                                       # Xnor()를 위해 xor_result 반환

    # Xnor: Data Cell과 Bit Cell 사이에 XNOR 연산을 수행합니다.                   ===== Xnor 함수 =====
    def Xnor(self, planenum):                                                   # planenum: XNOR 연산을 수행할 plane 번호
        xnor_result = ~self.Xor(planenum)                                       # Xor()의 결과에 not 연산 수행
        self.cell_data[planenum] = xnor_result                                  # Data Cell에 xnor_result 저장

    # Not: Bit Cell에서 NOT 연산을 수행합니다.                                    ===== Not 함수 =====
    def Not(self, planenum):                                                    # planenum: NOT 연산을 수행할 plane 번호
        not_val = self.Bin2Dec(planenum)                                        # not_val: NOT 연산을 수행할 값 (Bit Cell)
        not_result = ~not_val                                                   # not_result: NOT 연산 수행 결과
        self.cell_data[planenum] = not_result                                   # Data Cell에 not_result 저장

    # StaticOne: Static One Plane의 Data Cell의 값을 1로 고정합니다.              ===== StaticOne 함수 =====
    def StaticOne(self):
        planenum = self.FindPlane("One")                                        # 역할이 One인 plane 찾기
        for num in planenum:                                                    # plane list의 모든 원소에 대해 반복
            self.cell_data[num] = 1                                             # 해당 plane의 Data Cell의 값을 1로 설정

    # Shift: 입력한 plane의 모든 Bit Cell의 값을 한 번 Shift합니다.                ===== Shift 함수 =====
    def Shift(self, planenum):                                                  # planenum: Shift를 수행할 plane 번호
        bin = self.cell_bit[planenum]                                           # bin: 해당 plane의 Bit Cell의 Bit 값을 저장한 list
        raw_bin = Plval2Raw(planenum, bin)                                      # bin의 Bit 값을 자릿값 순서대로 정렬
        for i in range(7):                                                      # 0부터 6까지 7번 반복
            self.raw_bin[7-i] = self.raw_bin[6-i]                               # i번쨰 값을 i+1로 이동
        self.raw_bin[0] = 0                                                     # 첫 번째 값을 0으로 설정
        bin = Raw2Plval(planenum, raw_bin)                                      # raw_bin의 Bit 값을 해당 면의 자릿값 순서대로 정렬
        self.cell_bit[planenum] = bin                                           # 해당 plane의 Bit Cell의 Bit 값에 shift한 Bit 값 저장

    # Main Function: Input, Output, Load, Save, Clear, Execute, Rotate를 수행하는 function입니다. ======================================

    # Input: Input Plane에서 값을 받아옵니다.                                     ===== Input 함수 =====
    def Input(self, input_value):                                               # input_value: 입력받은 값
        planenum = self.FindPlane("Input")                                      # planenum: 모든 Input Cell의 번호를 담은 list
        if len(planenum) == 0:                                                  # Input Plane이 없을 때:
            logging.error("Couldn't find Input Plane")                          #   error 처리 (logging)
            return None                                                         #   Input 함수 종료
        for num in planenum:                                                    # planenum의 모든 값에 대해 반복
            self.cell_data[num] = input_value                                   # Data Cell에 입력 받은 값 저장

    # Output: Output Plane의 값을 출력합니다.                                     ===== Output 함수 =====
    def Output(self):
        planenum = self.FindPlane("Output")                                     # planenum: 모든 Output Cell의 번호를 담은 list
        if len(planenum) == 0:                                                  # Output Plane이 없을 때:
            logging.error("Couldn't find Output Plane")                         #   error 처리 (logging)
            return None                                                         #   Output 함수 종료
        elif len(planenum) > 1:                                                 # Output Plane이 여러 개일 떄:
            logging.error("Nonsense cube; more than one output cell")           #   error 처리 (logging)
            return None                                                         #   Output 함수 종료
        return self.cell_data[planenum[0]]                                      # Data Cell의 값 반환

    # Load: Data Cell의 값을 Bit Cell에 저장합니다.                               ===== Load 함수 =====
    def Load(self, plane = -1):
        if plane == -1:                                                         # 대상 Plane 번호가 -1일 때:
            for planenum in range(6):                                           #   모든 면에 대해 Load 실행
                raw_bin = self.Dec2Bin(planenum)                                #   planenum 번째 Plane의 Bit Cell
                bin = self.Raw2Plval(planenum, raw_bin)                         #   Bit Cell의 값을 자릿값 설정에 맞게 순서 바꾸기
                for bitnum in range(8):                                         #   planenum 번째 Plane의 bitnum 번째 Bit Cell에
                    self.cell_bit[planenum][bitnum] = bin[bitnum]               #   bitnum 번째 인덱스의 bin의 값 대입

        elif (plane > 5) | (plane < -1):                                        # 대상 Plane 번호가 범위 밖일 때:
            logging.error("Plane Number Should be -1, 0, 1, ..., or 5")         #   error 처리 (logging)
            return None                                                         #   Load 함수 종료

        else:                                                                   # 대상 Plane 번호가 0-5일 때:
            raw_bin = self.Dec2Bin(plane)                                       #   plane 번째 Plane의 Bit Cell
            bin = self.Raw2Plval(plane, raw_bin)                                #   Bit Cell의 값을 자릿값 설정에 맞게 순서 바꾸기
            for bitnum in range(8):                                             #   plane 번째 Plane의 bitnum 번째 Bit Cell에
                self.cell_bit[plane][bitnum] = bin[bitnum]                      #   bitnum 번째 인덱스의 bin의 값 대입

    # Save: Bit Cell의 값을 Data Cell에 저장합니다.                               ===== Save 함수 =====
    def Save(self, plane = -1):
        if plane == -1:                                                         # 대상 Plane 번호가 -1일 때:
            for planenum in range(6):                                           #   모든 Plane에 대해 Save 실행
                self.cell_data[planenum] = self.Bit2Dec(planenum)               #   planenum 번째 Plane에서 Save

        elif (plane > 5) | (plane < -1):                                        # 대상 Plane 번호가 범위 밖일 때:
            logging.error("Plane Number Should be -1, 0, 1, ..., or 5")         #   error 처리 (logging)
            return None                                                         #   Save 함수 종료

        else:                                                                   # 대상 Plane 번호가 0-5일 때:
            self.cell_data[plane] = self.Bit2Dec(plane)                         #   plane 번째 Plane에서 Save

    # Clear: Plane의 Bit Cell과 Data Cell의 값을 초기 상태로 되돌립니다.           ===== Clear 함수 =====
    def Clear(self, plane = -1):
        if plane == -1:                                                         # 대상 plane 번호가 -1일 떄:
            self.cell_data =  [0]     *6                                        #   모든 Plane의 Data Cell 초기화
            self.cell_bit  = [[0] *8] *6                                        #   모든 Plane의 Bit Cell 초기화
            self.cell_core =   0                                                #   Core Cell 초기화
            self.StaticOne()                                                    #   Static One 셀 1로 초기화

        elif (plane > 5) | (plane < -1):                                        # 대상 Plane 번호가 범위 밖일 때:
            logging.error("Plane Number Should be -1, 0, 1, ..., or 5")         #   error 처리 (logging)
            return None                                                         #   Clear 함수 종료

        else:                                                                   # 대상 Plane 번호가 0-5일 때:
            self.cell_data[plane] = 0                                           #   Data Cell 초기화
            self.cell_bit[plane] = [0] *8                                       #   Bit Cell 초기화
            if self.cell_func[plane] = "One":                                   # 대상 Plane이 Static One Cell일 때:
                self.cell_data[plane] = 1                                       #   Data Cell을 1로 초기화

    # Execute: 비트 연산과 Shift 연산을 수행합니다.                                ===== Execute 험수 =====
    def Execute(self, plane = -1):
        if plane == -1:                                                         # 대상 Plane 번호가 -1일 떄:
            and_plane   = self.FindPlane("And")                                 #   And   Plane의 번호 찾기
            nand_plane  = self.FindPlane("Nand")                                #   Nand  Plane의 번호 찾기
            or_plane    = self.FindPlane("Or")                                  #   Or    Plane의 번호 찾기
            nor_plane   = self.FindPlane("Nor")                                 #   Nor   Plane의 번호 찾기
            xor_plane   = self.FindPlane("Xor")                                 #   Xor   Plane의 번호 찾기
            xnor_plane  = self.FindPlane("Xnor")                                #   Xnor  Plane의 번호 찾기
            not_plane   = self.FindPlane("Not")                                 #   Not   Plane의 번호 찾기
            shift_plane = self.FindPlane("Shift")                               #   Shift Plane의 번호 찾기

            for planenum in and_plane: self.And(planenum)                       #   AND  연산 실행
            for planenum in nand_plane: self.Nand(planenum)                     #   NAND 연산 실행
            for planenum in or_plane: self.Or(planenum)                         #   OR   연산 실행
            for planenum in nor_plane: self.Nor(planenum)                       #   NOR  연산 실행
            for planenum in xor_plane: self.Xor(planenum)                       #   XOR  연산 실행
            for planenum in xnor_plane: self.Xnor(planenum)                     #   XNOR 연산 실행
            for planenum in not_plane: self.Not(planenum)                       #   NOT  연산 실행
            for planenum in shift_plane: self.Shift(planenum)                   #   Shift     실행

        elif (plane > 5) | (plane < -1):                                        # 대상 Plane 번호가 범위 밖일 때:
            logging.error("Plane Number Should be -1, 0, 1, ..., or 5")         #   error 처리 (logging)
            return None                                                         #   Execute 함수 종료

        else:                                                                   # 대상 Plane 번호가 0-5일 때:
            if self.cell_function[plane] in ["Input", "Output", "Inout", "One"]:#   plane의 역할이 Input/Output/Inout/Static One일 떄:
                pass                                                            #   실행 안 함
            elif self.cell_function[plane] == "And": self.And(plane)            #   AND  연산 실행
            elif self.cell_function[plane] == "Nand": self.Nand(plane)          #   NAND 연산 실행
            elif self.cell_function[plane] == "Or": self.Or(plane)              #   Or   연산 실행
            elif self.cell_function[plane] == "Nor": self.Nor(plane)            #   NOR  연산 실행
            elif self.cell_function[plane] == "Xor": self.Xor(plane)            #   XOR  연산 실행
            elif self.cell_function[plane] == "Xnor": self.Xnor(plane)          #   XNOR 연산 실행
            elif self.cell_function[plane] == "Not": self.Not(plane)            #   NOT  연산 실행
            elif self.cell_function[plane] == "Shift": self.Shift(plane)        #   Shift     실행

    # Rotate: 입력 받은 회전 기호에 따라 큐브의 층을 회전시킵니다.                  ===== Rotate 함수 =====
    def Rotate(self, rotation):                                                 # rotation: 회전 기호
        pass


class Cubes:

    def __init__(self, c_debug = 0, c_ascii = 0, c_cube = False, c_step = 0):

        self.cubes = list()                                                     # 큐브 리스트

        self.c_debug = c_debug
        self.c_ascii = c_ascii
        self.c_step = c_step

        cell_function, cell_bit_place_value = LoadCfg()                         # 사전 설정값 받아오기
        self.cube = Cube(cell_function, cell_bit_place_value)                   # 큐브 생성하기
        self.cubes.append(self.cube)                                            # 리스트에 큐브 추가하기
