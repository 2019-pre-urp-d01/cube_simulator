import logging
import numpy as np

rotate_list = ["U", "D", "L", "R", "F", "B", "u", "d", "l", "r", "f", "b", "M", "S", "E"]
index_list = ["0", "1", "2", "3", "4", "5", "6"]

from setup_file_io import LoadCfg

DEFAULT_FUNCTION = {0:"Input", 1:"One", 2:"Not", 3:"Or", 4:"And", 5:"Output"}

DEFAULT_UP_BIT_DICT    = {"u0":0, "u1":0, "u2":0, "u3":0, "u4":0, "u5":0, "u6":0, "u7":0}
DEFAULT_FRONT_BIT_DICT = {"f0":0, "f1":0, "f2":0, "f3":0, "f4":0, "f5":0, "f6":0, "f7":0}
DEFAULT_RIGHT_BIT_DICT = {"r0":0, "r1":0, "r2":0, "r3":0, "r4":0, "r5":0, "r6":0, "r7":0}
DEFAULT_LEFT_BIT_DICT  = {"l0":0, "l1":0, "l2":0, "l3":0, "l4":0, "l5":0, "l6":0, "l7":0}
DEFAULT_BACK_BIT_DICT  = {"b0":0, "b1":0, "b2":0, "b3":0, "b4":0, "b5":0, "b6":0, "b7":0}
DEFAULT_DOWN_BIT_DICT  = {"d0":0, "d1":0, "d2":0, "d3":0, "d4":0, "d5":0, "d6":0, "d7":0}

class Cube:
    # Cube initialization
    def __init__(self, cell_function_dict=DEFAULT_FUNCTION, cell_bit_up_dict=DEFAULT_UP_BIT_DICT, cell_bit_front_dict=DEFAULT_FRONT_BIT_DICT, cell_bit_right_dict=DEFAULT_RIGHT_BIT_DICT, cell_bit_left_dict=DEFAULT_LEFT_BIT_DICT, cell_bit_back_dict=DEFAULT_BACK_BIT_DICT, cell_bit_down_dict=DEFAULT_DOWN_BIT_DICT):
        self.hyper_in  = None
        self.hyper_out = None #Cubes에서 이용할 하이퍼인, 하이퍼아웃

        # Cell's function of each cell
        self.cell_function_dict = cell_function_dict
        self.cell_function = list(self.cell_function_dict.values())

        # Bit Cells
        self.cell_data_dict = {"U":0, "F":0, "R":0, "L":0, "B":0, "D":0}
        self.cell_data = list(self.cell_data_dict.values())

        # Data Cells
        self.cell_bit_up_dict    = cell_bit_up_dict
        self.cell_bit_front_dict = cell_bit_front_dict
        self.cell_bit_right_dict = cell_bit_right_dict
        self.cell_bit_left_dict  = cell_bit_left_dict
        self.cell_bit_back_dict  = cell_bit_back_dict
        self.cell_bit_down_dict  = cell_bit_down_dict

        self.cell_bit_up    = list(self.cell_bit_up_dict.values())
        self.cell_bit_front = list(self.cell_bit_front_dict.values())
        self.cell_bit_right = list(self.cell_bit_right_dict.values())
        self.cell_bit_left  = list(self.cell_bit_left_dict.values())
        self.cell_bit_back  = list(self.cell_bit_back_dict.values())
        self.cell_bit_down  = list(self.cell_bit_down_dict.values())

        self.cell_bit  = [self.cell_bit_up, self.cell_bit_front, self.cell_bit_right, self.cell_bit_left, self.cell_bit_back, self.cell_bit_down]

        # Core Cell
        self.cell_core = 0

    # Change cell's function as set-up file
    def SetUpPlane(self, file):
        self.setup_file = open(file, 'r')

        # Read whole line from file, lines 29-34
        for txt_ind, txt_ln in enumerate(self.setup_file):
            if   txt_ind == 28:    up_plane = txt_ln
            elif txt_ind == 29: front_plane = txt_ln
            elif txt_ind == 30: right_plane = txt_ln
            elif txt_ind == 31:  left_plane = txt_ln
            elif txt_ind == 32:  back_plane = txt_ln
            elif txt_ind == 33:  down_plane = txt_ln
        raw_plane = [up_plane, front_plane, right_plane, left_plane, back_plane, down_plane]

        # Read bit cells' positions from file
        self.cell_list = (self.setup_file.split(""))
        self.start_ind = self.cell_list.index("Available Actions")


        # Change cell's function if set-up actions are not blank
        for i in raw_plane:
            if len(raw_plane[i]) < 5: pass
            else: self.cell_function_dict[i] = raw_plane[i][4:]
        self.cell_function = list(self.cell_function_dict.values())

    # Convert Bit Cells' binary to Data Cell's Demical
    def Bit2Dec(self, plane):
        dec = 0
        for bitnum in range(8):
            dec += self.cell_bit[plane][bitnum] << bitnum
        return dec

    # Find corresponding Planes
    def FindPlane(self, inp):
        res = []
        for ind, val in enumerate(self.cell_function):
            if val==inp:
                res.append(ind)
                # return ind
        return res

    # Set Static 1 Cell's value to 1
    def StaticOne(self):
        planenum = self.FindPlane("One")
        self.cell_data[planenum] = 1

    # Store input value to input plane's data cell
    def Input(self, val):
        plane = self.FindPlane("Input")
        if len(plane) == 0:
            logging.error("error: Couldn't find input plane")
            return None
        for p in plane:
            self.cell_data[p] = val

    # Return value from output plane's data cell
    def Output(self):
        plane = self.FindPlane("Output")

        if len(plane) == 0:
            logging.error("error: Couldn't find output plane")
            return None
        elif len(plane) > 1:
            logging.error("Nonsense cube; more than one output cell")
        return self.cell_data[p]

    # Save bit cell to data cell
    def Save(self, plane=-1):
        if plane == -1:
            for i in range(6):
                self.cell_data[i] = self.Bit2Dec(i)
        elif (plane < 6) & (plane > -1):
            self.cell_data[plane] = self.Bit2Dec(plane)
        else:
            logging.error("error: Couldn't find that plane")
            return None

    # Load data cell to bit cell
    def Load(self, plane=-1):
        if plane == -1:
            for i in range(6):
                for bitnum in range(8):
                    self.cell_bit[i][bitnum] = (self.cell_data[i] >> bitnum) & 1
        elif (plane < 6) & (plane > -1):
            for bitnum in range(8):
                self.cell_bit[plane][bitnum] = (self.cell_data[plane] >> bitnum) & 1
        else:
            logging.error("error: Couldn't find that plane")
            return None

    # Clear every cell to initial state
    def Clear(self, plane=-1):
        if plane == -1:
            self.cell_data = [0]*6
            self.cell_bit  = [[0]*8]*6
            self.cell_core = 0
        elif (plane < 6) & (plane > -1):
            self.cell_data[plane] = 0
            for i in range(8):
                self.cell_bit[plane][i] = 0
        else:
            logging.error("error: Couldn't find that plane")
        self.StaticOne()

    # Execute cell
    def Execute(self, plane=-1):
        if plane == -1:
            var_and  = self.FindPlane("And")
            var_or   = self.FindPlane("Or")
            var_xor  = self.FindPlane("Xor")
            var_nand = self.FindPlane("Nand")
            var_nor  = self.FindPlane("Nor")
            var_xnor = self.FindPlane("Xnor")
            var_not  = self.FindPlane("Not")

            if var_and != -1:
                self.cell_data[var_and] = self.cell_data[var_and] & self.Bin2Dec(var_and)
            if var_or != -1:
                self.cell_data[var_or] = self.cell_data[var_or] | self.Bin2Dec(var_or)
            if var_xor != -1:
                self.cell_data[var_xor] = self.cell_data[var_xor] ^ self.Bin2Dec(var_xor)
            if var_nand != -1:
                self.cell_data[var_nand] = ~(self.cell_data[var_nand] & self.Bin2Dec(var_nand))
            if var_nor != -1:
                self.cell_data[var_nor] = ~(self.cell_data[var_nor] | self.Bin2Dec(var_nor))
            if var_xnor != -1:
                self.cell_data[var_xnor] = ~(self.cell_data[var_xnor] ^ self.Bin2Dec(var_xnor))
            if var_not != -1:
                self.cell_data[var_not] = ~self.Bin2Dec(var_not)

        elif plane < 6:
            if self.cell_function[plane] == "Input" or "Output" or "One":
                pass
            elif self.cell_function[plane] == "And":
                self.cell_data[plane] = self.cell_data[plane] & self.Bin2Dec(plane)
            elif self.cell_function[plane] == "Or":
                self.cell_data[plane] = self.cell_data[plane] | self.Bin2Dec(plane)
            elif self.cell_function[plane] == "Xor":
                self.cell_data[plane] = self.cell_data[plane] ^ self.Bin2Dec(plane)
            elif self.cell_function[plane] == "Nand":
                self.cell_data[plane] = ~(self.cell_data[plane] & self.Bin2Dec(plane))
            elif self.cell_function[plane] == "Nor":
                self.cell_data[plane] = ~(self.cell_data[plane] | self.Bin2Dec(plane))
            elif self.cell_function[plane] == "Xnor":
                self.cell_data[plane] = ~(self.cell_data[plane] ^ self.Bin2Dec(plane))
            elif self.cell_function[plane] == "Not":
                self.cell_data[plane] = ~self.Bin2Dec(plane)

        else:
            logging.error("error: Couldn't find that plane")
            return None

    # Rotate cube
    def Rotate(self):
        pass

class Cubes:
    def __init__(self, c_debug=0, c_ascii=0, c_cube=False, c_step=0):
        # List of cubes
        self.cubes = list()
        # Generate One cube

        self.c_debug = c_debug
        self.c_ascii = c_ascii
        self.c_step = c_step
        self.cube = Cube()

        func_dict, ubit_dict, fbit_dict, rbit_dict, lbit_dict, bbit_dict, dbit_dict = LoadCfg(fileLoc)
        self.cube = Cube(func_dict)

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
        s_word = script[script_index] #스크립트의 한글자 한글자씩 분석을 할 거기 때문에 인덱스로 할당함
        while script_index < len(script):
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
                input_ = input()
                logging.info("%s : Input"%s_word)
                self.cube.Input(ord(input_[0])) #첫번째 글자 추출 후 아스키 코드로 변환함(한 글자밖에 받을 수 없음)
            elif s_word == 'P': #print
                logging.info("%s : Output -> %s"%(s_word, input_[0]))
                if self.c_ascii: result += chr(self.cube.Output())
                else: result += "%3d "%self.cube.output()
            elif s_word == "X": logging.info("%s: Execute"%s); self.cube.execute()  #execute
            elif s_word == "*": logging.info("%s: Load"%s); self.cube.load() #load
            elif s_word == "=": logging.info("%s: Save"%s); self.cube.save() #save
            elif s_word == "C": logging.info("%s: Clear"%s); self.cube.clear() #clear
            elif s_word == "(": pass #감산기, 가산기 기능으로 변경할 예정
            elif s_word == ")": pass
            elif s_word == "!": pass
            elif s_word == "-": pass
            elif s_word == "+": pass
            elif s_word == "m": pass
            elif s_word == "p": pass
            elif s_word == "[":
                if self.cube.hyper_in == None: new_cube = self.CreateCubeOnDirection(self.cube, "in")
                else: new_cube = self.cube.hyper_in
                loggign.info("%s: Move Inside From %s to %s"%(s_word,id(self.cube),id(new_cube)))
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
            script_index += 1
            if self.c_cube:
                self.cube.Show() #보여주는 거 작성하는 함수는 아직
                
        logging.info('\n\n')
        return result

            

            
