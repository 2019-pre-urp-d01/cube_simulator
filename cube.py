import logging
import numpy as np

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
        self.hyper_out = None

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
<<<<<<< HEAD
<<<<<<< Updated upstream
        return self.cell_data[plane]
=======
        elif len(plane) > 1:
            logging.error("Nonsense cube; more than one output cell")
        return self.cell_data[plane[0]]
>>>>>>> Stashed changes
=======
        elif len(plane) > 1:
            logging.error("Nonsense cube; more than one output cell")
        return self.cell_data[p]
>>>>>>> 12f636e0bdd3711413b81cb6a050dbc47ab10b14

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
                for bitnum in range(8):
                    self.cell_bit[i][bitnum] = (self.cell_data[i] >> bitnum) & 1
        elif (plane < 6) & (plane > -1):
            for bitnum in range(8):
                self.cell_bit[plane][bitnum] = (self.cell_data[plane] >> bitnum) & 1
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

<<<<<<< Updated upstream
        elif plane < 6:
<<<<<<< HEAD
            if self.cell_function[plane] = "Input" or "Output" or "One":
                break
            elif self.cell_function[plane] = "And":
=======
        elif (plane < 6) & (plane > -1):
            if self.cell_function[plane] == "Input" or "Output" or "One":
                pass
            elif self.cell_function[plane] == "And":
>>>>>>> Stashed changes
=======
            if self.cell_function[plane] == "Input" or "Output" or "One":
                pass
            elif self.cell_function[plane] == "And":
>>>>>>> 12f636e0bdd3711413b81cb6a050dbc47ab10b14
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
    def __init__(self, config=dict()):

        # List of cubes
        self.cubes = list()
        # Generate One cube
        func_dict, ubit_dict, fbit_dict, rbit_dict, lbit_dict, bbit_dict, dbit_dict = LoadCfg(fileLoc)
        self.cube = Cube(func_dict)
        self.cubes.append(self.cube)

    # Create one cube, and set pointers
    def CreateCubeOnDirection(self, direction="in"):
        pass

    # Exectue one command
    def Execute(self, command):
        pass

    # Execute Commands
    def ExecuteCommands(self, commands):
        pass
