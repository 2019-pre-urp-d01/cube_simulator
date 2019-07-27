import logging
import numpy as np

from setup_file_io import LoadCfg

# 각 Plane의 default function을 저장한 dictionary입니다.
# 0: up, 1: front, 2: right, 3: left, 4: back, 5: down
DEF_FUNC = {0:"Input", 1:"One", 2:"Not", 3:"Or", 4:"And", 5:"Output"}

# 각 Bit cell의 absolute position에 대응하는 default place value를 저장한 dictionary입니다.
DEF_UBIT_PLVAL = {0:1, 1:2, 2:4, 3:8, 4:16, 5:32, 6:64, 7:128}
DEF_FBIT_PLVAL = {0:1, 1:2, 2:4, 3:8, 4:16, 5:32, 6:64, 7:128}
DEF_RBIT_PLVAL = {0:1, 1:2, 2:4, 3:8, 4:16, 5:32, 6:64, 7:128}
DEF_LBIT_PLVAL = {0:1, 1:2, 2:4, 3:8, 4:16, 5:32, 6:64, 7:128}
DEF_BBIT_PLVAL = {0:1, 1:2, 2:4, 3:8, 4:16, 5:32, 6:64, 7:128}
DEF_DBIT_PLVAL = {0:1, 1:2, 2:4, 3:8, 4:16, 5:32, 6:64, 7:128}

class Cube:

    # Cube initialization: Cube의 initial state를 설정합니다. =========================================================================================================
    def __init__(self, cell_func_dict=DEF_FUNC, cell_ubit_plval_dict=DEF_UBIT_PLVAL, cell_fbit_plval_dict=DEF_FBIT_PLVAL, cell_rbit_plval_dict=DEF_RBIT_PLVAL, cell_lbit_plval_dict=DEF_LBIT_PLVAL, cell_bbit_plval_dict=DEF_BBIT_PLVAL, cell_dbit_plva_dict=DEF_DBIT_PLVAL):
        self.hyper_in  = None
        self.hyper_out = None

        # 각 Plane의 direction에 대응하는 function을 저장한 dictionary와 list입니다.
        self.cell_func_dict = cell_func_dict
        self.cell_func = list(self.cell_func_dict.values())

        # 각 Data Cell의 bit value를 저장한 dictionary와 list입니다.
        self.cell_data_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
        self.cell_data = list(self.cell_data_dict.values())

        # 각 Bit cell의 absolute position에 대응하는 bit value를 저장한 dictionary와 list입니다.
        self.cell_ubit_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        self.cell_fbit_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        self.cell_rbit_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        self.cell_lbit_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        self.cell_bbit_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        self.cell_dbit_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}

        self.cell_ubit = list(self.cell_ubit_dict.values())                     # 여기에 있는 6개의 list는
        self.cell_fbit = list(self.cell_fbit_dict.values())                     # cell_bit 리스트를
        self.cell_rbit = list(self.cell_rbit_dict.values())                     # 간단히 생성하기 위해 만든
        self.cell_lbit = list(self.cell_lbit_dict.values())                     # temporary list이므로
        self.cell_bbit = list(self.cell_bbit_dict.values())                     # 실제 연산에는 여기의 list 말고
        self.cell_dbit = list(self.cell_dbit_dict.values())                     # cell_bit 리스트를 사용할 것

        self.cell_bit = [self.cell_ubit, self.cell_fbit, self.cell_rbit,\
                         self.cell_lbit, self.cell_bbit, self.cell_dbit]

        # 각 Bit cell의 absolute position에 대응하는 place value를 저장한 dictionary와 list입니다.
        self.cell_ubit_plval_dict = cell_ubit_plval_dict
        self.cell_fbit_plval_dict = cell_fbit_plval_dict
        self.cell_rbit_plval_dict = cell_rbit_plval_dict
        self.cell_lbit_plval_dict = cell_lbit_plval_dict
        self.cell_bbit_plval_dict = cell_bbit_plval_dict
        self.cell_dbit_plval_dict = cell_dbit_plval_dict

        self.cell_ubit_plval = list(self.cell_ubit_plval_dict.values())         # 여기에 있는 6개의 list는
        self.cell_fbit_plval = list(self.cell_fbit_plval_dict.values())         # cell_bit 리스트를
        self.cell_rbit_plval = list(self.cell_rbit_plval_dict.values())         # 간단히 생성하기 위해 만든
        self.cell_lbit_plval = list(self.cell_lbit_plval_dict.values())         # temporary list이므로
        self.cell_bbit_plval = list(self.cell_bbit_plval_dict.values())         # 실제 연산에는 여기의 list 말고
        self.cell_dbit_plval = list(self.cell_dbit_plval_dict.values())         # cell_bit_plval 리스트를 사용할 것

        self.cell_bit_plval = [self.cell_ubit_plval, self.cell_fbit_plval,\
                               self.cell_rbit_plval, self.cell_lbit_plval,\
                               self.cell_bbit_plval, self.cell_dbit_plval]

        # Core cell에 저장된 값을 나타내는 variable입니다.
        self.cell_core = 0

    # Sub Function: Input, Output, Load, Save, Clear, Execute, Rotate를 수행하는 데 사용하는 function입니다. ================================================================

    # Bin2Dec: Bit Cell의 Binary를 Data Cell에 저장할 Demical로 바꿉니다.
    def Bin2Dec(self, planenum):                                                # planenum: 연산을 수행할 plane의 번호
        dec = 0                                                                 # demical을 저장하여 return할 variable
        for i in range(8):                                                      # 8개의 bit cell에 대하여 반복 수행
            dec += self.cell_bit[planenum][i] * self.cell_bit_plval             # bit 값과 자릿값을 곱한 값을 dec에 저장
        return dec                                                              # dec 값 반환

    # Dec2Bin: Data Cell의 Demical을 Bit Cell에 저장할 Binary로 바꿉니다.
    def Dec2Bin(self, planenum):                                                # planenum: 연산을 수행할 plane의 번호
        raw_bin = [0, 0, 0, 0, 0, 0, 0, 0]                                      # raw_bin: 순서대로 이진수를 저장할 list
        for i in range(8):                                                      # 8개의 bit cell에 대하여 반복 수행
            raw_bin[i] = self.cell_data[planenum] >> i & 1                      # raw_bin list의 i번째 원소에 값 저장
        bin = self.Raw2Plval(planenum, raw_bin)                                 # 사전 설정한 자릿값 순서에 맞게 비트 값 순서 변경
        return bin                                                              # bin list 반환

    # Raw2Plval: 2진수 list의 비트 값이 자릿값 순서대로 정렬되어 있는 것을 설정된 대로 바꿉니다.
    def Raw2Plval(self, planenum, raw_bin):                                     # planenum: 자릿값 순서를 찾을 면, raw_bin: 순서를 바꿀 비트 값 리스트
        bin = [0, 0, 0, 0, 0, 0, 0, 0]                                          # bin: 정렬된 2진수 리스트

        for ind, plval in enumerate(self.cell_bit_plval[planenum]):             # ind: 인덱스, plval: 자릿값
            if plval == 1:                                                      # 자릿값이 1이면
                bin[ind] = raw_bin[0]                                           # raw_bin의 첫째 자리의 값을 bin의 해당 인덱스에 저장
            elif plval == 2:                                                    # 자릿값이 2이면
                bin[ind] = raw_bin[1]                                           # raw_bin의 둘째 자리의 값을 bin의 해당 인덱스에 저장
            elif plval == 4:                                                    # 자릿값이 4이면
                bin[ind] = raw_bin[2]                                           # raw_bin의 셋째 자리의 값을 bin의 해당 인덱스에 저장
            elif plval == 8:                                                    # 자릿값이 8이면
                bin[ind] = raw_bin[3]                                           # raw_bin의 넷째 자리의 값을 bin의 해당 인덱스에 저장
            elif plval == 16:                                                   # 자릿값이 16이면
                bin[ind] = raw_bin[4]                                           # raw_bin의 다섯째 자리의 값을 bin의 해당 인덱스에 저장
            elif plval == 32:                                                   # 자릿값이 32이면
                bin[ind] = raw_bin[5]                                           # raw_bin의 여섯째 자리의 값을 bin의 해당 인덱스에 저장
            elif plval == 64:                                                   # 자릿값이 64이면
                bin[ind] = raw_bin[6]                                           # raw_bin의 일곱째 자리의 값을 bin의 해당 인덱스에 저장
            elif plval == 128:                                                  # 자릿값이 128이면
                bin[ind] = raw_bin[7]                                           # raw_bin의 여덟째 자리의 값을 bin의 해당 인덱스에 저장

        return bin                                                              # bin list 반환

    # Plval2Raw: 2진수 list의 비트 값이 설정된 대로 있는 것을 자릿값 순서대로 정렬합니다.
    def Plval2Raw(self, planenum, bin):                                         # planenum: 자릿값 순서를 찾을 면, bin: 순서를 바꿀 비트 값 리스트
        raw_bin = [0, 0, 0, 0, 0, 0, 0, 0]                                      # raw_bin: 정렬된 2진수 리스트

        for ind, plval in enumerate(self.cell_bit_plval[planenum]):             # ind: 인덱스, plval: 자릿값
            if plval == 1:                                                      # 자릿값이 1이면
                raw_bin[0] = bin[ind]                                           # bin의 해당 인덱스의 값을 raw_bin의 첫째 자리에 저장
            elif plval == 2:                                                    # 자릿값이 2이면
                raw_bin[1] = bin[ind]                                           # bin의 해당 인덱스의 값을 raw_bin의 둘째 자리에 저장
            elif plval == 4:                                                    # 자릿값이 4이면
                raw_bin[2] = bin[ind]                                           # bin의 해당 인덱스의 값을 raw_bin의 셋째 자리에 저장
            elif plval == 8:                                                    # 자릿값이 8이면
                raw_bin[3] = bin[ind]                                           # bin의 해당 인덱스의 값을 raw_bin의 넷째 자리에 저장
            elif plval == 16:                                                   # 자릿값이 16이면
                raw_bin[4] = bin[ind]                                           # bin의 해당 인덱스의 값을 raw_bin의 다섯째 자리에 저장
            elif plval == 32:                                                   # 자릿값이 32이면
                raw_bin[5] = bin[ind]                                           # bin의 해당 인덱스의 값을 raw_bin의 여섯째 자리에 저장
            elif plval == 64:                                                   # 자릿값이 64이면
                raw_bin[6] = bin[ind]                                           # bin의 해당 인덱스의 값을 raw_bin의 일곱째 자리에 저장
            elif plval == 128:                                                  # 자릿값이 128이면
                raw_bin[7] = bin[ind]                                           # bin의 해당 인덱스의 값을 raw_bin의 여덟째 자리에 저장

        return raw_bin                                                          # raw_bin list 반환

    # FindPlane: 입력한 function을 가지고 있는 plane을 모두 찾아 list를 만듭니다.
    def FindPlane(self, planefunc):                                             # planefunc: 찾을 plane의 function
        planenum = list()                                                       # planenum: 결과를 찾아 저장할 list
        for ind, func in enumerate(self.cell_func):                             # ind: 인덱스, func: 역할
            planenum.append(ind) if func == planefunc else pass                 # func와 planefunc가 같으면 ind를 planenum에 추가
        return planenum                                                         # planenum list 반환

    # And: Data Cell과 Bit Cell 사이에 AND 연산을 수행합니다.
    def And(self, planenum):                                                    # planenum: AND 연산을 수행할 Plane 번호
        and_val1 = self.cell_data[planenum]                                     # and_val1: AND 연산을 수행할 값 1(Data Cell)
        and_val2 = self.Bin2Dec(planenum)                                       # and_val2: AND 연산을 수행할 값 2(Bit Cell)
        and_result = and_val1 & and_val2                                        # and_result: AND 연산 수행 결과
        self.cell_data[planenum] = and_result                                   # Data Cell에 and_result 저장
        return and_result                                                       # Nand()를 위해 and_result 반환

    # Nand: Data Cell과 Bit Cell 사이에 NAND 연산을 수행합니다.
    def Nand(self, planenum):                                                   # planenum: NAND 연산을 수행할 Plane 번호
        nand_result = ~self.And(planenum)                                       # And()의 결과에 not 연산 수행
        self.cell_data[planenum] = nand_result                                  # Data Cell에 nand_result 저장

    # Or: Data Cell과 Bit Cell 사이에 OR 연산을 수행합니다.
    def Or(self, planenum):                                                     # planenum: OR 연산을 수행할 Plane 번호
        or_val1 = self.cell_data[planenum]                                      # or_val1: OR 연산을 수행할 값 1(Data Cell)
        or_val2 = self.Bin2Dec(planenum)                                        # or_val2: OR 연산을 수행할 값 2(Bit Cell)
        or_result = or_val1 | or_val2                                           # or_result: OR 연산 수행 결과
        self.cell_data[planenum] = or_result                                    # Data Cell에 or_result 저장
        return or_result                                                        # Nor()를 위해 or_result 반환

    # Nor: Data Cell과 Bit Cell 사이에 NOR 연산을 수행합니다.
    def Nor(Self, planenum):                                                    # planenum: NOR 연산을 수행할 Plane 번호
        nor_result = ~self.Or(planenum)                                         # Or()의 결과에 not 연산 수행
        self.cell_data[planenum] = nor_result                                   # Data Cell에 nor_result 저장

    # Xor: Data Cell과 Bit Cell 사이에 XOR 연산을 수행합니다.
    def Xor(self, planenum):                                                    # planenum: XOR 연산을 수행할 Plane 번호
        xor_val1 = self.cell_data[planenum]                                     # xor_val1: XOR 연산을 수행할 값 1(Data Cell)
        xor_val2 = self.Bin2Dec(planenum)                                       # xor_val2: XOR 연산을 수행할 값 2(Bit Cell)
        xor_result = xor_val1 ^ xor_val2                                        # xor_result: XOR 연산 수행 결과
        self.cell_data[planenum] = xor_result                                   # Data Cell에 xor_result 저장
        return xor_result                                                       # Xnor()를 위해 xor_result 반환

    # Xnor: Data Cell과 Bit Cell 사이에 XNOR 연산을 수행합니다.
    def Xnor(self, planenum):                                                   # planenum: XNOR 연산을 수행할 plane 번호
        xnor_result = ~self.Xor(planenum)                                       # Xor()의 결과에 not 연산 수행
        self.cell_data[planenum] = xnor_result                                  # Data Cell에 xnor_result 저장

    # Not: Bit Cell에서 NOT 연산을 수행합니다.
    def Not(self, planenum):                                                    # planenum: NOT 연산을 수행할 plane 번호
        not_val = self.Bin2Dec(planenum)                                        # not_val: NOT 연산을 수행할 값 (Bit Cell)
        not_result = ~not_val                                                   # not_result: NOT 연산 수행 결과
        self.cell_data[planenum] = not_result                                   # Data Cell에 not_result 저장

    # StaticOne: Static One Plane의 Data Cell의 값을 1로 고정합니다.
    def StaticOne(self):
        planenum = self.FindPlane("One")                                        # 역할이 One인 plane 찾기
        for num in planenum:                                                    # plane 리스트의 모든 원소에 대해 반복
            self.cell_data[num] = 1                                             # 해당 plane의 data cell의 값을 1로 설정

    # Shift: 입력한 plane의 모든 bit cell의 값을 한 칸씩 시계방향으로 옮기고, 첫 번쨰 셀의 값은 0으로 바꿉니다.
    def Shift(self, planenum):                                                  # planenum: Shift를 수행할 plane 번호
        bin = self.cell_bit[planenum]                                           # bin: 해당 plane의 bit cell의 비트 값을 저장한 리스트
        raw_bin = Plval2Raw(planenum, bin)                                      # bin의 비트 값을 자릿값 순서대로 정렬
        for i in range(7):                                                      # 0부터 6까지 7번 반복
            self.raw_bin[7-i] = self.raw_bin[6-i]                               # i번쨰 값을 i+1로 이동
        self.raw_bin[0] = 0                                                     # 첫 번째 값을 0으로 설정
        bin = Raw2Plval(planenum, raw_bin)                                      # raw_bin의 비트 값을 해당 면의 자릿값 순서대로 정렬
        self.cell_bit[planenum] = bin                                           # 해당 plane의 bit cell의 비트 값에 shift한 비트 값 저장

    # Main Function: Input, Output, Load, Save, Clear, Execute, Rotate를 수행하는 function입니다. ======================================================================

    # Input: Input Plane에서 값을 받아옵니다.
    def Input(self, input_value):                                               # input_value: 입력받은 값
        planenum = self.FindPlane("Input")                                      # planenum: 모든 Input Cell의 번호를 담은 list
        if len(planenum) == 0:                                                  # Input Plane이 없을 때:
            logging.error("Couldn't find Input Plane")                          #   error 처리 (logging)
            return None                                                         #   Input 함수 종료
        for num in planenum:                                                    # planenum의 모든 값에 대해 반복
            self.cell_data[num] = input_value                                   # Data Cell에 입력 받은 값 저장

    # Output: Output Plane의 값을 출력합니다.
    def Output(self):
        planenum = self.FindPlane("Output")                                     # planenum: 모든 Output Cell의 번호를 담은 list
        if len(planenum) == 0:                                                  # Output Plane이 없을 때:
            logging.error("Couldn't find Output Plane")                         #   error 처리 (logging)
            return None                                                         #   Output 함수 종료
        elif len(planenum) > 1:                                                 # Output Plane이 여러 개일 떄:
            logging.error("Nonsense cube; more than one output cell")           #   error 처리 (logging)
            return None                                                         #   Output 함수 종료
        return self.cell_data[planenum[0]]                                      # Data Cell의 값 반환

    # Load: Data Cell의 값을 Bit Cell에 저장합니다.
    def Load(self, ):
        pass

    # Save: Bit Cell의 값을 Data Cell에 저장합니다.
    def Save(self, ):
        pass

    # Clear: Plane의 Bit Cell과 Data Cell의 값을 초기 상태로 되돌립니다.
    def Clear(self, ):
        pass

    # Execute: 비트 연산(AND, NAND, OR, NOR, XOR, XNOR, NOT)과 Shift 연산을 수행합니다.
    def Execute(self, plane = -1):
        pass

    # Rotate: 입력 받은 회전 기호에 따라 큐브의 층을 회전시킵니다.
    def Rotate(self, ):
        pass
