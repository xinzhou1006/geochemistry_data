#Find function approximating slab surface
def slab_surf_function(slab_file):
	import numpy as np
	x,dep=np.loadtxt(slab_file,unpack=True)
	coeffs=np.polyfit(dep,x,3)
	return coeffs
	
