#Kelley has olivine corrected compositions. These are input here to establish if these corrected compositions are corrected further by lee thermobarometer
import numpy as np
import matplotlib.pyplot as plt
import heapq
import operator
import sys
import os
import pdb
import matplotlib as mpl
import pet_read_in_with_labels

sys.path.insert(0, '/data/ap4909/30.10.2013-hot_cold_geochem/mantle_temp_cals/calculate_p_t_using_lee/aux_files')


from scipy.optimize import fsolve

samps_markers={}
h2o_colours={0:"r",4:'g',8:'b'}

volcano_names=["Ata","Tofua","Niuatoputapu","Tafahi","Kao","Late"]
island_symbols={"Agrigan":".","Almagan":"v","Anatahan":"8","Asuncion":"s","Guguan":"D","Pagan":'p',"Sarigan":"*","Uracas":"o"}#symbols for each island

for sub_zone in["Southern_Marianas"]:# 
		
	samps1=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/get_lat_lon_data/sz_with_lat_lon/individual_files/individual_files_with_feo/%s_new.xls"%(sub_zone),1,sub_zone)[0]
	kelley_samps=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/sample_testing/southern_marianas/kelley/kelley_appendix_4_formatted.xls",1,sub_zone)[0]
	
	mineral_props={"Fo=92":{"ol":0.65,"opx":0.3,"cpx":0.05},"Fo=91":{"ol":0.65,"opx":0.25,"cpx":0.1},"Fo=90":{"ol":0.65,"opx":0.2,"cpx":0.15}}	#mineral proportions for fo90,fo91,fo92 mantle

	ax=plt.gca()
	#ax2=ax.twinx()
	
	for samps,symbol in zip([kelley_samps],["d"]):
		x_vals=[]
		y_vals=[]
	
		t_vals=[]
		p_vals=[]
		graded_p_vals=[]
		latitudes=[]
		



		for comp in [0.9]:
			
				n=0#number of samples
			
				
				for key,value in samps.iteritems():
					h2o=value.pts["H2O(WT%)"]
					ti_post_corr=value.post_ol_correction_ti(comp,h2o,[0.25,0.25])
					print value.pts["TIO2(WT%)"],ti_post_corr
					
