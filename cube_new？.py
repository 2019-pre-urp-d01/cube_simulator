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

    # Cube initialization
    def __init__(self, cell_func_dict=DEF_FUNC, cell_ubit_plval_dict=DEF_UBIT_PLVAL, cell_fbit_plval_dict=DEF_FBIT_PLVAL, cell_rbit_plval_dict=DEF_RBIT_PLVAL, cell_lbit_plval_dict=DEF_LBIT_PLVAL, cell_bbit_plval_dict=DEF_BBIT_PLVAL, cell_dbit_plva_dict=DEF_DBIT_PLVAL):
        self.hyper_in  = None
        self.hyper_out = None

        # 각 Plane의 direction에 대응하는 function을 저장한 dictionary와 list입니다.
        # Cell's function of each cell
        self.cell_func_dict = cell_func_dict
        self.cell_func = list(self.cell_func_dict.values())

        # Data Cells: 각 Data Cell의 bit value를 저장한 dictionary와 list입니다.
        self.cell_data_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
        self.cell_data = list(self.cell_data_dict.values())

        # Bit Cells: 각 Bit cell의 absolute position에 대응하는 bit value를 저장한 dictionary와 list입니다.
        self.cell_ubit_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        self.cell_fbit_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        self.cell_rbit_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        self.cell_lbit_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        self.cell_bbit_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        self.cell_dbit_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}

        self.cell_ubit = list(self.cell_ubit_dict.values())
        self.cell_fbit = list(self.cell_fbit_dict.values())
        self.cell_rbit = list(self.cell_rbit_dict.values())
        self.cell_lbit = list(self.cell_lbit_dict.values())
        self.cell_bbit = list(self.cell_bbit_dict.values())
        self.cell_dbit = list(self.cell_dbit_dict.values())

        # Bit Cells: 각 Bit cell의 absolute position에 대응하는 place value를 저장한 dictionary와 list입니다.
        self.cell_ubit_plval_dict = cell_ubit_plval_dict
        self.cell_fbit_plval_dict = cell_fbit_plval_dict
        self.cell_rbit_plval_dict = cell_rbit_plval_dict
        self.cell_lbit_plval_dict = cell_lbit_plval_dict
        self.cell_bbit_plval_dict = cell_bbit_plval_dict
        self.cell_dbit_plval_dict = cell_dbit_plval_dict

        self.cell_ubit_plval = list(self.cell_ubit_plval_dict.values())
        self.cell_fbit_plval = list(self.cell_fbit_plval_dict.values())
        self.cell_rbit_plval = list(self.cell_rbit_plval_dict.values())
        self.cell_lbit_plval = list(self.cell_lbit_plval_dict.values())
        self.cell_bbit_plval = list(self.cell_bbit_plval_dict.values())
        self.cell_dbit_plval = list(self.cell_dbit_plval_dict.values())

        #Core Cell: Core cell에 저장된 값을 나타내는 variable입니다.
        self.cell_core = 0

    # Sub Function: Input, Output, Load, Save, Clear, Execute, Rotate를 수행하는 데 사용하는 function입니다.
    def Dec2Bin(self, ):
        pass

    def Bin2Dec(self, ):
        pass

    def Findplane(self, ):
        pass

    # Main Function: StaticOne, Input, Output, Load, Save, Clear, Execute, Rotate를 수행하는 function입니다.
