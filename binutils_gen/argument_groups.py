class ArgGroup(object):
    """ An argument type group.
    """

    def __init__(self, name, predicate=lambda at: True, hard_predicate="0"):
        """Given the name and a predicate to match the types that are part of
        the group. Only the ones with arg_type defined are
        considered. Hard predicate is a predicate that is directly
        passed down if no arguments were found.

        """
        self.name = name
        self.predicate = lambda at: predicate(at) and at.arg_type is not None
        self.hard_predicate = hard_predicate


    def types(self, from_types):
        return [t for t in from_types if self.predicate(t)]
