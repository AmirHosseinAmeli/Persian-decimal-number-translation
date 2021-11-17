import re

from decimal_group import DecimalGroup
from unity import Unity


class TwoDigits(DecimalGroup):
    instance = None

    @staticmethod
    def get_instance():
        if not TwoDigits.instance:
            TwoDigits.instance = TwoDigits()
        return TwoDigits.instance

    def __init__(self):
        self.unity = Unity.get_instance()
        self.teen_n2pats = {10 + i: [DecimalGroup.var_subs.compile_vars('(@2dig.' + str(10 + i)) + ')'] for i in
                                range(10)}
        self.teen_w2n = {DecimalGroup.var_subs.compile_vars('@2dig.' + str(10 + i)): 10 + i for i in range(10)}
        unity_pats = self.aggregate_pats({k: self.unity.pat_map[k] for k in range(1, 10)})  # excluding zero
        self.tenth_alphabet = DecimalGroup.var_subs.compile_vars('(@2dig.20' + ''.join(
            ['|@2dig.' + str(i) for i in range(30, 100, 10)]) + ')(?:\s*@and\s*(' + unity_pats + '))?')
        self.w2tenth = {DecimalGroup.var_subs.compile_vars('@2dig.' + str(i)): i for i in range(10, 100, 10)}
        self.tenth_num = '([\d])([\d])'

    def w2n(self, word):
        suc = re.search(self.aggregate_pats(self.teen_n2pats), word)
        if suc:
            return self.teen_w2n[suc.group()]
        suc = re.search(self.tenth_alphabet, word)
        if suc:
            res = self.w2tenth[suc.group(1)]
            if suc.group(2):
                res += self.unity.w2n(suc.group(2))
            return res
        suc = re.search(self.tenth_num, word)
        if suc:
            return 10 * self.unity.w2n(suc.group(1)) + self.unity.w2n(suc.group(2))
        return self.unity.w2n(word)

    def _capturing_pats(self):
        return '(?:' + self.aggregate_pats(self.teen_n2pats) + ')|(?:' + self.tenth_alphabet + ')|(?:' + \
               self.tenth_num + ')|(?:' + self.unity.non_capturing_pats() + ')'
