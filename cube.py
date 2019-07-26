import logging
import numpy as np

rotate_list = ["U", "D", "L", "R", "F", "B", "u", "d", "l", "r", "f", "b", "M", "S", "E"]
index_list = ["0", "1", "2", "3", "4", "5", "6"]

class Cube:
    # Cube initialization
    def __init__(self):
        self.hyper_in  = None
        self.hyper_out = None #Cubes에서 이용할 하이퍼인, 하이퍼아웃

        #Cell's function of each cell
        self.cell_function = ["Input","One","Not","Or","And","Output"]
        self.initial_location = [0, 0, 0, 0, 0, 0]

        self.cell_data = [0]*6
        self.cell_bit  = [[0]*8]*6
        self.cell_core = 0

    # Convert Bit Cells' binary to Data Cell's Demical
    def Bit2Dec(self, plane):
        dec = 0
        for bitnum in range(8):
            dec += self.cell_bit[plane][bitnum] << bitnum
        return dec

    # Find corresponding Plane
    def FindPlane(self, inp):
        for ind, val in enumerate(self.cell_function):
            if val==inp:
                return ind
        return -1

    # Set Static 1 Cell's value to 1
    def StaticOne(self):
        planenum = self.FindPlane("One")
        self.cell_data[planenum] = 1

    # Store input value to input plane's data cell
    def Input(self, val):
        plane = self.FindPlane("Input")
        if plane == -1:
            logging.error("error: Couldn't find input plane")
            return None
        self.cell_data[plane] = val

    # Return value from output plane's data cell
    def Output(self):
        plane = self.FindPlane("Output")
        if plane == -1:
            logging.error("error: Couldn't find output plane")
            return None
        return self.cell_data[plane]

    # Save bit cell to data cell
    def Save(self, plane=-1):
        if plane == -1:
            for i in range(6):
                self.cell_data[i] = self.Bit2Dec(i)
        elif plane < 6:
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
        elif plane < 6:
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
        elif plane < 6:
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

            

            
