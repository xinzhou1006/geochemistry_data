def find_sub_arc_isotherm_depth(u,temp,a_t_dist):#Take in vtu, temp, arc-trench distance, return isotherm depth
	import vtktools
	import numpy as np
	import matplotlib.pyplot as plt
	from scipy.interpolate import interp1d
	max_x=301000#maximum x distance from trench to be considered
	wedge_pts=[]
	X=np.array([i for i in np.arange(0,max_x,1000)])
	Y=np.array([i for i in np.arange(0,-201000,-1000)])
	
	for i in np.arange(0,max_x,1000):
		for j in np.arange(0,-201000,-1000):
	
			wedge_pts.append([i,j,0.0])	
	dom=vtktools.arr(np.array(wedge_pts))		
	temp_struct=u.ProbeData(dom,'Temperature')
	
	CS=plt.contour(X,Y,np.reshape(temp_struct,(301,201)).T,[temp],colors="w",linewidth=200)
	plt.clf()
	x=[]	
	y=[]
	for i in range(2):
		p=CS.collections[0].get_paths()[i]
	
		v=p.vertices
		x.extend(v[:,0])
		y.extend(v[:,1])
	x_new=[]
	y_new=[]
	for i in range(len(y)):
		if y[i] >-100000:
			x_new.append(x[i])
			y_new.append(y[i])
			
	f=interp1d(x_new,y_new)
	
	
	return f(a_t_dist)
	
