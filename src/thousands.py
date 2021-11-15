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
        cap_alphabet_pats = '(' + self.hundred.related_pats() + ')\s*@thousand(?:\s*@and\s*(' + self.hundred.related_pats() + '))?'
        ncap_alphabet_pats = self.hundred.related_pats() + '\s*@thousand(?:\s*@and\s*' + self.hundred.related_pats() + ')?'
        self.cap_alphabet_pats = DecimalGroup.var_subs.compile_vars(cap_alphabet_pats)
        self.ncap_alphabet_pats = DecimalGroup.var_subs.compile_vars(ncap_alphabet_pats)
        self.cap_numeric_pats = DecimalGroup.var_subs.compile_vars(
            '([' + DecimalGroup.dig_pats + ']{1,3})([' + DecimalGroup.dig_pats + ']{3})')
        self.ncap_numeric_pats = DecimalGroup.var_subs.compile_vars('[' + DecimalGroup.dig_pats + ']{4,6}')

