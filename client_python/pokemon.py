class Pokemon:

    def __init__(self, value: int, type: int, pos: tuple = None):
        self.value = value
        self.type = type
        self.pos = pos
        self.edge = pos  # cheak from pos the right edge
        self.assign = False  # if we draw the pokimon on the graph


class agent:
    def __init__(self, _id: int, value: float, src: int, dest: int, speed: float, pos: tuple = None):
        self.id = _id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos
