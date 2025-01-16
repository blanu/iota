from api import *
from register import *

def eval(*e):
    se = Object.from_python_to_expression(list(e))
    i_data = se.to_bytes()
    register = EvalRegister.allocate_zero()
    register.load_i(i_data)
    register.eval()
    r_data = register.retrieve_r()
    (result, rest) = Object.from_bytes(r_data)
    if len(rest) > 0:
        raise Exception("bad decode, %d bytes leftover" % len(rest))
    else:
        return Object.to_python(result)
