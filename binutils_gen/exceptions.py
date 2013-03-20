class ISAError(Exception):
    def __init__(self, str):
        super(ISAError, self).__init__(str)
