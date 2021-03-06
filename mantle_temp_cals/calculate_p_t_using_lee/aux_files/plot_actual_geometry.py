def plot_actual_geometry(sz_name):#plot realistic geometries from Cian
	files={"Tonga":'35_Tonga.dat',"Southern_Marianas":'40_S_Marianas.dat',"Izu":'43_Izu.dat',"South_Lesser_Antilles":"20_S_Antilles.dat","South_Sandwich":"21_Scotia.dat"}	
	infile=open("/data/ap4909/cian_flml/cian_meshes/Cian_Mesh_Generator/slab_geometries/%s"%files[sz_name],'r')
	lines =infile.readlines()
	depths=[]
	x=[]
	for line in lines:
		words=line.split()
		depths.append(float(words[1])*1000)
		x.append(float(words[0])*1000)
	return x,depths
