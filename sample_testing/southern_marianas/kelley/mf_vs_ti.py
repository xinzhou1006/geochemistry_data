#Plot mf vs ti 
import numpy as np
import matplotlib.pyplot as plt
import heapq
import operator
import sys
import os
import pdb
import matplotlib as mpl


sys.path.insert(0, '/data/ap4909/30.10.2013-hot_cold_geochem/mantle_temp_cals/calculate_p_t_using_lee/aux_files')
import pet_read_in_with_labels


from scipy.optimize import fsolve

samps_markers={}
h2o_colours={0:"r",4:'g',8:'b'}

volcano_names=["Ata","Tofua","Niuatoputapu","Tafahi","Kao","Late"]
island_symbols={"Agrigan":".","Almagan":"v","Anatahan":"8","Asuncion":"s","Guguan":"D","Pagan":'p',"Sarigan":"*","Uracas":"o"}#symbols for each island

for sub_zone in["Southern_Marianas"]:# 
		
	samps1=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/get_lat_lon_data/sz_with_lat_lon/individual_files/individual_files_with_feo/%s_new.xls"%(sub_zone),1,sub_zone)[0]
	kelley_samps=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/sample_testing/southern_marianas/kelley/kelley_appendix_4_formatted.xls",1,sub_zone)[0]
	
	mineral_props={"Fo=92":{"ol":0.65,"opx":0.3,"cpx":0.05},"Fo=91":{"ol":0.65,"opx":0.25,"cpx":0.1},"Fo=90":{"ol":0.65,"opx":0.2,"cpx":0.15}}	#mineral proportions for fo90,fo91,fo92 mantle
	
	for samps,symbol,colour,label in zip([samps1,kelley_samps],["s","d"],["r","b"],["My samples","Kelley samples"]):
		ti_vals=[]
		mf_vals=[]
		for h2o in [4]:

			for comp in [0.9]:	
				for key,value in samps.iteritems():
					if symbol=="d":
						#plt.plot(value.tio2,value.quick_mf(value.tio2,0.09,0.123),marker=symbol,c="b")
						mf_vals.append(value.quick_mf(value.tio2,0.09,0.123))
						ti_vals.append(value.tio2)
					elif symbol=="s":
						ti_corrected=value.get_ti_corrected(0.9,h2o,0.25)
						mf_vals.append(value.quick_mf(ti_corrected,0.09,0.123))
						ti_vals.append(ti_corrected)
#						if ti_corrected==0:
#							print key
		plt.scatter(ti_vals,mf_vals,marker=symbol,c=colour,label=label,s=100)
		
plt.legend()
fig1=plt.gcf()
fig1.set_size_inches(24, 12)
directory="figures/"+"melt_fractions/"#+"%s"%(comp.replace("=","_")) #%(sub_zone,comp.replace("=","_"))
if not os.path.exists(directory):
		os.makedirs(directory)

fig1.savefig("%smf_vs_ti.png"%(directory),bbox_inches='tight',dpi=(149))
plt.show()
