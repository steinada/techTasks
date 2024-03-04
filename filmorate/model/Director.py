class Director:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def __eq__(self, other):
        super().__eq__(other)
        return self.id == other.id

    def __hash__(self):
        return hash((self.id, self.name))
