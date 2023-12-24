from classes.Selector import Selector
import pandas as pd
import numpy as np

sl = Selector()


mydict = sl.get_groups_dfs(["FAF-223", "FAF-221"],[3,3])
print(mydict["FAF-221"]["subjects"])
