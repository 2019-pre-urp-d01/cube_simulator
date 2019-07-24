
class Cube:
    # Cube initialization
    def __init__(self):
        self.hyper_in  = None
        self.hyper_out = None

        # Cell's function of each cell
        self.cell_func = ["Input","One","Not","Or","And","Output"]

        self.cell_data = [0]*6
        self.cell_bit  = [[0]*8]*6
        self.cell_core = 0

    # Store input value to input plane's data cell
    def Input(self, val):
        pass

    # Return value to input plane's data cell
    def Output(self):
        return -1

    # Save bit cell to data cell
    def Save(self, plane=-1):
        pass
    
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