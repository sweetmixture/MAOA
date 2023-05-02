# /AppOutputAnalysis/Apps/NonPeriodic
'''

'''
class BaseAtom(object):

	def __init__(self,atom_type='atom',atom_attr='default',x=0.,y=0.,z=0.):

		self.type = atom_type
		self.cart  = [float(x),float(y),float(z)]
		self.attr = atom_attr
		
	def set_type(self,atom_type):
		self.type = atom_type

	def set_attr(self,atom_attr):
		self.attr = atom_attr

	def set_cart(self,x=None,y=None,z=None):

		if x != None:
			self.cart[0] = float(x)
		if y != None:
			self.cart[1] = float(y)
		if z != None:
			self.cart[2] = float(z)

	def get_cart(self):
		'''
			return type 'list' length:3 (cartesian xyz) : shallow copy
		'''
		return self.cart

	def get_type(self):
		return self.type

	def get_attr(self):
		return self.attr

	def show_info(self):
		print("type: {0:2s}, attr: {1:4s}, cart: {2: >+.12f} {3: >+.12f} {4: >+.12f}".format(self.type, self.attr, self.cart[0], self.cart[1], self.cart[2]))
		#print("type: {0:2s}, attr: {1:4s}, cart: {2: >+24f} {3: >+24f} {4: >+24f}".format(atom_type, atom_attr, x, y, z))
		#print('type: {}, attr: {}, cart: {} {} {}'.format(self.type, self.attr, self.cart[0], self.cart[1], self.cart[2]))
