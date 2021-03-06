def read_in():	#reads in H and crustal thickess from file
	thickness_tp={}	#Dictionary to hold single subduction parameter
	H_param={}
	AT_dist={} #arc-trench distance
	params_file=open("/data/ap4909/30.10.2013-hot_cold_geochem/code/sub_zone_params.csv",'r')
	lines=params_file.readlines()
	params=lines[0].split("\t")
	for line in lines[1:]:
		words=line.split('\t')
		thickness_tp[words[0].replace("_"," ")]=float(eval(words[12]))
		H_param[words[0].replace("_"," ")]=float(eval(words[6]))
		AT_dist[words[0].replace("_"," ")]=float(eval(words[13]))
	return thickness_tp,AT_dist
