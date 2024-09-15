from fractions import Fraction
from typing import Self, List, Tuple
from pathlib import PurePath
from xml.dom import minidom as md

class frac:
    """
        frac()
        Things:
        * frac + frac
        * frac - frac
        * frac * frac
        * frac / frac
        * len(frac)
        * frac == frac
        * int
    """
    def __init__(self, Numerator, Denominator):
        """
            ### Make a new Fraction Class

            <hr>

            # frac()
            Things:
            * frac + frac
            * frac - frac
            * frac * frac
            * frac / frac
            * len(frac)
            * frac == frac
            * int(frac)
            * frac

            :param Numerator:
            ### The Numerator or the number over the other number

            :param Denominator:
            ### The Denominator or the other number over the number
        """
        self.numerator = Numerator
        self.denominator = Denominator
        self.frac = Fraction(self.numerator, self.denominator)
    def __mul__(self, other : Self):
        return self.frac * other.frac
    def __add__(self, other : Self):
        return self.frac + other.frac
    def __truediv__(self, other : Self):
        return self.frac / other.frac
    def __sub__(self, other : Self):
        return self.frac - other.frac
    def __eq__(self, other : Self):
        if self.frac == other.frac:
            return True
        elif self.denominator == other.numerator and self.numerator == other.denominator:
            return True
        else:
            return False
    def __int__(self):
        return self.denominator + self.numerator
    def __repr__(self):
        return self.frac
def load_xml(file: PurePath) -> List[Tuple[int, int]]:
    """
        Load a xml file that has \\<frac\\>\\</frac\\> tags with \\<numerator\\>\\</numerator\\> and \\<dominator\\>\\</dominator\\> tags<hr>
        Returns a list of fraction tuples
    """
    dom = md.parse(file)

    fracs = dom.getElementsByTagName('frac')
    fracl = []
    for frac in fracs:
        numerator = frac.getElementsByTagName('numerator')[0].childNodes[0].nodeValue
        dominator = frac.getElementsByTagName('dominator')[0].childNodes[0].nodeValue
        fracl.append((numerator, dominator))
    return fracl