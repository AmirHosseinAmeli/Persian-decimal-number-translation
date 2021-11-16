import re

from decimal_group import DecimalGroup
from hundreds import Hundreds
from unity import Unity


class Thousand(DecimalGroup):
    instance = None

    @staticmethod
    def get_instance():
        if not Thousand.instance:
            Thousand.instance = Thousand()
        return Thousand.instance

    def __init__(self):
        self.unity = Unity.get_instance()
        self.hundred = Hundreds.get_instance()
        alphabet_pats = '(' + self.hundred.non_capturing_pats() + ')?\s*@thousand(?:\s*@and\s*(' + self.hundred.non_capturing_pats() + '))?'
        self.alphabet_pats = DecimalGroup.var_subs.compile_vars(alphabet_pats)
        self.numeric_pats = DecimalGroup.var_subs.compile_vars(
            '([' + DecimalGroup.dig_pats + ']{1,3})([' + DecimalGroup.dig_pats + ']{3})')

    def w2n(self, word):
        suc = re.search(self.alphabet_pats, word)
        if suc:
            res = 1000 if not suc.group(1) else 1000 * self.hundred.w2n(suc.group(1))
            res += 0 if not suc.group(2) else self.hundred.w2n(suc.group(2))
            return res
        suc = re.search(self.numeric_pats, word)
        if suc:
            return 1000 * self.hundred.w2n(suc.group(1)) + self.hundred.w2n(suc.group(2))
        return self.hundred.w2n(word)



    def _capturing_pats(self):
        return '(?:' + self.alphabet_pats + ')|(?:' + self.alphabet_pats + \
               ')|(?:' + self.numeric_pats + ')|(?:' + self.hundred.non_capturing_pats() + ')'

