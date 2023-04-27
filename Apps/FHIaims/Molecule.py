import os
from NonPeriodic.Molecule import BaseMolecule
from NonPeriodic.Atom import BaseAtom

'''

'''
class FHIaimsMolecule(BaseMolecule):

	def __init__(self,geometry_file=None):
		'''
		'''
		super().__init__()




		if geometry_file != None:
			if os.path.exists(geometry_file):
				print(geometry_file)

if __name__ == '__main__':

	print('test')

	fmol = FHIaimsMolecule()
	a1 = BaseAtom()

	fmol.add_atom(a1)

	fmol.show_info()
