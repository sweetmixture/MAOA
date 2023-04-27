from Apps.FHIaims.Molecule import FHIaimsMolecule as fmol
from NonPeriodic.Atom import BaseAtom as ba

a1 = ba()
a2 = ba()
fm1 = fmol()

fm1.add_atom(a1)
fm1.add_atom(a2)

fm1.show_info()
