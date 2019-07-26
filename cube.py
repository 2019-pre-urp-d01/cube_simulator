import logging
import numpy as np

class Cube:
    # Cube initialization
    def __init__(self):
        self.hyper_in  = None
        self.hyper_out = None

        # Cell's function of each cell
        self.cell_function_dict = {0:"Input", 1:"One", 2:"Not", 3:"Or", 4:"And", 5:"Output"}
        self.initial_location = self.cell_fucton_dict.keys()
        self.cell_function = self.cell_function_dict.values()

        self.cell_data = [0]*6
        self.cell_bit  = [[0]*8]*6
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

        # Read available actions and create a List
        self.available_action = []
        for txt_ind, txt_ln in enumerate(self.setup_file):
            # txt_ind = 40
            # while txt_ln[2] == "=":
                # action = txt_ln[4:]
                # available_action.append(action)
                # txt_ind += 1
            pass

        # Change cell's function if set-up actions are not blank
        for i in raw_plane:
            if len(raw_plane[i]) < 5: pass
            else: self.cell_function_dict[i] = raw_plane[i][4:]
        self.cell_function = self.cell_function_dict.values()

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
            logging.error("Couldn't find input plane")
            return None
        self.cell_data[plane] = val

    # Return value from output plane's data cell
    def Output(self):
        plane = self.FindPlane("Output")
        if plane == -1:
            logging.error("Couldn't find output plane")
            return None
        return self.cell_data[plane]

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
        self.cube = Cube()
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
