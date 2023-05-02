# AppOutputAnalysis/NonPeriodic
from NonPeriodic.Atom import BaseAtom		# '.' is essential
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

	def del_atom(self,idx):
		self.atom_list.pop(idx)

	def get_atomlist(self):
		return self.atom_list

	def get_atom(self,idx=None):

		'''
			Retrun type: BaseAtom
		'''

		if idx < len(self.atom_list):
			return self.atom_list[idx]

	def get_number_of_atoms(self):
		return self.number_of_atoms

	# DEV
	def show_info(self):
		for item in self.atom_list:
			item.show_info()
