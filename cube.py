import logging
from setup_file_io import LoadCfg

# 0: up, 1: front, 2: right, 3: left, 4: back, 5: down

# 각 Plane의 default function을 저장한 list입니다.
DEF_FUNC = ["Input", "One", "Not", "Or", "And", "Output"]

# 각 Bit Cell의 absolute position에 대응하는 default place value를 저장한 list입니다.
# [[up], [front], [right], [left], [back], [down]]
DEF_BIT_PLVAL = [[1, 2, 4, 8, 16, 32, 64, 128]] *6

# 회전 기호를 모아 둔 list입니다.
one_layer_rot_list =    ['U', 'F', 'R', 'L', 'B', 'D']                          # 한 줄 회전
two_layers_rot_list =   ['u', 'f', 'r', 'l', 'b', 'd']                          # 두 줄 회전
center_layer_rot_list = ['M', 'S', 'E']                                         # 가운데 줄 회전

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

    # Bin2Dec: Bit Cell의 Binary를 Data Cell에 저장할 Demical로 바꿉니다.       ===== Bin2Dec 함수 =====
    def Bin2Dec(self, planenum):                                                # planenum: 연산을 수행할 plane의 번호
        dec = 0                                                                 # demical을 저장하여 return할 variable
        for i in range(8):                                                      # 8개의 Bit Cell에 대하여 반복 수행
            dec += (self.cell_bit[planenum][i] * self.cell_bit_plval[planenum][i]) # Bit 값과 자릿값을 곱한 값을 dec에 저장
        return dec                                                              # dec 값 반환

    # Dec2Bin: Data Cell의 Demical을 Bit Cell에 저장할 Binary로 바꿉니다.         ===== Dec2Bin 함수 =====
    def Dec2Bin(self, planenum):                                                # planenum: 연산을 수행할 plane의 번호
        raw_bin = [0, 0, 0, 0, 0, 0, 0, 0]                                      # raw_bin: 순서대로 이진수를 저장할 list
        for i in range(8):                                                      # 8개의 Bit Cell에 대하여 반복 수행
            raw_bin[i] = self.cell_data[planenum] >> i & 1                      # raw_bin list의 i번째 원소에 값 저장
        binary = self.Raw2Plval(planenum, raw_bin)                                 # 사전 설정한 자릿값 순서에 맞게 Bit 값 순서 변경
        return binary                                                              # binary list 반환

    # Raw2Plval: 2진수 list의 Bit 값이 자릿값 순서대로 정렬되어 있는 것을 설정된 대로 바꿉니다. ===== Raw2Plval 함수 =====
    def Raw2Plval(self, planenum, raw_bin):                                     # planenum: 자릿값 순서를 찾을 면, raw_bin: 순서를 바꿀 Bit 값 list
        binary = [0, 0, 0, 0, 0, 0, 0, 0]                                          # binary: 정렬된 2진수 list

        for ind, plval in enumerate(self.cell_bit_plval[planenum]):             # ind: 인덱스, plval: 자릿값
            if   plval == 1:   binary[ind] = raw_bin[0]                            # 자릿값이   1일 때
            elif plval == 2:   binary[ind] = raw_bin[1]                            # 자릿값이   2일 때
            elif plval == 4:   binary[ind] = raw_bin[2]                            # 자릿값이   4일 때
            elif plval == 8:   binary[ind] = raw_bin[3]                            # 자릿값이   8일 떄
            elif plval == 16:  binary[ind] = raw_bin[4]                            # 자릿값이  16일 때
            elif plval == 32:  binary[ind] = raw_bin[5]                            # 자릿값이  32일 때
            elif plval == 64:  binary[ind] = raw_bin[6]                            # 자릿값이  64일 때
            elif plval == 128: binary[ind] = raw_bin[7]                            # 자릿값이 128일 때

        return binary                                                              # binary list 반환

    # Plval2Raw: 2진수 list의 Bit 값이 설정된 대로 있는 것을 자릿값 순서대로 정렬합니다. ===== Plval2Raw 함수 =====
    def Plval2Raw(self, planenum, binary):                                         # planenum: 자릿값 순서를 찾을 면, binary: 순서를 바꿀 Bit 값 list
        raw_bin = [0, 0, 0, 0, 0, 0, 0, 0]                                      # raw_bin: 정렬된 2진수 list

        for ind, plval in enumerate(self.cell_bit_plval[planenum]):             # ind: 인덱스, plval: 자릿값
            if   plval == 1:   raw_bin[0] = binary[ind]                            # 자릿값이   1일 때
            elif plval == 2:   raw_bin[1] = binary[ind]                            # 자릿값이   2일 때
            elif plval == 4:   raw_bin[2] = binary[ind]                            # 자릿값이   4일 때
            elif plval == 8:   raw_bin[3] = binary[ind]                            # 자릿값이   8일 때
            elif plval == 16:  raw_bin[4] = binary[ind]                            # 자릿값이  16일 때
            elif plval == 32:  raw_bin[5] = binary[ind]                            # 자릿값이  32일 때
            elif plval == 64:  raw_bin[6] = binary[ind]                            # 자릿값이  64일 때
            elif plval == 128: raw_bin[7] = binary[ind]                            # 자릿값이 128일 때

        return raw_bin                                                          # raw_bin list 반환

    # FindPlane: 입력한 function을 가지고 있는 plane을 모두 찾아 list를 만듭니다.   ===== FindPlane 함수 =====
    def FindPlane(self, planefunc):                                             # planefunc: 찾을 plane의 function
        planenum = list()                                                       # planenum: 결과를 찾아 저장할 list
        for ind, func in enumerate(self.cell_func):                             # ind: 인덱스, func: 역할
            if func == planefunc:
                planenum.append(ind)                                            # func와 planefunc가 같으면 ind를 planenum에 추가
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
        binary = self.cell_bit[planenum]                                           # binary: 해당 plane의 Bit Cell의 Bit 값을 저장한 list
        raw_bin = Plval2Raw(planenum, binary)                                      # binary의 Bit 값을 자릿값 순서대로 정렬
        for i in range(7):                                                      # 0부터 6까지 7번 반복
            self.raw_bin[7-i] = self.raw_bin[6-i]                               # i번쨰 값을 i+1로 이동
        self.raw_bin[0] = 0                                                     # 첫 번째 값을 0으로 설정
        binary = Raw2Plval(planenum, raw_bin)                                      # raw_bin의 Bit 값을 해당 면의 자릿값 순서대로 정렬
        self.cell_bit[planenum] = binary                                           # 해당 plane의 Bit Cell의 Bit 값에 shift한 Bit 값 저장

    # RotPlane: 입력한 Plane을 회전시킵니다.                                      ===== RotPlane 함수 =====
    def RotPlane(self, plane, direction):                                       # plane: 회전할 면, direction: 시계/반시계 방향

        if direction == 0:                                                      # direction이 0일 때: 시계 방향으로 회전
            temp_edge   = self.cell_bit[plane][7]                               # temp_edge: 자리 바꿀 때 임시 저장 (엣지 조각)
            temp_corner = self.cell_bit[plane][6]                               # temp_corner: 자리 바꿀 때 임시 저장 (코너 조각)
            for bit in [7, 6, 5, 4, 3, 2]:
                self.cell_bit[plane][bit] = self.cell_bit[plane][bit - 2]
            self.cell_bit[plane][1] = temp_edge
            self.cell_bit[plane][0] = temp_corner

        else: # direction == 1                                                  # direction이 1일 때: 반시계 방향으로 회전
            temp_corner = self.cell_bit[plane][0]                                   # temp_corner: 자리 바꿀 때 임시 저장 (코너 조각)
            temp_edge   = self.cell_bit[plane][1]                                   # temp_edge: 자리 바꿀 때 임시 저장 (엣지 조각)
            for bit in [0, 1, 2, 3, 4, 5]:
                self.cell_bit[plane][bit] = self.cell_bit[plane][bit + 2]
            self.cell_bit[plane][7] = temp_edge

    # RotLine: 입력한 plane 주위의 layer를 회전시킵니다.                           ===== RotLine 함수 =====
    def RotLine(self, plane, direction):                                        # plane: 회전할 면, direction: 시계/반시계 방향

        if   plane == 0: planes = [4, 2, 1, 3]; bits = [[0, 7, 6]] *4           # U Plane 주변 Plane과 Bit Cell 번호
        elif plane == 1: planes = [0, 2, 5, 3]; bits = [[4, 3, 2], [6, 5, 4], [0, 7, 6], [2, 1, 0]] # F Plane 주변 Plane과 Bit Cell 번호
        elif plane == 2: planes = [0, 4, 5, 1]; bits = [[2, 1, 0], [6, 5, 4], [2, 1, 0], [2, 1, 0]] # R Plane 주변 Plane과 Bit Cell 번호
        elif plane == 3: planes = [0, 1, 5, 4]; bits = [[6, 5, 4], [6, 5, 4], [6, 5, 4], [2, 1, 0]] # L Plane 주변 Plane과 Bit Cell 번호
        elif plane == 4: planes = [0, 3, 5, 2]; bits = [[0, 7, 6], [6, 5, 4], [4, 3, 2], [2, 1, 0]] # B Plane 주변 Plane과 Bit Cell 번호
        elif plane == 5: planes = [1, 2, 4, 3]; bits = [[2, 1, 0]] *4           # D Plane 주변 Plane과 Bit Cell 번호

        if direction == 0:                                                      # direction이 0일 때: 시계 방향으로 회전
            temp1 = self.cell_bit[planes[3]][bits[3][0]]
            temp2 = self.cell_bit[planes[3]][bits[3][1]]                        # temp1, temp2, temp3: 자리 바꿀 떄 임시 저장
            temp3 = self.cell_bit[planes[3]][bits[3][2]]
            for i in [3, 2, 1]:
                for j in range(3):
                    self.cell_bit[planes[i]][bits[i][j]] = self.cell_bit[planes[i-1]][bits[i-1][j]]
            self.cell_bit[planes[0]][bits[0][0]] = temp1
            self.cell_bit[planes[0]][bits[0][1]] = temp2
            self.cell_bit[planes[0]][bits[0][2]] = temp3

        else: # direction == 1                                                  # direction이 1일 때: 반시계 방향으로 회전
            temp1 = self.cell_bit[planes[0]][bits[0][0]]
            temp2 = self.cell_bit[planes[0]][bits[0][1]]                        # temp1, temp2, temp3: 자리 바꿀 떄 임시 저장
            temp3 = self.cell_bit[planes[0]][bits[0][2]]
            for i in [0, 1, 2]:
                for j in range(3):
                    self.cell_bit[planes[i]][bits[i][j]] = self.cell_bit[planes[i+1]][bits[i+1][j]]
            self.cell_bit[planes[3]][bits[3][0]] = temp1
            self.cell_bit[planes[3]][bits[3][1]] = temp2
            self.cell_bit[planes[3]][bits[3][2]] = temp3

    # RotMidLine: 입력한 회전을 실행합니다.                                       ===== RotMidLine 함수 =====
    def RotMidLine(self, plane, mode, direction):                               # plane: 기준 Plane, mode: 회전할 층, direction: 시계/반시계 방향
        # mode - 0: M, 1: S, 2: E
        # plane == 0 or 5: mode = 2, plane == 1 or 4: mode == 1, plane == 2 or 3: mode = 0
        # plane == 0 or 2 or 4: flip direction

        if plane == -1: pass
        elif plane == 0: mode = 2; direction = 1 if direction == 0 else 0
        elif plane == 1: mode = 1
        elif plane == 2: mode = 0; direction = 1 if direction == 0 else 0
        elif plane == 3: mode = 0
        elif plane == 4: mode = 1; direction = 1 if direction == 0 else 0
        elif plane == 5: mode = 2

        if   mode == 0: planes = [0, 1, 5, 4]; bits = [[7, 3], [7, 3], [7, 3], [3, 7]] # M일 때
        elif mode == 1: planes = [0, 2, 5, 3]; bits = [[5, 1], [7, 3], [1, 5], [3, 7]] # S일 때
        elif mode == 2: planes = [1, 2, 4, 3]; bits = [[5, 1]] *4               # E일 때

        if direction == 0:                                                      # direction이 0일 때: 시계 방향으로 회전
            temp_edge1 = self.cell_bit[planes[3]][bits[3][0]]
            temp_edge2 = self.cell_bit[planes[3]][bits[3][1]]
            temp_data  = self.cell_data[planes[3]]
            temp_func  = self.cell_func[planes[3]]
            for i in [3, 2, 1]:
                for j in range(2):
                    self.cell_bit[planes[i]][bits[i][j]] = self.cell_bit[planes[i-1]][bit[i-1][j]]
                self.cell_data[planes[i]] = self.cell_data[planes[i-1]]
                self.cell_func[planes[i]] = self.cell_func[planes[i-1]]
            self.cell_bit[planes[0]][bits[0][0]] = temp_edge1
            self.cell_bit[planes[0]][bits[0][0]] = temp_edge2
            self.cell_data[planes[0]]            = temp_data
            self.cell_func[planes[0]]            = temp_func

        else: # direction == 1                                                  # direction이 1일 때: 반시계 방향으로 회전
            temp_edge1 = self.cell_bit[planes[0]][bits[0][0]]
            temp_edge2 = self.cell_bit[planes[0]][bits[0][1]]
            temp_data  = self.cell_data[planes[0]]
            temp_func  = self.cell_func[planes[0]]
            for i in [0, 1, 2]:
                for j in range(2):
                    self.cell_bit[planes[i]][bits[i][j]] = self.cell_bit[planes[i+1]][bit[i+1][j]]
                self.cell_data[planes[i]] = self.cell_data[planes[i+1]]
                self.cell_func[planes[i]] = self.cell_func[planes[i+1]]
            self.cell_bit[planes[3]][bits[0][0]] = temp_edge1
            self.cell_bit[planes[3]][bits[0][0]] = temp_edge2
            self.cell_data[planes[3]]            = temp_data
            self.cell_func[planes[3]]            = temp_func

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
                binary = self.Dec2Bin(planenum)                                    #   planenum 번째 Plane의 Bit Cell
                for bitnum in range(8):                                         #   planenum 번째 Plane의 bitnum 번째 Bit Cell에
                    self.cell_bit[planenum][bitnum] = binary[bitnum]               #   bitnum 번째 인덱스의 binary의 값 대입

        elif (plane > 5) | (plane < -1):                                        # 대상 Plane 번호가 범위 밖일 때:
            logging.error("Plane Number Should be -1, 0, 1, ..., or 5")         #   error 처리 (logging)
            return None                                                         #   Load 함수 종료

        else:                                                                   # 대상 Plane 번호가 0-5일 때:
            binary = self.Dec2Bin(plane)                                           #   plane 번째 Plane의 Bit Cell
            for bitnum in range(8):                                             #   plane 번째 Plane의 bitnum 번째 Bit Cell에
                self.cell_bit[plane][bitnum] = binary[bitnum]                      #   bitnum 번째 인덱스의 binary의 값 대입

    # Save: Bit Cell의 값을 Data Cell에 저장합니다.                               ===== Save 함수 =====
    def Save(self, plane = -1):
        if plane == -1:                                                         # 대상 Plane 번호가 -1일 때:
            for planenum in range(6):                                           #   모든 Plane에 대해 Save 실행
                self.cell_data[planenum] = self.Bin2Dec(planenum)               #   planenum 번째 Plane에서 Save

        elif (plane > 5) | (plane < -1):                                        # 대상 Plane 번호가 범위 밖일 때:
            logging.error("Plane Number Should be -1, 0, 1, ..., or 5")         #   error 처리 (logging)
            return None                                                         #   Save 함수 종료

        else:                                                                   # 대상 Plane 번호가 0-5일 때:
            self.cell_data[plane] = self.Bin2Dec(plane)                         #   plane 번째 Plane에서 Save

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
            if self.cell_func[plane] == "One":                                   # 대상 Plane이 Static One Cell일 때:
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
            if self.cell_func[plane] in ["Input", "Output", "Inout", "One"]:    #   plane의 역할이 Input/Output/Inout/Static One일 떄:
                pass                                                            #   실행 안 함
            elif self.cell_func[plane] == "And": self.And(plane)                #   AND  연산 실행
            elif self.cell_func[plane] == "Nand": self.Nand(plane)              #   NAND 연산 실행
            elif self.cell_func[plane] == "Or": self.Or(plane)                  #   Or   연산 실행
            elif self.cell_func[plane] == "Nor": self.Nor(plane)                #   NOR  연산 실행
            elif self.cell_func[plane] == "Xor": self.Xor(plane)                #   XOR  연산 실행
            elif self.cell_func[plane] == "Xnor": self.Xnor(plane)              #   XNOR 연산 실행
            elif self.cell_func[plane] == "Not": self.Not(plane)                #   NOT  연산 실행
            elif self.cell_func[plane] == "Shift": self.Shift(plane)            #   Shift     실행

    # Rotate: 입력 받은 회전 기호에 따라 큐브의 층을 회전시킵니다.                  ===== Rotate 함수 =====
    def Rotate(self, rot):                                                      # rot: 회전 기호

        if rot[0] in one_layer_rot_list:                                        # 대문자 회전 기호: 한 층만 회전
            plane = one_layer_rot_list.index(rot[0])                            # plane: 회전하려는 Plane 번호
            if len(rot) == 1:                                                   # 회전 기호가 한 글자: ' 없음 - 시계 방향
                self.RotPlane(plane, 0)                                         #   Plane 시계 방향으로 회전
                self.RotLine(plane, 0)                                          #   Plane 주위 layer 시계 방향으로 회전
            else: # len(rot) == 2                                               # 회전 기호가 두 글자: ' 있음 - 반시계 방향
                self.RotPlane(plane, 1)                                         #   Plane 반시계 방향으로 회전
                self.RotLine(plane, 1)                                          #   Plane 주위 layer 반시계 방향으로 회전

        elif rot[0] in two_layers_rot_list:                                     # 소문자 회전 기호: 두 층을 회전
            plane = two_layers_rot_list.index(rot[0])                           # plane: 회전하려는 Plane 번호
            if len(rot) == 1:                                                   # 회전 기호가 한 글자: ' 없음 - 시계 방향
                self.RotPlane(plane, 0)                                         #   Plane 시계 방향으로 회전
                self.RotLine(plane, 0)                                          #   Plane 주위 layer 시계 방향으로 회전
                self.RotMidLine(plane, 0, 0)                                    #   Plane 옆 layer 시계 방향으로 회전
            else: # len(rot) == 2                                               # 회전 기호가 두 글자: ' 있음 - 반시계 방향
                self.RotPlane(plane, 1)                                         #   Plane 반시계 방향으로 회전
                self.RotLine(plane, 1)                                          #   Plane 주위 layer 반시계 방향으로 회전
                self.RotMidLine(plane, 0, 1)                                    #   Plane 옆 layer 반시계 방향으로 회전

        elif rot[0] in center_layer_rot_list:                                   # M, S, E: 가운데 층을 회전
            mode = center_layer_rot_list.index(rot[0])                          # Mode: 회전하려는 layer 방향
            if len(rot) == 1:                                                   # 회전 기호가 한 글자: ' 없음 - 시계 방향
                self.RotMidLine(-1, mode, direction)                            #   가운데 layer 시계 방향으로 회전
            else: #len(rot) == 2                                                # 회전 기호가 두 글자: ' 있음 - 반시계 방향
                self.RotMidLine(-1, mode, direction)                            #   가운데 layer 반시계 방향으로 회전

    # Core Function: 'Cubes' class에서 사용하는 함수입니다. ===========================================================================

    # ShowPlane: 입력한 Plane의 Bit Cell의 비트 값과 자릿값, Data Cell의 값을 보여줍니다. ===== ShowPlane 함수 =====
    def ShowPlane(self, plane):                                                 # plane: 표시할 Plane 번호
        line_one   = "|  %3d %3d %3d  " % (self.cell_bit_plval[plane][6], self.cell_bit_plval[plane][7], self.cell_bit_plval[plane][0])
        line_two   = "|  %3d %3d %3d  " % (self.cell_bit[plane][6],       self.cell_bit[plane][7],       self.cell_bit[plane][0])
        line_three = "|  %3d %d %s %3d  " % (self.cell_bit_plval[plane][5], plane, one_layer_rot_list[plane], self.cell_bit_plval[plane][1])
        line_four  = "|  %3d %3d %3d  " % (self.cell_bit[plane][5],       self.cell_data[plane],         self.cell_bit[plane][1])
        line_five  = "|  %3d %3d %3d  " % (self.cell_bit_plval[plane][4], self.cell_bit_plval[plane][3], self.cell_bit_plval[plane][2])
        line_six   = "|  %3d %3d %3d  " % (self.cell_bit[plane][4],       self.cell_bit[plane][3],       self.cell_bit[plane][2])
        return [line_one, line_two, line_three, line_four, line_five, line_six]

    # Show: 프로그램을 실행했을 때 명령어 하나하나마다의 큐브의 상태를 보여줍니다.    ===== Show 함수 =====
    def Show(self):
        print("Sum of Bit Cell: ", end = '')                                    # Bit Cell의 값 표시
        for i in range(6):
            print("Face %s %d, " % (one_layer_rot_list[i], self.Bin2Dec(i)), end = '')
        print("Core Cell: %d" % self.cell_core, end = '')                       # Core Cell의 값 표시
        print()                                                                 # 줄바꿈
        print(" " *17 + "-" *15)
        print(" " *16 + self.ShowPlane(0)[0] + "|")
        print(" " *16 + self.ShowPlane(0)[1] + "|")
        print(" " *16 + self.ShowPlane(0)[2] + "| Plane UP(0):")
        print(" " *16 + self.ShowPlane(0)[3] + "| " + self.cell_func[0] + "Plane")
        print(" " *16 + self.ShowPlane(0)[4] + "|")
        print(" " *16 + self.ShowPlane(0)[5] + "|")
        print(" " + "-" *15 + " " + "-" *15 + " " + "-" *15 + " " + "-" *15)
        print(self.ShowPlane(3)[0] + self.ShowPlane(1)[0] + self.ShowPlane(2)[0] + self.ShowPlane(4)[0] + "|")
        print(self.ShowPlane(3)[1] + self.ShowPlane(1)[1] + self.ShowPlane(2)[1] + self.ShowPlane(4)[1] + "| FRONT(1): " + self.cell_func[1])
        print(self.ShowPlane(3)[2] + self.ShowPlane(1)[2] + self.ShowPlane(2)[2] + self.ShowPlane(4)[2] + "| RIGHT(2): " + self.cell_func[2])
        print(self.ShowPlane(3)[3] + self.ShowPlane(1)[3] + self.ShowPlane(2)[3] + self.ShowPlane(4)[3] + "| LEFT (3): " + self.cell_func[3])
        print(self.ShowPlane(3)[4] + self.ShowPlane(1)[4] + self.ShowPlane(2)[4] + self.ShowPlane(4)[4] + "| BACK (4): " + self.cell_func[4])
        print(self.ShowPlane(3)[5] + self.ShowPlane(1)[5] + self.ShowPlane(2)[5] + self.ShowPlane(4)[5] + "|")
        print(" " + "-" *15 + " " + "-" *15 + " " + "-" *15 + " " + "-" *15)
        print(" " *16 + self.ShowPlane(5)[0] + "|")
        print(" " *16 + self.ShowPlane(5)[1] + "|")
        print(" " *16 + self.ShowPlane(5)[2] + "| Plane DOWN(5):")
        print(" " *16 + self.ShowPlane(5)[3] + "| " + self.cell_func[5] + "Plane")
        print(" " *16 + self.ShowPlane(5)[4] + "|")
        print(" " *16 + self.ShowPlane(5)[5] + "|")
        print(" " *17 + "-" *15)
        print()

    # Printing Form
    # [                 ---------------]
    # [                |  plv plv plv  |]                                       # plv: 자릿값
    # [                |  bit bit bit  |]                                       # bit: 비트 값
    # [                |  plv pln plv  |  Plane UP(0):]                         # pln: Plane 번호 + Plane 방향
    # [                |  bit dta bit  |  Input Plane]                          # dta: 데이터 값
    # [                |  plv plv plv  |]
    # [                |  bit bit bit  |]
    # [ --------------- --------------- --------------- ---------------]
    # [|  plv plv plv  |  plv plv plv  |  plv plv plv  |  plv plv plv  |]
    # [|  bit bit bit  |  bit bit bit  |  bit bit bit  |  bit bit bit  | FRONT(1): Static One]
    # [|  plv pln plv  |  plv pln plv  |  plv pln plv  |  plv pln plv  | RIGHT(2): AND]
    # [|  bit dta bit  |  bit dta bit  |  bit dta bit  |  bit dta bit  | LEFT (3): OR]
    # [|  plv plv plv  |  plv plv plv  |  plv plv plv  |  plv plv plv  | BACK (4): NOT]
    # [|  bit bit bit  |  bit bit bit  |  bit bit bit  |  bit bit bit  |]
    # [ --------------- --------------- --------------- ---------------]
    # [                |  plv plv plv  |]
    # [                |  bit bit bit  |]
    # [                |  plv pln plv  |  Plane DOWN(5):]
    # [                |  bit dta bit  |  Output Plane]
    # [                |  plv plv plv  |]
    # [                |  bit bit bit  |]
    # [                 ---------------]


class Cubes:

    def __init__(self, c_debug = 0, c_ascii = 0, c_cube = False, c_step = 0):

        self.cubes = list()                                                     # 큐브 리스트

        self.c_debug = c_debug
        self.c_ascii = c_ascii
        self.c_step = c_step
        self.c_cube = c_cube

        cell_function, cell_bit_place_value = LoadCfg()                         # 사전 설정값 받아오기
        self.cube = Cube(cell_function, cell_bit_place_value)                   # 큐브 생성하기
        self.cubes.append(self.cube)


    # Create one cube, and set pointers
    def CreateCubeOnDirection(self, cube_structure, direction="in"):
        new_cube = Cube() #새로운 큐브를 제작함
        if direction == 'in': #방향이 in이라면
            new_cube.hyper_out = cube_structure #큐브 자료형에다가 기존의 큐브 구조를 할당함
            cube_structure.hyper_in = new_cube #기존 큐브 구조에다가 새로운 큐브 구조를 할당함
        else:
            new_cube.hyper_in = cube_structure
            cube_structure.hyper_out = new_cube
        self.cubes.append(new_cube)
        return new_cube


    # Exectue one command
    def Execute(self, script = ""):
        script_index = 0 #매길 인덱스들
        result = ""
        if script.count(")") != 0 and script.count("(") == script.count(")"):
            if script.count(")") == 0:
                logging.warning("Can't find ')', please write it.")
                raise CoreCellCmdError_NO
            else:
                logging.warning("('s count and )'s count are not match, please rewrite it.")
                raise CoreCellCmdError_COUNT
        #스크립트의 한글자 한글자씩 분석을 할 거기 때문에 인덱스로 할당함

        while script_index < len(script):
            print('위로올라옴')
            s_word = script[script_index]
            if s_word in rotate_list:
                if script_index+1 < len(script) and script[script_index+1] in ["'"]: #' 붙인 거 판별
                    logging.info("%s : Rotate"%script[script_index:script_index+2]) # 커맨드를 작성한다
                    self.cube.Rotate(script[script_index:script_index+2]) # rotate로 돌린다
                    script_index += 1 #일단 1만 더해준다음에 나중에 1 또 더해주니까(모든 if문을 빠져나오면 +1하게 설정할 것임) 1만 더해준다
                else:
                    logging.info("%s : Rotate"%s_word)
                    self.cube.Rotate(s_word)

            elif s_word in index_list: #명령 확장
                logging.info("%s Number inputed"%s_word)

            elif s_word == 'I': #input
                print(">"*9+"INPUT"+">"*9, end="")
                inp = input()
                logging.info("%s : Input"%s_word)
                self.cube.Input(ord(inp[0])) #첫 번째 글자 추출 후 아스키 코드로 변환함(한 글자밖에 받을 수 없음)

            elif s_word == 'P': #print
                logging.info("%s : Output"%(s_word))
                if self.c_ascii: result += chr(self.cube.Output())
                else: result += "%3d "%self.cube.output()

            elif s_word == "X": logging.info("%s: Execute"%s_word); self.cube.Execute()  #execute

            elif s_word == "*": logging.info("%s: Load"%s_word); self.cube.Load() #load

            elif s_word == "=": logging.info("%s: Save"%s_word); self.cube.Save() #save

            elif s_word == "C": logging.info("%s: Clear"%s_word); self.cube.Clear() #clear

            elif s == "(":
                if self.cube.cell_core != 0:
                    logging.info("%s: If open, Core Cell is Not Zero:%d"%(s_word,self.cube.cell_core))
                    # par_stack.append(script_index+1)
                else:
                    logging.info("%s: If open, Core Cell is Zero"%s_word)
                    locate = script_index+1
                    level = 0
                    # Need to converted into stack... for awesomeness
                    while locate < len(scr):
                        if script[locate] == "(": level += 1
                        elif script[locate] == ")":
                            if level > 0: level -= 1
                            else: break
                        locate += 1
                    script_index = locate

            elif s == ")":
                if self.cube.cell_core != 0:
                    logging.info("%s: If close, Core Cell is Not Zero:%d"%(s_word,self.cube.cell_core))
                    locate = script_index-1
                    level = 0
                    # Need to converted into stack... for awesomeness
                    while locate > 0:
                        if script[locate] == ")": level += 1
                        elif script[locate] == "(":
                            if level > 0: level -= 1
                            else: break
                        loc -= 1
                    script_index = locate
                else:
                    logging.info("%s If close, Core Cell is Zero"%s_word)
                    # par_stack.append(script_index+1)

            elif s == "!": logging.info("%s: Core <- Input"%s_word); self.cube.cell_core = self.cube.cell_data[0]

            elif s == "-": logging.info("%s: Core -= Input"%s_word); self.cube.cell_core -= self.cube.cell_data[0]

            elif s == "+": logging.info("%s: Core += Input"%s_word); self.cube.cell_core += self.cube.cell_data[0]

            elif s == "m": logging.info("%s: Core - 1"%s_word); self.cube.cell_core -= 1 #나중에 여기 수정해야 한다!!

            elif s == "p": logging.info("%s: Core + 1"%s_word); self.cube.cell_core += 1

            elif s_word == "[":
                if self.cube.hyper_in == None: new_cube = self.CreateCubeOnDirection(self.cube, "in")
                else: new_cube = self.cube.hyper_in
                logging.info("%s: Move Inside From %s to %s"%(s_word,id(self.cube),id(new_cube)))
                self.cube = new_cube

            elif s_word == "]":
                if self.cube.hyper_out == None: new_cube = self.CreateCubeOnDirection(self.cube, "out")
                else: new_cube = self.cube.hyper_out
                logging.info("%s: Move Outside From %s to %s"%(s_word,id(self.cube),id(new_cube)))
                self.cube = new_cube

            elif s_word == "{":
                if self.cube.hyper_in == None: new_cube = self.CreateCubeOnDirection(self.cube, "in")
                else: new_cube = self.cube.hyper_in
                logging.info("%s: Send Data Inside From %s to %s"%(s_word,id(self.cube),id(new_cube)))
                for i in range(6):
                    new_cube.cell_data[i] = self.cube.cell_data[i]

            elif s == "}":
                if self.cube.hyper_out == None: new_cube = self.CreateCubeOnDirection(self.cube, "out")
                else: new_cube = self.cube.hyper_out
                logging.info("%s: Send Data Outside From %s to %s"%(s_word,id(self.cube),id(new_cube)))
                for i in range(6):
                    new_cube.cell_data[i] = self.cube.cell_data[i]

            else:
                logging.info("%s: Unrecognized Character"%s_word)

                logging.warning("please input right Character")
                script_index += 1
                continue
            print(script_index)

            script_index += 1

            print(script_index)

            if self.c_cube:
                self.cube.Show() #보여주는 거 작성하는 함수는 아직

        logging.info('\n\n')
        return result
        pass
