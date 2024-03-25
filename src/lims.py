class Lims:
    def __init__(self, lims: list[int]):
        self.lims = lims

    '''
    I've done these as functions so that they update after init
    '''
    def down(self, value = None) -> int:
        if isinstance(value, int):
            self.lims[0] = value
        return self.lims[0]
    def right(self, value = None) -> int:
        if isinstance(value, int):
            self.lims[1] = value
        return self.lims[1]
    def up(self, value = None) -> int:
        if isinstance(value, int):
            self.lims[2] = value
        return self.lims[2]
    def left(self, value = None) -> int:
        if isinstance(value, int):
            self.lims[3] = value
        return self.lims[3]

    def __str__(self) -> str:
        return f"down: {str(self.down())}\n"\
            f"right: {str(self.right())}\n"\
            f"up: {str(self.up())}\n"\
            f"left: {str(self.left())}\n"
