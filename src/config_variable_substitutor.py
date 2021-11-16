import re
from functools import reduce

import yaml


class ConfigVariableSumbstitutor:
    '''
    This class converts strings containing constant self-defined variables to
    their values. We've found this approuch avoids complications related to
    right-to-left in Persian.
    '''

    instance = None

    @staticmethod
    def get_instance():
        if not ConfigVariableSumbstitutor.instance:
            ConfigVariableSumbstitutor.instance = ConfigVariableSumbstitutor()
        return ConfigVariableSumbstitutor.instance

    def compile_vars(self, string):
        repl = lambda m: self._fetch_var(m.group(1))
        return re.sub('@([a-zA-Z0-9.]+)', repl, string)

    def _fetch_var(self, key):
        """
        We load the file with each retrieval INTENTIONALLY in the dev environment
        because of the frequent updates on the file.
        """
        stream = open("configs.yaml", "r")
        config_vars = yaml.safe_load(stream)['vars']
        return reduce(lambda c, k: c[int(k) if k.isnumeric() else k], key.split('.'), config_vars)
