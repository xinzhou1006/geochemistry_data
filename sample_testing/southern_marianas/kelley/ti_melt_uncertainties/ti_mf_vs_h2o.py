#Plot mf vs P
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
h2o_vals=np.linspace(0,8,10)
for sub_zone in["Southern_Marianas"]:# 
		
	samps1=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/get_lat_lon_data/sz_with_lat_lon/individual_files/individual_files_with_feo/%s_new.xls"%(sub_zone),1,sub_zone)[0]
	
	mineral_props={"Fo=92":{"ol":0.65,"opx":0.3,"cpx":0.05},"Fo=91":{"ol":0.65,"opx":0.25,"cpx":0.1},"Fo=90":{"ol":0.65,"opx":0.2,"cpx":0.15}}	#mineral proportions for fo90,fo91,fo92 mantle

	for samps,symbol,colour,label in zip([samps1],["s"],["r"],["My samples"]):
		
		

		for comp in [0.9]:	
				for key,value in samps.iteritems():
					print key
					P_vals=[]
					mf_vals=[]
					for h2o in h2o_vals:
					
						ti_corrected=value.get_ti_corrected(0.9,h2o,0.25)
						mf_vals.append(value.quick_mf(ti_corrected,0.09,0.123))
					#P_vals.append(value.lee_pt_decimal(comp,h2o,[0.25,0.25])[0][1])
#						if ti_corrected==0:
#							print key
					plt.plot(h2o_vals,mf_vals,marker=".",markersize=10)
plt.legend()
plt.xlabel("H$_2$O wt%")
plt.ylabel("Ti melt Fraction")
fig1=plt.gcf()
fig1.set_size_inches(24, 12)
directory="figures/"#+"%s"%(comp.replace("=","_")) #%(sub_zone,comp.replace("=","_"))
if not os.path.exists(directory):
		os.makedirs(directory)
import matplotlib
print matplotlib.matplotlib_fname()
fig1.savefig("%sti_mf_vs_h2o.png"%(directory),bbox_inches='tight',dpi=(149))
plt.show()
