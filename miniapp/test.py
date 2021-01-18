#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by huangding 2017/7/9

import json
import re

t = '造成<br>⇒ 5,000 萬光屬'
print(re.sub(r'(\d+)(,)(\d+)',r'\1\3', t))
# [\u4e00-\u9fa5]*[0-9]*[.]*[0-9]*[%]*[\u4e00-\u9fa5]*