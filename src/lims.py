class Lims:
    def __init__(self, lims: list[int]):
        self.lims = lims

    '''
    I've done these as functions so that they update after init
    '''
    def down(self) -> int:
        return self.lims[0]
    def right(self) -> int:
        return self.lims[1]
    def up(self) -> int:
        return self.lims[2]
    def left(self) -> int:
        return self.lims[3]

    def __str__(self) -> str:
        return f"down: {str(self.down())}\n"\
            f"right: {str(self.right())}\n"\
            f"up: {str(self.up())}\n"\
            f"left: {str(self.left())}\n"
