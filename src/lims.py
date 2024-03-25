class Lims:
    def __init__(self, lims: list[int]):
        self.lims = lims

    '''
    I've done these as functions so that they update after init
    '''

    @property
    def down(self):
        return self.lims[0]

    @down.setter
    def down(self, value):
        self.lims[0] = value

    @property
    def right(self):
        return self.lims[1]

    @right.setter
    def right(self, value):
        self.lims[1] = value

    @property
    def up(self):
        return self.lims[2]

    @up.setter
    def up(self, value):
        self.lims[2] = value

    @property
    def left(self):
        return self.lims[3]

    @left.setter
    def left(self, value):
        self.lims[3] = value

    def __str__(self) -> str:
        return f"down: {str(self.down)}\n"\
            f"right: {str(self.right)}\n"\
            f"up: {str(self.up)}\n"\
            f"left: {str(self.left)}\n"
