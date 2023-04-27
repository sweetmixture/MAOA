# OutputAnalysis/main.py


# importing viewpoint from $CWD

from NonPeriodic import Atom
from NonPeriodic import Molecule

if __name__ == "__main__":

	a1 = Atom.BaseAtom()
	a2 = Atom.BaseAtom()
	a3 = Atom.BaseAtom()

	m1 = Molecule.BaseMolecule()
	m1.add_atom(a1)
	m1.add_atom(a2)
	m1.add_atom(a3)
	m1.show_info()

	print('')
	print('---- after modification')
	a1.set_type('O')
	a2.set_type('H')
	a3.set_type('H')
	#print(a1.get_attr())
	m1.show_info()

	#NotImplemented
