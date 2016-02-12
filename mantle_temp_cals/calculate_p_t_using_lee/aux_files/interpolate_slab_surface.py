#Interpolate x coordinate of slab surface from coords
def interpolate_slab_surface(slab_file):
	from scipy import interpolate
	import numpy as np
	x,dep=np.loadtxt(slab_file,unpack=True)
	f = interpolate.interp1d(dep,x)
	return f
	
