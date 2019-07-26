import logging
import numpy as np

class Cube:
    # Cube initialization
    def __init__(self):
        self.hyper_in  = None
        self.hyper_out = None

        # Cell's function of each cell
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
            logging.error("Couldn't find input plane")
            return None
        self.cell_data[plane] = val

    # Return value from output plane's data cell
    def Output(self):
        plane = self.FindPlane("Output")
        if plane == -1:
            logging.error("Couldn't find output plane")
            return None
<<<<<<< Updated upstream
        return self.cell_data[plane]
=======
        elif len(plane) > 1:
            logging.error("Nonsense cube; more than one output cell")
        return self.cell_data[plane[0]]
>>>>>>> Stashed changes

    # Save bit cell to data cell
    def Save(self, plane=-1):
        if plane == -1:
            for i in range(6):
                self.cell_data[i] = self.Bit2Dec(i)
        elif plane < 6:
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
        elif plane < 6:
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
        elif plane < 6:
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
            if self.cell_function[plane] = "Input" or "Output" or "One":
                break
            elif self.cell_function[plane] = "And":
=======
        elif (plane < 6) & (plane > -1):
            if self.cell_function[plane] == "Input" or "Output" or "One":
                pass
            elif self.cell_function[plane] == "And":
>>>>>>> Stashed changes
                self.cell_data[plane] = self.cell_data[plane] & self.Bin2Dec(plane)
            elif self.cell_function[plane] = "Or":
                self.cell_data[plane] = self.cell_data[plane] | self.Bin2Dec(plane)
            elif self.cell_function[plane] = "Xor":
                self.cell_data[plane] = self.cell_data[plane] ^ self.Bin2Dec(plane)
            elif self.cell_function[plane] = "Nand":
                self.cell_data[plane] = ~(self.cell_data[plane] & self.Bin2Dec(plane))
            elif self.cell_function[plane] = "Nor":
                self.cell_data[plane] = ~(self.cell_data[plane] | self.Bin2Dec(plane))
            elif self.cell_function[plane] = "Xnor":
                self.cell_data[plane] = ~(self.cell_data[plane] ^ self.Bin2Dec(plane))
            elif self.cell_function[plane] = "Not":
                self.cell_data[plane] = ~self.Bin2Dec(plane)

        else:
            logging.error("Couldn't find that plane")
            return None

    # Rotate cube
    def Rotate(self):
        pass

class Cells:
    def __init__(self,      ):
        

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
