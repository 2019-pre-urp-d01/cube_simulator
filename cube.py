import logging
import numpy as np

from setup_file_io import LoadCfg

DEFAULT_FUNCTION = {0:"Input", 1:"One", 2:"Not", 3:"Or", 4:"And", 5:"Output"}

DEFAULT_UP_BIT_DICT    = {"u0":[1,0], "u1":[2,0], "u2":[4,0], "u3":[8,0], "u4":[16,0], "u5":[32,0], "u6":[64,0], "u7":[128,0]}
DEFAULT_FRONT_BIT_DICT = {"f0":[1,0], "f1":[2,0], "f2":[4,0], "f3":[8,0], "f4":[16,0], "f5":[32,0], "f6":[64,0], "f7":[128,0]}
DEFAULT_RIGHT_BIT_DICT = {"r0":[1,0], "r1":[2,0], "r2":[4,0], "r3":[8,0], "r4":[16,0], "r5":[32,0], "r6":[64,0], "r7":[128,0]}
DEFAULT_LEFT_BIT_DICT  = {"l0":[1,0], "l1":[2,0], "l2":[4,0], "l3":[8,0], "l4":[16,0], "l5":[32,0], "l6":[64,0], "l7":[128,0]}
DEFAULT_BACK_BIT_DICT  = {"b0":[1,0], "b1":[2,0], "b2":[4,0], "b3":[8,0], "b4":[16,0], "b5":[32,0], "b6":[64,0], "b7":[128,0]}
DEFAULT_DOWN_BIT_DICT  = {"d0":[1,0], "d1":[2,0], "d2":[4,0], "d3":[8,0], "d4":[16,0], "d5":[32,0], "d6":[64,0], "d7":[128,0]}

rotate_list = ["U", "D", "L", "R", "F", "B", "u", "d", "l", "r", "f", "b", "M", "S", "E"]
index_list = ["0", "1", "2", "3", "4", "5", "6"]

class Cube:
    # Cube initialization
    def __init__(self, cell_function_dict=DEFAULT_FUNCTION, cell_bit_up_dict=DEFAULT_UP_BIT_DICT, cell_bit_front_dict=DEFAULT_FRONT_BIT_DICT, cell_bit_right_dict=DEFAULT_RIGHT_BIT_DICT, cell_bit_left_dict=DEFAULT_LEFT_BIT_DICT, cell_bit_back_dict=DEFAULT_BACK_BIT_DICT, cell_bit_down_dict=DEFAULT_DOWN_BIT_DICT):
        self.hyper_in  = None
        self.hyper_out = None

        # Cell's function of each cell
        self.cell_function_dict = cell_function_dict
        self.cell_function = list(self.cell_function_dict.values())

        # Data Cells
        self.cell_data_dict = {"U":0, "F":0, "R":0, "L":0, "B":0, "D":0}
        self.cell_data = list(self.cell_data_dict.values())

        # Bit Cells
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

        self.cell_val  = [list(self.cell_bit_up_dict.keys()), list(self.cell_bit_front_dict.keys()), list(self.cell_bit_right_dict.keys()), list(self.cell_bit_left_dict.keys()), list(self.cell_bit_back_dict.keys()), list(self.cell_bit_back_down.keys())]
        self.cell_bit  = [self.cell_bit_up, self.cell_bit_front, self.cell_bit_right, self.cell_bit_left, self.cell_bit_back, self.cell_bit_down]

        # Core Cell
        self.cell_core = 0

    # Convert Bit Cells' binary to Data Cell's demical
    def Bit2Dec(self, plane):
        dec = 0
        for num in range(8):
            dec += (self.cell_bit[num][0] * self.cell_bit[num][1])
        return dec

    # Convert Data Cell's demical to Bit Cells' binary
    def Dec2Bin(self, plane):
        bin = list(bin(self.cell_data[plane])[2:])
        list_bin = list(map(int, bin))
        return list_bin

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
            logging.error("Couldn't find input plane")
            return None
        for p in plane:
            self.cell_data[p] = val

    # Return value from output plane's data cell
    def Output(self):
        plane = self.FindPlane("Output")
        if len(plane) == 0:
            logging.error("Couldn't find output plane")
            return None
        elif len(plane) > 1:
            logging.error("Nonsense cube; more than one output cell")
        return self.cell_data[plane[0]]

    # Save bit cell to data cell
    def Save(self, plane=-1):
        if plane == -1:
            for i in range(6):
                self.cell_data[i] = self.Bit2Dec(i)
        elif (plane < 6) & (plane > -1):
            self.cell_data[plane] = self.Bit2Dec(plane)
        else:
            logging.error("Couldn't find that plane")
            return None

    # Load data cell to bit cell
    def Load(self, plane=-1):
        if plane == -1:
            for i in range(6):
                self.cell_bit[i] = [0, 0, 0, 0, 0, 0, 0, 0]
                list_bin = self.Dec2Bin(i)
                while len(list_bin) < 8:
                    list_bin.append(0, 0)
                for j in range(8):
                    if list_bin[j] == 0: pass
                    else:
                        for k in range(8):
                            if self.cell_val[i][k] == 2 ** list_bin[j]:
                                self.cell_bit[i][k] == 1

            self.cell_bit_up = self.cell_bit[0]
            self.cell_bit_front = self.cell_bit[1]
            self.cell_bit_right = self.cell_bit[2]
            self.cell_bit_left = self.cell_bit[3]
            self.cell_bit_back = self.cell_bit[4]
            self.cell_bit_down = self.cell_bit[5]
            self.cell_bit_up_dict.values() = self.cell_bit_up
            self.cell_bit_front_dict.values() = self.cell_bit_front
            self.cell_bit_right_dict.values() = self.cell_bit_right
            self.cell_bit_left_dict.values() = self.cell_bit_left
            self.cell_bit_back_dict.values() = self.cell_bit_back
            self.cell_bit_down_dict.values() = self.cell_bit_down

        elif (plane < 6) & (plane > -1):
            self.cell_bit[plane] = [0, 0, 0, 0, 0, 0, 0, 0]
            list_bin = self.Dec2Bin(plane)
            while len(list_bin) < 8:
                list_bin.append(0, 0)
            for j in range(8):
                if list_bin[j] == 0: pass
                else:
                    for k in range(8):
                        if self.cell_val[plane][k] == 2 ** list_bin[j]:
                            self.cell_bit[plane][k] == 1
        else:
            logging.error("Couldn't find that plane")
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
            logging.error("Couldn't find that plane")
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

            if len(var_and) != 0:
                for i in var_and:
                    self.cell_data[var_and[i]] = self.cell_data[var_and[i]] & self.Bin2Dec(var_and[i])
            if len(var_or) != 0:
                for i in var_or:
                    self.cell_data[var_or[i]] = self.cell_data[var_or[i]] | self.Bin2Dec(var_or[i])
            if var_xor != 0:
                for i in var_xor:
                    self.cell_data[var_xor[i]] = self.cell_data[var_xor[i]] ^ self.Bin2Dec(var_xor[i])
            if var_nand != 0:
                for i in var_nand:
                    self.cell_data[var_nand[i]] = ~(self.cell_data[var_nand[i]] & self.Bin2Dec(var_nand[i]))
            if var_nor != 0:
                for i in var_nor:
                    self.cell_data[var_nor[i]] = ~(self.cell_data[var_nor[i]] | self.Bin2Dec(var_nor[i]))
            if var_xnor != 0:
                for i in var_xnor:
                    self.cell_data[var_xnor[i]] = ~(self.cell_data[var_xnor[i]] ^ self.Bin2Dec(var_xnor[i]))
            if var_not != -1:
                for i in var_not:
                    self.cell_data[var_not[i]] = ~self.Bin2Dec(var_not[i])

        elif (plane < 6) & (plane > -1):
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
            logging.error("Couldn't find that plane")
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
        self.cubes.append(self.cube)


        func_dict, ubit_dict, fbit_dict, rbit_dict, lbit_dict, bbit_dict, dbit_dict = LoadCfg(fileLoc)
        self.cube = Cube(func_dict, ubit_dict, fbit_dict, rbit_dict, lbit_dict, bbit_dict, dbit_dict)

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
        if script.count("(") == script.count(")"):
            if script.count(")") == 0:
                logging.warning("Can't find ')', please write it.")
                raise CoreCellCmdError_NO
            else:
                logging.warning("('s count and )'s count are not match, please rewrite it.")
                raise CoreCellCmdError_COUNT
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
                self.cube.Input(ord(input_[0])) #첫 번째 글자 추출 후 아스키 코드로 변환함(한 글자밖에 받을 수 없음)

            elif s_word == 'P': #print
                logging.info("%s : Output -> %s"%(s_word, input_[0]))
                if self.c_ascii: result += chr(self.cube.Output())
                else: result += "%3d "%self.cube.output()

            elif s_word == "X": logging.info("%s: Execute"%s); self.cube.Execute()  #execute

            elif s_word == "*": logging.info("%s: Load"%s); self.cube.Load() #load

            elif s_word == "=": logging.info("%s: Save"%s); self.cube.Save() #save

            elif s_word == "C": logging.info("%s: Clear"%s); self.cube.Clear() #clear

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

            script_index += 1

            if self.c_cube:
                self.cube.Show() #보여주는 거 작성하는 함수는 아직

        logging.info('\n\n')
        return result
        pass
