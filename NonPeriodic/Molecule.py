# AppOutputAnalysis/Apps/NonPeriodic
from .Atom import BaseAtom		# '.' is essential
#from .Atom import BaseAtom

'''

'''

class BaseMolecule(object):

	def __init__(self):
		self.number_of_atoms = 0
		self.atom_list = []

	def add_atom(self,BaseAtom):
		self.number_of_atoms = self.number_of_atoms + 1
		self.atom_list.append(BaseAtom)

	def show_info(self):
		for item in self.atom_list:
			item.show_info()

