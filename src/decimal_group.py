import operator
import re
from abc import ABC, abstractmethod
from functools import reduce

from config_variable_substitutor import ConfigVariableSumbstitutor


class DecimalGroup(ABC):

  var_subs = ConfigVariableSumbstitutor.get_instance()

  @abstractmethod
  def w2n(self, word):
    pass

  @abstractmethod
  def _capturing_pats(self):
    pass

  @staticmethod
  def aggregate_pats(num2pats_dict):
    pats = reduce(operator.iconcat, num2pats_dict.values(), [])
    if len(pats) > 0:
      return reduce(lambda a, b: a + '|' + b, pats[1:], pats[0])
    return ''

  def non_capturing_pats(self):
    return re.sub('\((?!\?)', '(?:', self._capturing_pats())
