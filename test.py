
# Entries in a `dicti` can be accessed case invariantly:

from pydicti import dicti, build_dicti, Dicti
keys = ['Hello', 'beautiful', 'world!']
values = [1, 2, 3]
z = list(zip(keys, values))
i = dicti(z)
assert "WorLD!" in i and "universe" not in i


# However, the in calls like `.keys()` or `.items()` the keys are returned
# as in their original case:

assert "Hello" in list(i.keys())


# `dicti` can be "derived" from  another custom dictionary extension using
# it as the underlying dictionary to gain additional properties like order
# preservation:

from collections import OrderedDict
odicti = build_dicti(OrderedDict)
oi = odicti(z)
assert list(oi.keys()) == keys


# The equality  comparison preserves  the semantics of  the base  type and
# reflexitivity as best  as possible. This has impact  on the transitivity
# of the comparison operator:

rz = list(zip(reversed(keys), reversed(values)))
roi = odicti(rz)
assert roi == i and i == oi
assert oi != roi and roi != oi  # NOT transitive!
assert oi == i and i == oi      # reflexive


# Be careful  with reflexitivity when  comparing to non-`dicti`  types and
# even more so if both operands are  not subclasses of each other. Here it
# is important  to know about  coercion rules.  `o == oli`  actually calls
# `oli.__eq__(o)` if `oli` is of a subclass of the type of of `o`. See:

# http://docs.python.org/2/reference/datamodel.html#coercion-rules 

o = OrderedDict(oi)
oli = Dicti(oi.lower_dict())
assert oli == o and o == oli    # reflexive (coercion rules)
print(o.__eq__(oli))            # dependends on OrderedDict.__eq__


# Note that `dicti` is the type corresponding to `builtins.dict`:

assert build_dicti(dict) is dicti


# The  method   `Dicti`  is  convenient  for   creating  case  insensitive
# dictionaries from a given object automatically using the objects type as
# the underlying dictionary type.

assert oi == Dicti(o)
assert type(oi) is type(Dicti(o))


# The  subclassing approach  works well  with "badly"  written code  as in
# `json` that checks for `isinstance(dict)`:

import json
assert oi == json.loads(json.dumps(oi), object_pairs_hook=odicti)
