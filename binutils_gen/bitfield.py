import re

class WorkFlow(object):
    def __init__(self, states):
        """Be sure not to add a None state"""
        self.states = states
        self.it = iter(self.states)
        self.item = None
        self.current = next(self.it, None)

    def next(self, stay=None):
        """Update unless the current state is `stay`"""
        if stay is not None and self.current not in stay:
            self.current = next(self.it, None)

    def finished(self):
        return self.current is None

class ParametricBitfield(object):
    """A bitfield that can support variable bits"""
    def __init__(self, string, length=None):
        self.string = ""
        self.append(string, length)

    def __int__(self):
        """Make a usable int out of this. All parametrics or non-1
        digits are ignored."""
        return self.integral_mask('1')

    def __contains__(self, c):
        return c in self.string

    def integral_mask(self, regex):
        ret = 0
        for s,c in enumerate(reversed(self.string)):
            if re.match(regex, c):
                ret |= 1<<s

        return ret

    def mask(self, regex='\d'):
        """Get parametric bitfield with the characters that match
        regex set"""
        return ParametricBitfield(self.integral_mask(regex))

    def ones(self, warn_nonconsecutive=True):
        ret = 0
        wf = WorkFlow(['scanning', 'reading', 'checking_rest'])
        for i in self.string:
            if i == '1':
                wf.next(stay=['reading'])
                ret += 1
            else:
                wf.next(stay=['scanning', 'checking_rest'])

            if wf.finished():
                warnings.warn('fragmented mask')

        return ret

    def symbols(self, non_parameters=['1', '0', 'x']):
        """Return a frozenset of the parameters."""
        return frozenset([i for i in self.string if i not in non_parameters])

    def __eq__(self, target):
        """If a parametric bitfield can with certain parameters become
        another the two are equal. Also this fails if they have
        different sizes"""
        if len(self.string) != len( str(target)):
            return False

        for x,y in zip(self.string, str(target)):
            if x in ['0', '1'] and y in ['0', '1'] and x != y:
                return False

        return True


    def append(self, x, length=None, force_string=False):
        """Append the string or integer x to the bitfield. If length
        is a positive integer we keep only the last `length`
        bits/characters. If force string is true we do not try to
        convert x to an int before appending. This is useful in case
        we are pushing a binary of binaries."""

        if not force_string:
            try:
                s = bin(int(x))[2:]
            except ValueError:
                s = x

        else:
            s = x

        if length and length > 0:
            if length > len(s):
                s = length*'0'+s

            self.string += s[-length:]
        else:
            self.string += s

    def __add__(self, string):
        """Append these bits to the bitfield"""
        self.append(string)

    def __str__(self):
        """Return how the bitfield looks"""
        return self.string

    def mismatches(self, expected_symbols):
        """Return a tuple of the (unexpected, unfound)."""
        return frozenset(expected_symbols - self.symbols()), frozenset(self.symbols() - expected_symbols)
