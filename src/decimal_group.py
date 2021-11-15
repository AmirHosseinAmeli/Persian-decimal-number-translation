import operator
from abc import ABC, abstractmethod
from functools import reduce

from config_variable_substitutor import ConfigVariableSumbstitutor


class DecimalGroup(ABC):

  pers_digs = '۰۱۲۳۴۵۶۷۸۹'
  var_subs = ConfigVariableSumbstitutor.get_instance()
  dig_pats = pers_digs + ''.join(str(i) for i in range(10))

  @abstractmethod
  def w2n(self, word):
    pass

  @abstractmethod
  def related_pats(self):
    pass

  @staticmethod
  def aggregate_pats(num2pats_dict):
    pats = reduce(operator.iconcat, num2pats_dict.values(), [])
    if len(pats) > 0:
      return reduce(lambda a, b: a + '|' + b, pats[1:], pats[0])
    return ''
