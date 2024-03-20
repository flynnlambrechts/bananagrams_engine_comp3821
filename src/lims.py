class Lims:
    def __init__(self, lims: list[int]):
        self.down = lims[0]
        self.right = lims[1]
        self.up = lims[2]
        self.left = lims[3]
        self.lims = lims

    def __str__(self) -> str:
        return f"down: {str(self.down)}\n"\
            f"right: {str(self.right)}\n"\
            f"up: {str(self.up)}\n"\
            f"left: {str(self.left)}\n"
