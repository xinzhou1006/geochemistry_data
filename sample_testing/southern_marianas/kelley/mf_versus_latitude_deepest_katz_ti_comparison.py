#estimate melt fraction from Katz/Kelley theromabarometry and from Ti vs latitude
import numpy as np
import matplotlib.pyplot as plt
import heapq
import operator
import sys
import os
import pdb
import matplotlib as mpl

sys.path.insert(0, '/data/ap4909/30.10.2013-hot_cold_geochem/mantle_temp_cals/calculate_p_t_using_lee')
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

	ax=plt.gca()
	#ax2=ax.twinx()
	latitudes=[]
	p_vals=[]
	mf_vals=[]
	for samps,symbol in zip([samps1,kelley_samps],["s","d"]):
	#for samps,symbol in zip([samps1],["s"]):
		
		
		
		
		for h2o in [4]:



			for comp in [0.9]:
			
				n=0#number of samples
			
			
				for key,value in samps.iteritems():
					if symbol=="d":
							
						h2o=value.pts["H2O(WT%)"]
					
					if sub_zone in ["Central_Aleutians","West_Aleutians","New_Britain"]:
						latitude=(value.pts["LONGITUDE (MIN.)"]+value.pts["LONGITUDE (MAX.)"])/2.
					else:
						latitude=(value.pts["LATITUDE (MIN.)"]+value.pts["LATITUDE (MAX.)"])/2.
					if latitude!=0:
						latitudes.append(latitude)
					l=value.lee_pt_decimal(comp,h2o,[0.15,0.15])
					
					#print l,volcano
					if l[0][0]==0 and l[1][0]==0:
						est_ave_x=0
						est_ave_y=0
					elif l[0][0]==0 or l[1][0]==0:	#sometimes lee algorithm returns 0.0 for an oxygen fugacity - therefore average turns out to be half of the other fo2 P,T
						for i in l:
							if i[0] !=0:

								est_ave_x=i[0]
								est_ave_y=i[1]



					elif l[0][0]!=0 and l[1][0]!=0:	#if two values are available for two different fo2's
						est_ave_x=(l[0][0]+l[1][0])/2.
						est_ave_y=(l[0][1]+l[1][1])/2.
						
					
						if symbol=="d":
					
							plt.plot(latitude,value.quick_mf(value.tio2,0.09,0.123),markeredgecolor='g',markersize=30,markerfacecolor='None',marker=symbol)
							mf_vals.append(value.quick_mf(value.tio2,0.09,0.123))
						elif symbol=="s":
							ti_corrected=value.get_ti_corrected(0.9,h2o,0.25)
							
							plt.plot(latitude,value.quick_mf(ti_corrected,0.09,0.123),color='g',markersize=30,marker=symbol,markeredgecolor="k")	
							mf_vals.append(value.quick_mf(ti_corrected,0.09,0.123))
	plt.title("Melt fraction variation along arc, 4wt% H2O")
	print max(latitudes),max(latitudes)+(max(latitudes)-min(latitudes))*0.05
	plt.xlim(min(latitudes)-(max(latitudes)-min(latitudes))*0.05,max(latitudes)+(max(latitudes)-min(latitudes))*0.05)
	
	plt.ylim(min(mf_vals)-(max(mf_vals)-min(mf_vals))*0.1,max(mf_vals)+(max(mf_vals)-min(mf_vals))*0.05)
	#setting up legend
#	for col,name in zip(["g",'none'],["Full symbol - Mg#=0.90","Hollow symbol - Mg#=0.92"]):
#		plt.scatter(0,0,label=name,marker="s",edgecolor="g",facecolors=col)
	for col,name in zip(["s","d"],["Database from this study","Kelley et al 2010"]):
		plt.scatter(0,0,label=name,marker=col,edgecolor="g",facecolors="g")
	plt.annotate("Sarigan",xy = (16.7,3),fontsize=30)
	plt.annotate("Guguan",xy = (17.4,3),fontsize=30)
	plt.annotate("Pagan",xy = (18,3),fontsize=30)
	plt.annotate("Agrigan",xy = (18.5,3),fontsize=30)
	plt.annotate("Hollow symbol",xy = (17.4,4),fontsize=30)
	ax=plt.gca()
	ax.invert_yaxis()
	#box = ax.get_position()
	#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])		
	ax.legend(loc=3,numpoints=1,markerscale=6,fontsize=30,scatterpoints=1)
	if sub_zone in ["Central_Aleutians","West_Aleutians","New_Britain"]:	
		plt.xlabel("Longitude ($^\circ$)",fontsize=40)
	else:
		plt.xlabel("Latitude ($^\circ$)",fontsize=40)
	plt.ylabel("Melt fraction",fontsize=40)
	
	plt.tick_params(axis='both', which='major', labelsize=30)
	fig1=plt.gcf()
	fig1.set_size_inches(24, 12)
	directory="figures/"+"mf_vs_lat/"+"dataset_comparison/"#+"%s"%(comp.replace("=","_")) #%(sub_zone,comp.replace("=","_"))
	if not os.path.exists(directory):
			os.makedirs(directory)
	
	print "%s%s.png"%(directory,sub_zone)
	fig1.savefig("%s%s.png"%(directory,sub_zone),bbox_inches='tight',dpi=(149))
	
	plt.show()
	
	#plt.show()
