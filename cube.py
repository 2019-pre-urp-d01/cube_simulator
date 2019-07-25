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
    def bit2dec(self, plane):
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
    def Save(self, plane=0):
        if plane == 0:
            for i in range(6):
                self.cell_data[i] = self.bit2dec(i)
        elif plane < 6:
            self.cell_data[plane] = self.bit2dec(plane)
        else:
            logging.error("Couldn't find that plane")
            return None

    # Load data cell to bit cell
    def Load(self, plane=-1):
        pass

    # Clear every cell to initial state
    def Clear(self, plane=-1):
        pass

    # Execute cell
    def Execute(self, plane=-1):
        pass

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
