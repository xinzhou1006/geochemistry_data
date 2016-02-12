def thermal_erosion(wedge_pts,temp_struct,arc_t_dist,temp_depth,Tc):#Takes arrays of x and y points, the temperature grid at those points, arc trench distance, and Tc and adds in thermal erosion model of England and Katz 2010
	M=4e-3
	
	Ts=273
	dt=Tc-Ts
	k=4
	L=4e5
	h_w=5

	def Meta():
		return M*L*h_w/(k*dt)

	def T(z):
		zm=Meta()/(Meta()+1)
		
		zm=temp_depth-(zm*temp_depth)
		
		if z<zm:
			return Tc
		else:
			
			print ((abs(z)-abs(zm))/(abs(temp_depth)-abs(zm)))
			return Tc+(Tc-Ts)*((abs(z)-abs(zm))/(abs(temp_depth)-abs(zm)))
	for i in range(len(wedge_pts)):
			if arc_t_dist-7500<wedge_pts[i][0]<arc_t_dist+7500:
				if wedge_pts[i][1]>temp_depth: 
					temp_struct[i]=T(wedge_pts[i][1])

	#print Meta()/(Meta()+1),temp_depth
	return temp_struct
