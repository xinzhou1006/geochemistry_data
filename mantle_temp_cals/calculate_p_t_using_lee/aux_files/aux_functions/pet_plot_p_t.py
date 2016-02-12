
def plot_pet_p_t(pet_files,m,l,col):#takes in list of files, markersize,linestyle and colour
	import matplotlib.pyplot as plt
	for fil in pet_files:	#looping through P-T from petrological estimates
		infile=open(fil,'r')
		lines=infile.readlines()
		lab=lines[0]
		P=[]
		T=[]
	
		for line in lines[1:]:
			nums=line.split(",")
			print nums
			P.append(float(nums[1]))
			T.append(float(nums[0]))
		plt.plot(T,P,"%s"%l,markersize=m,c=col,label="%s"%lab)
