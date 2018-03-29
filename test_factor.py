
from pprint import pprint

import abs2lkm
import muls_gen
import librfactor_python

s = abs2lkm.convert(muls_gen.isw(3))
pprint(librfactor_python.factor_mi(s, 0.01, 10, 1e-6, 100))

