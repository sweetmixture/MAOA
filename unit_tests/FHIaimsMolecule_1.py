from AppOutputExtractor.FHIaims.FHIaimsMolecule import molecule as fmol
from NonPeriodic.Atom import BaseAtom as ba

import copy


a1 = ba()
a2 = ba()
fm1 = fmol()

fm1.add_atom(a1)
fm1.add_atom(a2)

fm1.show_info()


# ----- modify atoms
print("after atom modification")

ga1 = fm1.get_atom(0)
ga1.show_info()
print('--')
ga1.set_cart(1,2,3)
ga1.show_info()
print('--')
fm1.show_info()

fm1.get_atom(1).set_cart(-1,0.2,-4)
fm1.get_atom(1).show_info()

a3 = fm1.add_atom(copy.deepcopy(fm1.get_atom(1)))
fm1.show_info()
print(fm1.get_number_of_atoms())
