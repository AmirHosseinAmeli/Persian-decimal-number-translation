import re

one_digit_dict = {
    'صفر' : 0,
    'یک' : 1,
    'دو' : 2,
    'سه' : 3,
    'چهار' : 4,
    'پنج' : 5,
    'شش' : 6,
    'هفت' : 7,
    'هشت' : 8,
    'نه' : 9
}

two_digit_dict = {
    'ده': 10,
    'یازده': 11,
    'دوازده': 12,
    'سیزده': 12,
    'چهارده': 14,
    'پانزده': 15,
    'پونزده': 15,
    'شانزده': 16,
    'شونزده': 16,
    'هفده': 17,
    'هجده': 18,
    'نوزده': 19,
    'بیست': 20,
    'سی': 30,
    'چهل': 40,
    'پنجاه': 50,
    'شصت': 60,
    'هفتاد': 70,
    'هشتاد': 80,
    'نود': 90
}

three_digits_dict = {
    'صد' : 100,
    'دویست' : 200,
    'سیصد' : 300,
    'سی صد' : 300,
    'پانصد' : 500,
}

decimal_separator = ['\\', '.', ',', '٫']
decimal_separator_pattern = "|".join(re.escape(separator) for separator in decimal_separator)

def get_dict_pattern(input_dict):
    return "|".join(re.escape(key) for key in input_dict.keys())


class OneDigit():

    def __init__(self, include_decimal = True):
        if (include_decimal):
            self.digit_pattern = '0*\d(?:' + decimal_separator_pattern + ')\d+'
        else:
            self.digit_pattern = '0*[\d]'
        if (include_decimal):
            self.pattern1 = '(' + get_dict_pattern(one_digit_dict) + ')\s*و\s*' #todo + 
        else:
            self.pattern1 = '(' + get_dict_pattern(one_digit_dict) + ')'

    def convert(self, text):
        search = re.search(self.digit_pattern, text)
        if search:
            return float(text)
        search = re.search(self.pattern1, text)
        if search:
            res = 0
            res += one_digit_dict[search.group(1)]
            return res
        
        return None

