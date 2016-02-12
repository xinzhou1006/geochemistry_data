
def pet_read_in(pet_file):#takes in file and returns P,T list
	import matplotlib.pyplot as plt
	infile=open(pet_file,'r')
	lines=infile.readlines()
	lab=lines[0]
	P=[]
	T=[]
	
	for line in lines[1:]:
		nums=line.split(",")
		
		if nums[1]!='\n':
			P.append(float(nums[1].strip()))
			T.append(float(nums[0].strip()))
	return P,T,lab
