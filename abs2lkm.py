# Copyright 2018 FirstName LastName
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Conversion from abstract circuit model to circuit leakage model.
"""

import sys
import abs_circuit

def export_circuit_model(cont_vars, bijections, leaking_ops, properties):
    equalities, var_leakage, cont_vars, _ = abs_circuit.simplify_circuit_model(
            cont_vars, bijections, leaking_ops, properties)
    res = ''
    for op_kind, dest, ops in equalities:
        res += f'E {op_kind} {dest} {" ".join(ops)}\n'
    for var, leakage in var_leakage.items():
        res += f'L {var} {leakage}\n'
    for var in cont_vars:
        res += f'C {var}\n'
    return res

def convert(s):
    return export_circuit_model(*abs_circuit.parse_circuit_raw(s))

if __name__ == '__main__':
    in_fname = sys.argv[1]
    with open(in_fname) as f:
        s = f.read()
    res = convert(s)
    if len(sys.argv) < 3:
        print(res)
    else:
        with open(sys.argv[2], 'w') as f:
            f.write(res)
