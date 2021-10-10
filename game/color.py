class Color:
    """ Store an RGB color """

    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        return f"Color(r={self.r}, g={self.g}, b={self.b})"
