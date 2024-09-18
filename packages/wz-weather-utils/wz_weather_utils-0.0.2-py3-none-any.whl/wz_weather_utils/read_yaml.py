# -*- coding: UTF-8 -*-
"""
@Name:__init__.py
@Auth:yujw
@Date:2024/7/25-20:13
"""

import yaml
from . import get_encoding


class ReadYaml:
    def __init__(self, file_path="resources/wea_config.yaml"):
        self.file_path = file_path
        self.encoding = get_encoding(file_path)
        with open(file_path, "r", encoding=self.encoding) as f:
            self.conf = yaml.load(f.read(), Loader=yaml.FullLoader)

    def read(self, key):
        return self.conf.get(key)

    def write(self, values):
        with open(self.file_path, "w+", encoding=self.encoding) as f:
            yaml.dump(values, stream=f, allow_unicode=True)
