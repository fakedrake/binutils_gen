class ISAError(Exception):
    def __init__(self, str):
        super(ISAError, self).__init__(str)

class BinutilGenError(Exception):
    def __init__(self, str):
        super(BinutilGenError, self).__init__(str)
