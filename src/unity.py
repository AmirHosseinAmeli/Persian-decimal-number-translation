from decimal_group import DecimalGroup


class Unity(DecimalGroup):

  instance = None

  @staticmethod
  def get_instance():
    if not Unity.instance:
      Unity.instance = Unity()
    return Unity.instance

  def __init__(self):
    self.w2n_dict = None
    self.pat_map = {i: [str(i), DecimalGroup.var_subs.compile_vars('@unity.'+str(i)), DecimalGroup.pers_digs[i]] for i in range(10)}

  def w2n(self, word):
    if not self.w2n_dict:
      self.w2n_dict = {}
      for num , pat_list in self.pat_map.items():
        for pat in pat_list:
          self.w2n_dict[pat] = num
    if word in self.w2n_dict:
      return self.w2n_dict[word]

  def _capturing_pats(self):
    return self.aggregate_pats(self.pat_map)
