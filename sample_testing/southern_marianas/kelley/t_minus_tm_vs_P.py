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

#sys.path.insert(0, '/data/ap4909/30.10.2013-hot_cold_geochem/mantle_temp_cals/calculate_p_t_using_lee')
sys.path.insert(0, '/data/ap4909/30.10.2013-hot_cold_geochem/mantle_temp_cals/calculate_p_t_using_lee/aux_files')
import pet_read_in_with_labels
import katz_melt_frac,fractionate

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
markers={"Southern_Marianas":".","South_Sandwich":"v","South_Vanuatu":"8","Central_Aleutians":"s","Izu":"D","Kermadec":"*","South_Lesser_Antilles":"o","North_Lesser_Antilles":"_","Tonga":"p","West_Aleutians":"h","New_Zealand":">","New_Britain":"x","North_Vanuatu":"+"}
#marker styles
colours={"Southern_Marianas":"b","South_Sandwich":"g","Costa_Rica":"r","Central_Aleutians":"c","Izu":"m","Kermadec":"k","South_Lesser_Antilles":"k","Tonga":"y","West_Aleutians":"w","New_Zealand":"m","New_Britain":"k","North_Vanuatu":"y"}
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



#Pressure function
d_a=[ 0.,     3000.,    15000.,    24400.,    71000.,   171000.,   220000.,271000.,   371000.,   400000.,   471000.,   571000.,  670000.,   771000., 871000.,   971000.,  1071000.,  1171000.,  1271000.,  1371000.,  1471000.,1571000.,  1671000.,  1771000.,  1871000.,  1971000.,  2071000.,  2171000.,2271000.,  2371000., 2471000.,  2571000.,  2671000.,  2771000.,  2871000.,2891000.]	#PREM depths

p_a=[  0.00000000e+00,   0.00000000e+00,   3.00000000e+08,   6.0000000e+08,  2.20000000e+09,   5.50000000e+09 ,  7.10000000e+09,   8.90000000e+09,   1.23000000e+10,   1.34000000e+10,   1.60000000e+10,   1.99000000e+10,   2.38000000e+10,   2.83000000e+10,  3.28000000e+10,   3.73000000e+10,   4.19000000e+10 ,  4.65000000e+10,   5.12000000e+10,  5.59000000e+10,  6.07000000e+10,   6.55000000e+10,7.04000000e+10,   7.54000000e+10,   8.04000000e+10,   8.55000000e+10,   9.06000000e+10,   9.58000000e+10,   1.01100000e+11,   1.06400000e+11,   1.11900000e+11,   1.17400000e+11,   1.23000000e+11,   1.28800000e+11 ,  1.34600000e+11,   1.35800000e+11]	#PREM pressures
def prem_pressure(height):
	for prem_depth in range(1,len(d_a)):	#loops through depths, starting at index one
		
		if -height<=d_a[prem_depth]: #checks in which depth interval the height is 
			Pressure=((p_a[prem_depth]-p_a[prem_depth-1])/(d_a[prem_depth]-d_a[prem_depth-1]))*((-height)-d_a[prem_depth-1])+p_a[prem_depth-1]
			
			break
	return Pressure
def depth(height):#find depth from pressure
	for prem_depth in range(1,len(p_a)):	#loops through depths, starting at index one
		
		if -height<=p_a[prem_depth]: #checks in which depth interval the height is 
			Pressure=((d_a[prem_depth]-d_a[prem_depth-1])/(p_a[prem_depth]-p_a[prem_depth-1]))*((-height)-p_a[prem_depth-1])+d_a[prem_depth-1]
			
			break
	return Pressure

#for geotherm_sub_zone in["Tonga"]:
#		
#		 	
#			P,T,lab=pet_read_in.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/mantle_temp_cals/calculate_p_t_using_lee/pt_files/fluidity_mantle_geotherms/vwet_%s_sub_arc_geotherms.csv"%(geotherm_sub_zone))
#		
#			print P,T

#P.reverse()
#T.reverse()
#	
#min_T=[]
#min_P=[]
#for i in range(len(T)):
#	if T[i]<1320:	#tempertaure where Tonga geotherm crosses 1300 adiabat
#		min_T.append(T[i])
#		min_P.append(P[i])
#	else:
#		break

#print depth(min_P[-1]*-1e9)
#for i in np.arange(depth(min_P[-1]*-1e9)/1000,300,1):
#	print i
#	min_T.append(1300+0.5*i)

#	min_P.append(prem_pressure(i*-1000)*1e-9)


#max_T=[]
#max_P=[]
#dT_dP_lith=(1472.-1051.)/(1.2-0.64)#deg per Gigapascal

#for i in np.linspace(0.64,1.2,100):
#	max_T.append(1051+dT_dP_lith*(i-0.64))

#	max_P.append(i)

#for i in np.arange(max_P[-1],6,1):
#	print i
#	max_T.append(1450+0.5*depth(i*-1e9)/1000)

#	max_P.append(i)
#plt.plot(max_T,max_P)
#plt.plot(min_T,min_P)
#ax=plt.gca()
#ax.invert_yaxis()
#plt.show()
#sys.exit()
def T_sol_solid_h2o(P,h2o,A1=1159):#calculate solidus given h2o in solid
	
	A2=132.9
	A3=-5.1
	K=43.0
	gam=0.75
	D_h2o=0.01
	#melt_h2o=h2o/(D_h2o+F*(1-D_h2o))
	dt=K*h2o**gam
	return A1+A2*P+A3*P**2-dt

	
ave_t={"Fo=90":0,"Fo=91":0,"Fo=92":0}
num_t={"Fo=90":0,"Fo=91":0,"Fo=92":0}
ave_p={"Fo=90":0,"Fo=91":0,"Fo=92":0}
num_samps={0:0,2:0,4:0,6:0,8:0}
num_in_range={0:0,2:0,4:0,6:0,8:0}
for sub_zone in ["Southern_Marianas"]:#["South_Vanuatu","North_Vanuatu","Southern_Marianas","North_Lesser_Antilles","South_Lesser_Antilles","West_Aleutians","Central_Aleutians",, "South_Sandwich","New_Britain","Kermadec","Izu","New_Zealand"]:
	
	if not os.path.exists(sub_zone):
		os.makedirs(sub_zone)
	
	labels=[]
	index=1
	samps1=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/get_lat_lon_data/sz_with_lat_lon/individual_files/individual_files_with_feo/%s_new.xls"%(sub_zone),1,sub_zone)[0]
	kelley_samps=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/sample_testing/southern_marianas/kelley/kelley_appendix_4_formatted.xls",1,sub_zone)[0]
	#samps=pet_read_in_with_labels.pet_read_in("pt_files/sample_tester.csv")
	mineral_props={"Fo=92":{"ol":0.65,"opx":0.3,"cpx":0.05},"Fo=91":{"ol":0.65,"opx":0.25,"cpx":0.1},"Fo=90":{"ol":0.65,"opx":0.2,"cpx":0.15}}	#mineral proportions for fo90,fo91,fo92 mantle

	ax=plt.gca()
	#ax2=ax.twinx()
	x_vals=[]
	y_vals=[]
	for samps,symbol,colour,label in zip([samps1,kelley_samps],["s","d"],["r","b"],["My samples","Kelley samples"]):
		i=0
		for key,value in samps.iteritems():
			
			for h2o in [4]:
			
			
			
				for comp in [0.9]:
				
					l=value.lee_pt_decimal(comp,h2o,[0.25,0.25])
					if symbol=="d":
						l=value.lee_pt_decimal_no_frac_correction(comp,h2o,[0.25,0.25])
						
						
						plt.plot(l[0][0]-T_sol_solid_h2o(l[0][1],h2o,A1=1085.7),l[0][1],markersize=20,marker=symbol,c="r",label="Kelley samples" if i==0 else "")
						i+=1
					elif symbol=="s":
						l=value.lee_pt_decimal(comp,h2o,[0.25,0.25])
						plt.plot(l[0][0]-T_sol_solid_h2o(l[0][1],h2o,A1=1085.7),l[0][1],markersize=20,marker=symbol,c=h2o_colours[h2o],label="My samples" if i==0 else "")
						i+=1
					
					
				
#"%s"%comp_style	
#			if est_ave_x!=0:
#				num_samps[h2o]+=1
#				for p in range(1,len(min_T),1):
#					if min_P[p-1]<est_ave_y<min_P[p]:
#						minimum_temp=((min_T[p]-min_T[p-1])/(min_P[p]-min_P[p-1]))*(est_ave_y-min_P[p-1])+min_T[p-1]
#				for p in range(1,len(max_T),1):
#					if max_P[p-1]<est_ave_y<max_P[p]:
#						maximum_temp=((max_T[p]-max_T[p-1])/(max_P[p]-max_P[p-1]))*(est_ave_y-max_P[p-1])+max_T[p-1]
#				if minimum_temp<est_ave_x<maximum_temp:
#					
#					num_in_range[h2o]+=1
					
				
		
		#setting up labels for legend

	
	
	#Annotating plot
	#solid
	
	
	
		#plt.annotate("Bars - Uncertainty due to Fe$^{3+}$/Fe (0.1-0.2)" ,xy = (1400,2.2), xytext = (1350, 3),fontsize=30,arrowprops=dict(facecolor='black', shrink=0.05))
	#ax.invert_yaxis()
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])		
	ax.legend(loc=4, numpoints=1)

	plt.title("Assumed constant 4 wt%% H2O")
		
	fs=20
	#Plotting solidi
	
	#plotting extreme geotherms
	#plt.plot(max_T,max_P,'k')
	#plt.plot(min_T,min_P,'k')
	#plt.xlim(1050,1410)
	plt.ylim(0,3)
	plt.xlim(0,200)	
	import matplotlib	
	print matplotlib.matplotlib_fname()
	ax.set_xlabel("Temperature - T$_{dry_sol}$")
	ax.set_ylabel("Pressure (GPa)")

	fig1=plt.gcf()
	fig1.set_size_inches(16, 12)
	directory="figures/"#+"%s"%(comp.replace("=","_")) #%(sub_zone,comp.replace("=","_"))

	if not os.path.exists(directory):
			os.makedirs(directory)

	
	print directory
	fig1.savefig("%st_minus_t_4pc_sol_vs_P.png"%(directory),bbox_inches='tight',dpi=(149))


	plt.show()
	plt.clf()

	
