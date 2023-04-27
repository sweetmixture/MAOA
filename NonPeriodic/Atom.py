# /AppOutputAnalysis/Apps/NonPeriodic
'''

'''
class BaseAtom(object):

	def __init__(self,atom_type='atom',x=0.,y=0.,z=0.,atom_attri='defualt'):

		self.type = atom_type
		self.xyz  = [float(x),float(y),float(z)]
		self.attr = atom_attri
		
	def set_type(self,atom_type):
		self.type = atom_type

	def get_type(self):
		return self.type

	def set_attr(self,atom_attr):
		self.attr = atom_attr

	def get_attr(self):
		return self.attr

	def set_cart(self,x=None,y=None,z=None):

		if x != None:
			self.xyz[0] = float(x)
		if y != None:
			self.xyz[1] = float(y)
		if z != None:
			self.xyz[2] = float(z)

	def get_cart(self):
		'''
			return type 'list' length:3
		'''
		return self.xyz

	def show_info(self):
		#print('type: {} / cart: {} {} {} / attr: {}'.format(self.type,self.xyz[0],self.xyz[1],self.xyz[2],self.attr))
		print('type: {}, attr: {}, cart: {} {} {}'.format(self.type, self.attr, self.xyz[0], self.xyz[1], self.xyz[2]))
