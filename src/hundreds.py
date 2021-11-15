import re

from decimal_group import DecimalGroup
from two_digits import TwoDigits
from unity import Unity


class Hundreds(DecimalGroup):
    instance = None

    @staticmethod
    def get_instance():
        if not Hundreds.instance:
            Hundreds.instance = Hundreds()
        return Hundreds.instance

    def __init__(self):
        self.unity = Unity.get_instance()
        self.two_digits = TwoDigits.get_instance()
        unity_pats = self.aggregate_pats({k: self.unity.pat_map[k] for k in [1, 4, 6, 7, 8, 9]})
        cap_alphabet_pats = '(?:(' + unity_pats + ')\s*@hundreds.1|(@hundreds.1|@hundreds.2|@hundreds.3|@hundreds.5))' + \
                            '(?:\s*@and\s*(' + self.two_digits.related_pats() + '))?'
        ncap_alphabet_pats = '(?:(' + unity_pats + ')\s*@hundreds.1|(?:@hundreds.1|@hundreds.2|@hundreds.3|@hundreds.5))' + \
                             '(?:\s*@and\s*(?:' + self.two_digits.related_pats() + '))?'
        self.cap_alphabet_pats = DecimalGroup.var_subs.compile_vars(cap_alphabet_pats)
        self.ncap_alphabet_pats = DecimalGroup.var_subs.compile_vars(ncap_alphabet_pats)
        self.w2n_dict = {DecimalGroup.var_subs.compile_vars('@hundreds.' + str(i)): 100 * i for i in [1, 2, 3, 5]}
        self.cap_numeric_pats = DecimalGroup.var_subs.compile_vars(
            '([' + DecimalGroup.dig_pats + '])([' + DecimalGroup.dig_pats + ']{2})')
        self.ncap_numeric_pats = '[' + DecimalGroup.dig_pats + ']{3}'

    def w2n(self, word):
        suc = re.search(self.cap_alphabet_pats, word)
        if suc:
            res = 0
            if suc.group(1):
                res = 100 * self.unity.w2n(suc.group(1))
            elif suc.group(2):
                res = self.w2n_dict[suc.group(2)]
            if suc.group(3):
                res += self.two_digits.w2n(suc.group(3))
            return res
        suc = re.search(self.cap_numeric_pats, word)
        if suc:
            return 100 * self.unity.w2n(suc.group(1)) + self.two_digits.w2n(suc.group(2))
        return self.two_digits.w2n(word)

    def related_pats(self):
        return '(?:' + self.ncap_alphabet_pats + ')|(?:' + \
               self.ncap_numeric_pats + ')|(?:' + self.two_digits.related_pats() + ')'
