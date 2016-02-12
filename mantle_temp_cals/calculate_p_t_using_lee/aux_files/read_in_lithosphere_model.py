def read_in_lithosphere_model(model_file):#read in Conrad lithosphere model (lon,lat,z)
#	import numpy as np
#	infile=open(model_file,'r')
#	lines=infile.readlines()
#	model={}
#	for n in np.arange(-90,91,1):
#		model[n]={}
#	print model
#	for line in lines:
#		nums=line.split()
#		lat=float(nums[1])
#		lon=float(nums[0])
#		prev_lat=float(nums[1])
#		z=float(nums[2])
#		model[lat][lon]=z
#	return model
	import numpy as np
	infile=open(model_file,'r')
	lines=infile.readlines()
	model=[]
	
	li=[]
	for line_n in range(len(lines)-1):
				
		
		nums=lines[line_n].split()
		lat=float(nums[1])
		lon=float(nums[0])

		next_nums=lines[line_n+1].split()
		next_lat=float(next_nums[1])
		if lat!=next_lat:
			model.append(li)
			li=[]
		else:
			li.append(float(nums[2]))
	print np.array(model)
	
	return np.array(model)	
