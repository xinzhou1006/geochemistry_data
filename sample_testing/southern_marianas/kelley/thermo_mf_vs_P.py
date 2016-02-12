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

def find_sample_cpx(h2o,value):
	mg_num_pressures={1:[0.893419654, 0.8939711286, 0.8947333745, 0.8955833832, 0.8965132211, 0.8977497991, 0.9010621194, 0.9046779485, 0.9068739487, 0.9083730847, 0.9122724521, 0.9163512318, 0.9184344261, 0.9289337253720003],2:[0.893419654,0.8946631348,0.8958661911,0.8971594463,0.8997587134,0.9030800356,0.9065112616,0.9101533627,0.9143320171,0.9183456819,0.9225677704,0.9251762166,0.9296685406111111],3:[0.893419654, 0.8948892454, 0.896325929, 0.8977307977, 0.9004492264, 0.9042174011, 0.9078788702, 0.9115185463, 0.9156145063, 0.9198119194, 0.923737173, 0.927344753, 0.9303134612, 0.9308657790046512]}
	mf_pressures={1:[0.000,0.020,0.040,0.061,0.079,0.100,0.151,0.201,0.231,0.251,0.299,0.349,0.374,0.5],2:[0.000,0.022,0.040,0.061,0.100,0.149,0.199,0.248,0.299,0.348,0.402,0.438,0.5],3:[0.000,0.020,0.041,0.060,0.099,0.151,0.201,0.252,0.299,0.351,0.400,0.449,0.492,0.5]}
	
	
	pre_P=1
	if pre_P<1:
		comp_frac=np.interp(comp,mg_num_pressures[1],mf_pressures[1])
	elif 1<pre_P<2:
		comp_frac_1=np.interp(comp,mg_num_pressures[1],mf_pressures[1])
		comp_frac_2=np.interp(comp,mg_num_pressures[2],mf_pressures[2])
		comp_frac_list=[comp_frac_1,comp_frac_2]
		comp_frac=np.interp(P,[1,2],comp_frac_list)
	elif 2<pre_P<3:
		comp_frac_1=np.interp(comp,mg_num_pressures[2],mf_pressures[2])
		comp_frac_2=np.interp(comp,mg_num_pressures[3],mf_pressures[3])
		comp_frac_list=[comp_frac_1,comp_frac_2]
		comp_frac=np.interp(P,[2,3],comp_frac_list)
	elif pre_P>3:
		comp_frac=np.interp(comp,mg_num_pressures[3],mf_pressures[3])

	cpx_mode=value.mineral_mode(comp_frac,pre_P,"cpx")#getting modal abundance of cpx in source
	return cpx_mode
for sub_zone in["Southern_Marianas"]:# 
		
	samps1=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/get_lat_lon_data/sz_with_lat_lon/individual_files/individual_files_with_feo/%s_new.xls"%(sub_zone),1,sub_zone)[0]
	kelley_samps=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/sample_testing/southern_marianas/kelley/kelley_appendix_4_formatted.xls",1,sub_zone)[0]
	
	mineral_props={"Fo=92":{"ol":0.65,"opx":0.3,"cpx":0.05},"Fo=91":{"ol":0.65,"opx":0.25,"cpx":0.1},"Fo=90":{"ol":0.65,"opx":0.2,"cpx":0.15}}	#mineral proportions for fo90,fo91,fo92 mantle
	mf_vals_their_h2o=[]
	mf_vals_katz=[]
	for samps,symbol,colour,label in zip([samps1,kelley_samps],["s","d"],["r","b"],["My samples","Kelley samples"]):
		P_vals=[]
		mf_vals=[]
		
		for h2o in [4]:

			for comp in [0.9]:	
				for key,value in samps.iteritems():
					if symbol=="d":
						l=value.lee_pt_decimal_no_frac_correction(comp,h2o,[0.25,0.25])
						their_h2o=value.pts["H2O(WT%)"]
						P_vals.append(value.lee_pt_decimal_no_frac_correction(comp,h2o,[0.25,0.25])[0][1])
						mf_vals.append(value.kelley_mf_arc(comp,l[0],h2o))
						mf_vals_katz.append(value.katz_mf_new(comp,find_sample_cpx(h2o,value),l[0],h2o))
						mf_vals_their_h2o.append(value.kelley_mf_arc(comp,l[0],their_h2o))
					elif symbol=="s":
						l=value.lee_pt_decimal(comp,h2o,[0.25,0.25])
						ti_corrected=value.get_ti_corrected(0.9,h2o,0.25)
						mf_vals.append(value.kelley_mf_arc(comp,l[0],h2o))
						P_vals.append(value.lee_pt_decimal(comp,h2o,[0.25,0.25])[0][1])
#						if ti_corrected==0:
#							print key

		print mf_vals,P_vals
		plt.scatter(mf_vals,P_vals,marker=symbol,c=colour,label=label,s=100)
		
plt.scatter(mf_vals_their_h2o,P_vals,marker=symbol,c="g",label="using their h2o",s=100)
#plt.scatter(mf_vals_their_h2o,P_vals,marker=symbol,c="g",label="using their h2o",s=100)
plt.legend()
plt.ylabel("Pressure (GPa)")
plt.xlabel("Thermo melt Fraction")
fig1=plt.gcf()
fig1.set_size_inches(24, 12)
directory="figures/"+"melt_fractions/"#+"%s"%(comp.replace("=","_")) #%(sub_zone,comp.replace("=","_"))
if not os.path.exists(directory):
		os.makedirs(directory)
import matplotlib
print matplotlib.matplotlib_fname()
fig1.savefig("%sthermo_mf_vs_P.png"%(directory),bbox_inches='tight',dpi=(149))
plt.show()
