####################################################################
#Reads in major elements for each subduction zone, calculates P,T for a range of conditions using Lee et al 2009 spreadsheet algorithm. Compares P,T with range expected in subduction zones to find which H2O fits the most samples
####################################################################
import numpy as np
import matplotlib.pyplot as plt
import heapq
import operator
import sys
import os
import pdb
import matplotlib as mpl
import math
#sys.path.insert(0, '/data/ap4909/30.10.2013-hot_cold_geochem/mantle_temp_cals/calculate_p_t_using_lee')
sys.path.insert(0, '/data/ap4909/30.10.2013-hot_cold_geochem/mantle_temp_cals/calculate_p_t_using_lee/aux_files')
import pet_read_in_with_labels
import katz_melt_frac,fractionate
import sub_zone_markers
from scipy.optimize import fsolve
#########################USER INPUT#######################
plot_melting_adiabat=0#calculates melting adiabat back to solidus
annotate_samps=0#annotate samples by name
dP=0.005 #pressure increment in GPa
colour_by_param=0#colour by subduction zone parameters
homologous_T=1 #Plot homologous temp (temperature divided by solidus T at that depth)

#Plot settings
title_fs=20#title fontsize
#########################USER INPUT#######################

H_annotate_locs={"Southern_Marianas":1200,"South_Sandwich":1100,"South_Vanuatu":"1080","Central_Aleutians":1100,"Izu":1100,"Kermadec":1200,"South_Lesser_Antilles":1100,"North_Lesser_Antilles":1100,"Tonga":1100,"West_Aleutians":1100,"New_Zealand":1200,"New_Britain":1200,"North_Vanuatu":1100}
markers=sub_zone_markers.markers
colours={"Southern_Marianas":"b","South_Sandwich":"g","Costa_Rica":"r","Central_Aleutians":"c","Izu":"m","Kermadec":"k","Lesser_Antilles":"c","Tonga":"y","West_Aleutians":"w","New_Zealand":"m","New_Britain":"k","North_Vanuatu":"y"}
comp_colours={"Fo=92":'k',"Fo=91":'b',"Fo=90":'g'}
h2o_colours={0:'r',2:'y',4:'c',6:'g',8:'b'}
mant_vals={"Fo=92":{"Y":3.129,"La":0.134,"Ti":650.0},"Fo=91":{"Y":3.328,"La":0.192,"Ti":716.3},"Fo=90":{"Y":3.548,"La":0.253,"Ti":792.0}}#mantle concentrations for DDMM, Ave DMM and enriched DMM from workman and Hart 2005
island_symbols={"Tafahi":".","Tofua":"v","Ata":"8","Niuatoputapu":"s","Kao":"D","Tongatapu":"*","Late":'p'}#symbols for each island

all_params={}
params_file=open("/data/ap4909/30.10.2013-hot_cold_geochem/code/sub_zone_params_slim_version.csv",'r')
lines=params_file.readlines()
params=lines[0].split("\t")[1:]

for p in range(len(params)):#getting all subduction parameters in dictionary in form all_params[PARAMETER][SUBDUCTION ZONE]
	
	all_params[params[p]]={}
for line in lines[1:]:
	words=line.split('\t')
	for p in range(len(params)):
		val=float(eval(words[p+1].rstrip()))
		if np.isnan(val) == True:
			all_params[params[p]][words[0]]=0.0
		elif np.isnan(val) == False:
			all_params[params[p]][words[0]]=float(eval(words[p+1].rstrip()))



all_x_vals=[]
all_y_vals=[]
num_samps={0:0,2:0,4:0,6:0,8:0}
num_in_range={0:0,2:0,4:0,6:0,8:0}
for sub_zone in ["Southern_Marianas","Lesser_Antilles","West_Aleutians","Central_Aleutians","Tonga", "South_Sandwich","New_Britain","Kermadec","Izu"]:
	
	
	
	labels=[]
	index=1
	samps=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/get_lat_lon_data/sz_with_lat_lon/individual_files/individual_files_with_feo/%s_new.xls"%(sub_zone),1,sub_zone)[0]
	#samps=pet_read_in_with_labels.pet_read_in("pt_files/sample_tester.csv")
	
	#ax2=ax.twinx()
	
	fo2=[0.15,0.15]
	i=0
	x_vals=[]
	y_vals=[]
	for key,value in samps.iteritems():
		
		for h2o in [4]:
			
			
			
			for comp in [0.9]:
				print value.get_majors_corrected(comp,h2o,fo2)
				tio2=float(value.get_majors_corrected(comp,h2o,fo2)["TIO2"])
				na2o=float(value.get_majors_corrected(comp,h2o,fo2)["NA2O"])
				print tio2
				
				ti=(((47.87/79.87)*tio2)/100.)*1000000.
				na=(((45.978/61.977)*na2o)/100.)*1000000.
				if math.isnan(na2o) is False and math.isnan(tio2) is False: 
					x_vals.append(tio2)
					y_vals.append(na2o)
					all_x_vals.append(tio2)
					all_y_vals.append(na2o)
	
				i+=1
				

	plt.scatter(x_vals,y_vals,s=200,marker=markers[sub_zone],c=colours[sub_zone],label=sub_zone)#"%s"%comp_style
	
	
	plt.title("H2O=%s,residue=%s,fo2=%s"%(h2o,comp,fo2[0]))
	
	
	plt.xlabel("TiO2 (frac corrected)")
	plt.ylabel("Na2O (frac corrected)")
	

	fig1=plt.gcf()
	fig1.set_size_inches(24, 12)
	directory="figures/melt_fractions/"#"#+"%s"%(comp.replace("=","_")) #%(sub_zone,comp.replace("=","_"))

	if not os.path.exists(directory):
			os.makedirs(directory)

print np.corrcoef(x_vals,y_vals)
plt.annotate("r=%.2f"%np.corrcoef(all_x_vals,all_y_vals)[0][1],xy = (0.23,3),fontsize=30)
plt.legend()
print "%sna2o_vs_tio2.png"%(directory)
fig1.savefig("%sna2o_vs_tio2.png"%(directory),bbox_inches='tight',dpi=(149))


plt.show()
	

	
