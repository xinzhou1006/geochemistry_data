#plot serpentinite and chlorite out for peridotite as digitized from grove 2009
def plot_phase_outs(files,colours,coord,temp_struct):#takes in files and colours as lists, vtk object of pvtu and plots lines
	import sys
	sys.path.insert(0, '/data/ap4909/30.10.2013-hot_cold_geochem/mantle_temp_cals/calculate_p_t_using_lee')
	import pet_read_in
	import numpy as np
	import vtktools
	import matplotlib.pyplot as plt
	from matplotlib.colors import LinearSegmentedColormap
	max_x=301000
	x=np.array([i for i in np.arange(0,max_x,1000)])
	y=np.array([i for i in np.arange(0,-201000,-1000)])
	print len(temp_struct)
	
	
	#sys.exit()
	for phase_file,phase_col in zip(files,colours):
		phase_arr=[]#creating an array with same dimensions as u; overwrite values later
		p_p,p_t,la=pet_read_in.pet_read_in("%s"%phase_file)#depth,temperature,label(at top of file) returned
		for i in range(len(temp_struct)):
			#print temp_struct[i][0], "this"
			found=0
			for k in range(len(p_p)-1):
				#print -1*coord[i][1], p_p[k+1],temp_struct[i]
				if p_p[k]<-1*coord[i][1]<p_p[k+1]:
					found=1
					T_interp=p_t[k]+((p_t[k+1]-p_t[k])/(p_p[k+1]-p_p[k]))*(-1*coord[i][1]-p_p[k])
					
					
					if (temp_struct[i][0]-273+(0.0005*coord[i][1]*-1))<T_interp:
						phase_arr.append([1])
					else:
						phase_arr.append([0])
			if found==0:
				phase_arr.append([0])
		phase_arr=np.array(phase_arr)
		print phase_arr,len(phase_arr),len(temp_struct)
		cmap = LinearSegmentedColormap.from_list('mycmap', [(0 , 'white'),
                                                    (1 , '%s'%phase_col),
                                                    ]
                                        )
		S=plt.pcolormesh(x,y,np.reshape(phase_arr,(301,201)).T,cmap=cmap,shading='gouraud')
			
			
#		for i in np.arange(0,max_x,1000):
#			for j in np.arange(0,-201000,-1000):
				
#		for d,t in zip(p_p,p_t):	#looping through each p,t for phase out		
#			adi_dep=d#depth of point in metres
#			adi_T=t		
#			adi_pts=[]
#			print adi_T,adi_dep
#			for x_point in np.arange(0,max_x,1000):	#create array of points from slab surface to x_max at the depth of the sample						
#				adi_pts.append([x_point,-1*adi_dep,0.0])

#			adi_pts=vtktools.arr(adi_pts)
#			adi_temperature_structured = u.ProbeData(adi_pts, 'Temperature')
##			if adi_dep<10000:
##				print adi_temperature_structured-273
#			for adi_t in range(len(adi_temperature_structured)-1):
#				if adi_temperature_structured[adi_t]-273+(0.0005*adi_dep)<adi_T<adi_temperature_structured[adi_t+1]-273+(0.0005*adi_dep):
#				#c=raw_input('hello')
##									print h2o,key
##									print adi_T+273,adi_temperature_structured[adi_t]-273+(0.0005*adi_dep),adi_temperature_structured[adi_t+1]-273+(0.0005*adi_dep)
#					adi_x=(1000.0/(adi_temperature_structured[adi_t+1]-adi_temperature_structured[adi_t]))*((adi_T+273)-adi_temperature_structured[adi_t])+adi_pts[adi_t][0]
#			
#					X_lis.append(adi_x)
#					print "in"
#					Y_lis.append(adi_dep*-1)
#				
#					


#		plt.plot(X_lis,Y_lis,c="%s"%phase_col,linewidth=2,label=la)

