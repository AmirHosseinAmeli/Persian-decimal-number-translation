import re

persian_alphabet = ['ش', 'س', 'ی', 'ب', 'ل', 'ا', 'ت', 'ن', 'م', 'ک', 'گ', 'ض', 'ص', 'ث', 'ق', 'ف', 'غ', 'ع', 'ه',
'خ', 'ح', 'ج', 'چ', 'ظ', 'ط', 'ز', 'ر', 'ذ', 'ر', 'ذ', 'د', 'ئ', 'و', 'پ', 'ژ', 'آ']

decimal_dict = {
    'دهم' : 0.1,
    'صدم' : 0.01,
    'هزارم' : 0.001
}

decimal_exceptional_dict = {
    'نیم' : 0.5
}

one_digit_dict = {
    'صفر' : 0.,
    'یک' : 1.,
    'دو' : 2.,
    'سه' : 3.,
    'چهار' : 4.,
    'پنج' : 5.,
    'شش' : 6.,
    'هفت' : 7.,
    'هشت' : .8,
    'نه' : 9.
}

two_digit_dict1 = {
    'ده': 10.,
    'یازده': 11.,
    'دوازده': 12.,
    'سیزده': 13.,
    'چهارده': 14.,
    'پانزده': 15.,
    'پونزده': 15.,
    'شانزده': 16.,
    'شونزده': 16.,
    'هفده': 17.,
    'هجده': 18.,
    'نوزده': 19.
}

two_digit_dict2 = {
    'بیست': 20.,
    'سی': 30.,
    'چهل': 40.,
    'پنجاه': 50.,
    'شصت': 60.,
    'هفتاد': 70.,
    'هشتاد': 80.,
    'نود': 90.
}

three_digits_dict = {
    'صد' : 100.,
    'دویست' : 200.,
    'سیصد' : 300.,
    'پانصد' : 500.,
}

value_list = ['صد', 'هزار', 'میلیون', 'میلیارد']

#decimal separator for numerical part
decimal_separator = ['\\', '.', ',', '٫', '/']
decimal_separator_pattern = "|".join(re.escape(separator) for separator in decimal_separator)

#persian alphabet pattern to avoid mismatching
persian_alphabet_pattern = "|".join(re.escape(alphabet) for alphabet in persian_alphabet)

#get regex pattern of a dictionary by it's keys
def get_dict_pattern(input_dict):
    return "|".join(re.escape(key) for key in input_dict.keys())

#replace capturing group regex with non-capturing regex
def remove_pattern_groups_matching(pattern):
    return re.sub('\((?!\?)', '(?:', pattern)

#convert persian numbers to english ones
def get_normalized_text(text):
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    for i in range(len(persian_digits)):
        text = re.sub(persian_digits[i], english_digits[i], text)

    return text

#class of decimal part of language
class Decimal():

    def __init__(self):
        self.digit_pattern = '(?:' + decimal_separator_pattern + ')\d*'
        self.hundred = Hundred(include_decimal = False)
        #pattern like نیم
        self.pattern1 = '(' + get_dict_pattern(decimal_exceptional_dict) + ')'
        #pattern like دویست صدم
        self.pattern2 = '(' + self.hundred.get_class_patterns() + ')\s*(' + get_dict_pattern(decimal_dict) + ')'

    def convert(self, text):
        search = re.fullmatch(self.pattern1, text)
        if search:
            res = decimal_exceptional_dict[search.group(1)]
            return res
        search = re.fullmatch(self.pattern2, text)
        if search:
            res = decimal_dict[search.group(2)] * self.hundred.convert(search.group(1))
            return res
        return None

    def get_class_patterns(self):
        class_pattern = '(?<!' + persian_alphabet_pattern + ')' + self.pattern1 + \
                            '(?!' + persian_alphabet_pattern + ')'
        class_pattern += '|' + '(?<!' + persian_alphabet_pattern + ')' + self.pattern2 + \
                            '(?!' + persian_alphabet_pattern + ')'
        return remove_pattern_groups_matching(class_pattern)


class OneDigit():

    def __init__(self, include_decimal = True):
        self.include_decimal = include_decimal
        self.digit_pattern = '(0*\d{1})'
        #pattern like یک
        self.pattern1 = '(' + get_dict_pattern(one_digit_dict) + ')'
        self.decimal_suffixes = get_dict_pattern(decimal_exceptional_dict) + '|' + get_dict_pattern(decimal_dict)
        if include_decimal:
            self.decimal = Decimal()
            self.digit_pattern = '(' + remove_pattern_groups_matching(self.digit_pattern) + '(?:' + \
                                    self.decimal.digit_pattern + ')?)'
            self.adding_decimal_pattern = '(?:\s*و\s*(' + self.decimal.get_class_patterns() + '))'
            self.decimal_pattern = '(' + self.decimal.get_class_patterns() + ')'

    def convert(self, text):
        search = re.fullmatch(self.digit_pattern, text)
        if search:
            number = re.sub(decimal_separator_pattern, '.', search.group(1))
            return float(number)
        #first check pattern with decimal if self.include_decimal == True
        if self.include_decimal:
            search = re.fullmatch(self.pattern1 + self.adding_decimal_pattern, text)
            if search:
                res = 0.
                res += one_digit_dict[search.group(1)]
                res += self.decimal.convert(search.group(2))
                return res
        #then check all patterns without decimal part
        search = re.fullmatch(self.pattern1, text)
        if search:
            res = one_digit_dict[search.group(1)]
            return res
        search = re.fullmatch(self.decimal_pattern, text)
        #sublevel pattern check
        if search:
            res = self.decimal.convert(search.group(1))
            return res
        return None

    def get_class_patterns(self):
        class_pattern = self.digit_pattern
        if self.include_decimal:
            class_pattern += '|' + '(?<!' + persian_alphabet_pattern + ')' + self.pattern1 + self.adding_decimal_pattern + \
                            '(?!' + persian_alphabet_pattern + ')'
        class_pattern += '|' + '(?<!' + persian_alphabet_pattern + ')' + self.pattern1 + \
                            ('(?!\s*(?:'+ self.decimal_suffixes + '))' if self.include_decimal else '') + \
                                '(?!' + persian_alphabet_pattern + ')'
        if self.include_decimal:
            class_pattern += '|' + self.decimal_pattern
        return remove_pattern_groups_matching(class_pattern)


class TwoDigit():

    def __init__(self, include_decimal = True):
        self.include_decimal = include_decimal
        self.digit_pattern = '(0*\d{2})'
        self.one_digit = OneDigit(include_decimal = include_decimal)
        #pattern like یازده
        self.pattern1 = '(' + get_dict_pattern(two_digit_dict1) + ')'
        #pattern like پنجاه و دو
        self.pattern2 = '(' + get_dict_pattern(two_digit_dict2) + ')(?:\s*و\s*(' +  self.one_digit.get_class_patterns() + '))?'
        #sublevel patterns in the language hierarchy tree
        self.pattern3 = '(' + self.one_digit.get_class_patterns() + ')'
        self.decimal_suffixes = get_dict_pattern(decimal_exceptional_dict) + '|' + get_dict_pattern(decimal_dict)
        if include_decimal:
            self.decimal = Decimal()
            self.digit_pattern = '(' + remove_pattern_groups_matching(self.digit_pattern) + '(?:' + \
                                    self.decimal.digit_pattern + ')?)'
            self.adding_decimal_pattern = '(?:\s*و\s*(' + self.decimal.get_class_patterns() + '))'
            self.decimal_pattern = '(' + self.decimal.get_class_patterns() + ')'

    def convert(self, text):
        search = re.fullmatch(self.digit_pattern, text)
        if search:
            number = re.sub(decimal_separator_pattern, '.', search.group(1))
            return float(number)
        #first check pattern with decimal if self.include_decimal == True
        if self.include_decimal:
            search = re.fullmatch(self.pattern1 + self.adding_decimal_pattern, text)
            if search: 
                res = 0.
                res += two_digit_dict1[search.group(1)]
                res += self.decimal.convert(search.group(2))
                return res
            search = re.fullmatch(self.pattern2 + self.adding_decimal_pattern, text)
            if search:
                res = 0.
                res += two_digit_dict2[search.group(1)]
                if search.group(2):
                    res += self.one_digit.convert(search.group(2))
                res += self.decimal.convert(search.group(3))
                return res
        #then check all patterns without decimal part
        search = re.fullmatch(self.pattern1, text)
        if search:
            res = two_digit_dict1[search.group(1)]
            return res
        search = re.fullmatch(self.pattern2, text)
        if search:
            res = 0.
            res += two_digit_dict2[search.group(1)]
            if search.group(2):
                res += self.one_digit.convert(search.group(2))
            return res
        #sublevel pattern check
        search = re.fullmatch(self.pattern3, text)
        if search:
            res = self.one_digit.convert(search.group(1))
            return res
        return None

    def get_class_patterns(self):
        class_pattern = self.digit_pattern
        if self.include_decimal:
            class_pattern += '|' + '(?<!' + persian_alphabet_pattern + ')' + self.pattern1 + self.adding_decimal_pattern + \
                            '(?!' + persian_alphabet_pattern + ')'
            class_pattern += '|' + '(?<!' + persian_alphabet_pattern + ')' + self.pattern2 + self.adding_decimal_pattern + \
                            '(?!' + persian_alphabet_pattern + ')'
        class_pattern += '|' + '(?<!' + persian_alphabet_pattern + ')' + self.pattern1 + \
                            ('(?!\s*(?:'+ self.decimal_suffixes + '))' if self.include_decimal else '') + \
                                '(?!' + persian_alphabet_pattern + ')'
        class_pattern += '|' + '(?<!' + persian_alphabet_pattern + ')' + self.pattern2 + \
                            ('(?!\s*(?:'+ self.decimal_suffixes + '))' if self.include_decimal else '') + \
                                '(?!' + persian_alphabet_pattern + ')'
        class_pattern += '|' + self.pattern3
        return remove_pattern_groups_matching(class_pattern)


class Hundred():

    def __init__(self, include_decimal = True):
        self.include_decimal = include_decimal
        self.digit_pattern = '(0*\d{3})'
        self.two_digit = TwoDigit(include_decimal = include_decimal)
        hundred_part = '(?:(' + get_dict_pattern(three_digits_dict) + ')' + \
                        '|(' + self.two_digit.get_class_patterns() + ')\s*' + value_list[0] + ')'
        two_digit_part = '(' + self.two_digit.get_class_patterns() + ')'
        #pattern like صد و بیست و 2
        self.pattern1 = hundred_part + '(?:\s*و\s*' + two_digit_part + ')?'
        #sublevel patterns in the language hierarchy tree
        self.pattern2 = two_digit_part
        self.decimal_suffixes = get_dict_pattern(decimal_exceptional_dict) + '|' + get_dict_pattern(decimal_dict)
        if (include_decimal):
            self.decimal = Decimal()
            self.digit_pattern = '(' + remove_pattern_groups_matching(self.digit_pattern) + '(?:' + \
                                    self.decimal.digit_pattern + ')?)'
            self.adding_decimal_pattern = '(?:\s*و\s*(' + self.decimal.get_class_patterns() + '))'
            self.decimal_pattern = '(' + self.decimal.get_class_patterns() + ')'

    def convert(self, text):
        search = re.fullmatch(self.digit_pattern, text)
        if search:
            number = re.sub(decimal_separator_pattern, '.', search.group(1))
            return float(number)
        #first check pattern with decimal if self.include_decimal == True
        if self.include_decimal:
            search = re.fullmatch(self.pattern1 + self.adding_decimal_pattern, text)
            if search:
                res = 0.
                if search.group(1):
                    res += three_digits_dict[search.group(1)]
                if search.group(2):
                    res += 100 * self.two_digit.convert(search.group(2))
                if search.group(3):
                    res += self.two_digit.convert(search.group(3))
                res += self.decimal.convert(search.group(4))
                return res
        #then check all patterns without decimal part
        search = re.fullmatch(self.pattern1, text)
        if search:
            res = 0.
            if search.group(1):
                res += three_digits_dict[search.group(1)]
            if search.group(2):
                res += 100 * self.two_digit.convert(search.group(2))
            if search.group(3):
                res += self.two_digit.convert(search.group(3))
            return res
        #sublevel pattern check
        search = re.fullmatch(self.pattern2, text)
        if search:
            res = self.two_digit.convert(search.group(1))
            return res
        return None

    def get_class_patterns(self):
        class_pattern = self.digit_pattern
        if self.include_decimal:
            class_pattern += '|' + '(?<!' + persian_alphabet_pattern + ')' + self.pattern1 + self.adding_decimal_pattern + \
                            '(?!' + persian_alphabet_pattern + ')'
        class_pattern += '|' + '(?<!' + persian_alphabet_pattern + ')' + self.pattern1 + \
                            ('(?!\s*(?:'+ self.decimal_suffixes + '))' if self.include_decimal else '') + \
                                '(?!' + persian_alphabet_pattern + ')'
        class_pattern += '|' + self.pattern2
        return remove_pattern_groups_matching(class_pattern)


class Thousand():

    def __init__(self, include_decimal = True):
        self.include_decimal = include_decimal
        self.digit_pattern = '(0*\d{4,6})'
        self.hundred = Hundred(include_decimal = include_decimal)
        thousand_part = '(?:(?:(' + self.hundred.get_class_patterns() + ')\s*)?' + value_list[1] + ')'
        hundred_part = '(' + self.hundred.get_class_patterns() + ')'
        #pattern like 2 هزار و صد و 20
        self.pattern1 = thousand_part + '(?:\s*و\s*' + hundred_part + ')?'
        #sublevel patterns in the language hierarchy tree
        self.pattern2 = hundred_part
        if (include_decimal):
            self.decimal = Decimal()
            self.digit_pattern = '(' + remove_pattern_groups_matching(self.digit_pattern) + '(?:' + \
                                    self.decimal.digit_pattern + ')?)'
            self.adding_decimal_pattern = '(?:\s*و\s*(' + self.decimal.get_class_patterns() + '))'
            self.decimal_pattern = '(' + self.decimal.get_class_patterns() + ')'

    def convert(self, text):
        search = re.fullmatch(self.digit_pattern, text)
        if search:
            number = re.sub(decimal_separator_pattern, '.', search.group(1))
            return float(number)
        #first check pattern with decimal if self.include_decimal == True
        if self.include_decimal:
            search = re.fullmatch(self.pattern1 + self.adding_decimal_pattern, text)
            if search:
                res = 1000.
                if search.group(1):
                    res = 1000. * self.hundred.convert(search.group(1))
                if search.group(2):
                    res += self.hundred.convert(search.group(2))
                res += self.decimal.convert(search.group(3))
                return res
        #then check all patterns without decimal part
        search = re.fullmatch(self.pattern1, text)
        if search:
            res = 1000.
            if search.group(1):
                res = 1000. * self.hundred.convert(search.group(1))
            if search.group(2):
                res += self.hundred.convert(search.group(2))
            return res
        #sublevel pattern check
        search = re.fullmatch(self.pattern2, text)
        if search:
            res = self.hundred.convert(search.group(1))
            return res
        return None

    def get_class_patterns(self):
        class_pattern = self.digit_pattern
        if self.include_decimal:
            class_pattern += '|' + '(?<!' + persian_alphabet_pattern + ')' + self.pattern1 + self.adding_decimal_pattern + \
                            '(?!' + persian_alphabet_pattern + ')'
        class_pattern += '|' + '(?<!' + persian_alphabet_pattern + ')' + self.pattern1 + \
                            '(?!' + persian_alphabet_pattern + ')'
        class_pattern += '|' + self.pattern2
        return remove_pattern_groups_matching(class_pattern)

class Million():

    def __init__(self, include_decimal = True):
        self.include_decimal = include_decimal
        self.digit_pattern = '(0*\d{7,9})'
        self.thousand = Thousand(include_decimal = include_decimal)
        million_part = '(?:(' + self.thousand.get_class_patterns() + ')\s*' + value_list[2] + ')'
        thousand_part = '(' + self.thousand.get_class_patterns() + ')'
        #pattern like دویست میلیون و 100 هزار
        self.pattern1 = million_part + '(?:\s*و\s*' + thousand_part + ')?'
        #sublevel patterns in the language hierarchy tree
        self.pattern2 = thousand_part
        if (include_decimal):
            self.decimal = Decimal()
            self.digit_pattern = '(' + remove_pattern_groups_matching(self.digit_pattern) + '(?:' + \
                                    self.decimal.digit_pattern + ')?)'
            self.adding_decimal_pattern = '(?:\s*و\s*(' + self.decimal.get_class_patterns() + '))'
            self.decimal_pattern = '(' + self.decimal.get_class_patterns() + ')'

    def convert(self, text):
        search = re.fullmatch(self.digit_pattern, text)
        if search:
            number = re.sub(decimal_separator_pattern, '.', search.group(1))
            return float(number)
        #first check pattern with decimal if self.include_decimal == True
        if self.include_decimal:
            search = re.fullmatch(self.pattern1 + self.adding_decimal_pattern, text)
            if search:
                res = 0.
                if search.group(1):
                    res += 1e6 * self.thousand.convert(search.group(1))
                if search.group(2):
                    res += self.thousand.convert(search.group(2))
                res += self.decimal.convert(search.group(3))
                return res
        #then check all patterns without decimal part
        search = re.fullmatch(self.pattern1, text)
        if search:
            res = 0.
            if search.group(1):
                res += 1e6 * self.thousand.convert(search.group(1))
            if search.group(2):
                res += self.thousand.convert(search.group(2))
            return res
        #sublevel pattern check
        search = re.fullmatch(self.pattern2, text)
        if search:
            res = self.thousand.convert(search.group(1))
            return res
        return None

    def get_class_patterns(self):
        class_pattern = self.digit_pattern
        if self.include_decimal:
            class_pattern += '|' + '(?<!' + persian_alphabet_pattern + ')' + self.pattern1 + self.adding_decimal_pattern + \
                            '(?!' + persian_alphabet_pattern + ')'
        class_pattern += '|' + '(?<!' + persian_alphabet_pattern + ')' + self.pattern1 + \
                            '(?!' + persian_alphabet_pattern + ')'
        class_pattern += '|' + self.pattern2
        return remove_pattern_groups_matching(class_pattern)

class Billion():

    def __init__(self, include_decimal = True):
        self.include_decimal = include_decimal
        self.digit_pattern = '(0*\d{10,12})'
        self.million = Million(include_decimal = include_decimal)
        billion_part = '(?:(' + self.million.get_class_patterns() + ')\s*' + value_list[3] + ')'
        million_part = '(' + self.million.get_class_patterns() + ')'
        #pattern like دویست هزار میلیارد و یک
        self.pattern1 = billion_part + '(?:\s*و\s*' + million_part + ')?'
        #sublevel patterns in the language hierarchy tree
        self.pattern2 = million_part
        if (include_decimal):
            self.decimal = Decimal()
            self.digit_pattern = '(' + remove_pattern_groups_matching(self.digit_pattern) + '(?:' + \
                                    self.decimal.digit_pattern + ')?)'
            self.adding_decimal_pattern = '(?:\s*و\s*(' + self.decimal.get_class_patterns() + '))'
            self.decimal_pattern = '(' + self.decimal.get_class_patterns() + ')'

    def convert(self, text):
        search = re.fullmatch(self.digit_pattern, text)
        if search:
            number = re.sub(decimal_separator_pattern, '.', search.group(1))
            return float(number)
        #first check pattern with decimal if self.include_decimal == True
        if self.include_decimal:
            search = re.fullmatch(self.pattern1 + self.adding_decimal_pattern, text)
            if search:
                res = 0.
                if search.group(1):
                    res += 1e9 * self.million.convert(search.group(1))
                if search.group(2):
                    res += self.million.convert(search.group(2))
                res += self.decimal.convert(search.group(3))
                return res
        #then check all patterns without decimal part
        search = re.fullmatch(self.pattern1, text)
        if search:
            res = 0.
            if search.group(1):
                res += 1e9 * self.million.convert(search.group(1))
            if search.group(2):
                res += self.million.convert(search.group(2))
            return res
        #sublevel pattern check
        search = re.fullmatch(self.pattern2, text)
        if search:
            res = self.million.convert(search.group(1))
            return res
        return None

    def get_class_patterns(self):
        class_pattern = self.digit_pattern
        if self.include_decimal:
            class_pattern += '|' + '(?<!' + persian_alphabet_pattern + ')' + self.pattern1 + self.adding_decimal_pattern + \
                                '(?!' + persian_alphabet_pattern + ')'
        class_pattern += '|' + '(?<!' + persian_alphabet_pattern + ')' + self.pattern1 + \
                            '(?!' + persian_alphabet_pattern + ')'
        class_pattern += '|' + self.pattern2
        return remove_pattern_groups_matching(class_pattern)


def number_extractor(text):
    output = []
    number_class = Billion()
    whole_pattern = '(' + number_class.get_class_patterns() + ')'
    text = get_normalized_text(text)
    matched_patterns = re.finditer(whole_pattern, text)

    for matched_pattern in matched_patterns:
        matched_text = matched_pattern.group(1)
        number = number_class.convert(matched_text)
        output.append(
            {
                'phrase' : matched_text,
                'value' : number
            }
        )

    return output
