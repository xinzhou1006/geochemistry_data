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

sys.path.insert(0, '/data/ap4909/30.10.2013-hot_cold_geochem/mantle_temp_cals/calculate_p_t_using_lee')
sys.path.insert(0, '/data/ap4909/30.10.2013-hot_cold_geochem/mantle_temp_cals/calculate_p_t_using_lee/aux_files')
import pet_read_in_with_labels
import katz_melt_frac,fractionate
import katz_adiabatic_eqns as ka
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


markers={"Southern_Marianas":".","South_Sandwich":"v","Costa_Rica":"8","Central_Aleutians":"s","Izu":"D","Kermadec":"*","South_Lesser_Antilles":"o","Tonga":"p","West_Aleutians":"h","New_Zealand":">","New_Britain":"x","North_Vanuatu_1":"+"}
#marker styles
colours={"Southern_Marianas":"b","South_Sandwich":"g","Costa_Rica":"r","Central_Aleutians":"c","Izu":"m","Kermadec":"k","South_Lesser_Antilles":"k","Tonga":"y","West_Aleutians":"w","New_Zealand":"m","New_Britain":"k","North_Vanuatu_1":"y"}
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
 

	
ave_t={"Fo=90":0,"Fo=91":0,"Fo=92":0}
num_t={"Fo=90":0,"Fo=91":0,"Fo=92":0}
ave_p={"Fo=90":0,"Fo=91":0,"Fo=92":0}
num_samps={0:0,2:0,4:0,6:0,8:0}
num_in_range={0:0,2:0,4:0,6:0,8:0}
for sub_zone in ["Southern_Marianas"]:
	
	
	
	labels=[]
	index=1
	samps=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/get_lat_lon_data/sz_with_lat_lon/individual_files/individual_files_with_feo/%s_new.xls"%(sub_zone),1,sub_zone)[0]
	#samps=pet_read_in_with_labels.pet_read_in("pt_files/sample_tester.csv")
	mineral_props={"Fo=92":{"ol":0.65,"opx":0.3,"cpx":0.05},"Fo=91":{"ol":0.65,"opx":0.25,"cpx":0.1},"Fo=90":{"ol":0.65,"opx":0.2,"cpx":0.15}}	#mineral proportions for fo90,fo91,fo92 mantle

	ax=plt.gca()
	#ax2=ax.twinx()
	x_vals=[]
	y_vals=[]
	
	for key,value in samps.iteritems():
		
		for h2o in [0.0,2,4,6,8.0]:
			
			
			
			for comp in [0.9,0.92]:
				
				l=value.lee_pt_decimal(comp,h2o,[0.1,0.2])
				
				if l[0][0]==0 and l[1][0]==0:
					est_ave_x=0
					est_ave_y=0
				elif l[0][0]==0 or l[1][0]==0:	#sometimes lee algorithm returns 0.0 for an oxygen fugacity - therefore average turns out to be half of the other fo2 P,T
					for i in l:
						if i[0] !=0:
		
							est_ave_x=i[0]
							est_ave_y=i[1]
				
					
					
					
						
							x_vals.append(est_ave_x)
							y_vals.append(est_ave_y)
			
				else:	#if two values are available for two different fo2's
					est_ave_x=(l[0][0]+l[1][0])/2.
					est_ave_y=(l[0][1]+l[1][1])/2.		
				
					x_vals.append(est_ave_x)
					y_vals.append(est_ave_y)
	
					x=np.array([est_ave_x])
					y=np.array([est_ave_y])
					ytop=np.array([abs(l[0][1]-est_ave_y)])
					ybot=ytop
					xtop=np.array([abs(l[0][0]-est_ave_x)])
					xbot=xtop
				plt.errorbar(est_ave_x,est_ave_y,yerr=(ybot,ytop),xerr=(xbot,xtop),lw=1,linestyle="None",c="r",capsize=5)
				if est_ave_y>5:
					print key
				if comp==0.9:	
					ax.plot(est_ave_x,est_ave_y,markersize=20,marker=markers[sub_zone],c=h2o_colours[h2o])#"%s"%comp_style
				elif comp==0.92:
					ax.plot(est_ave_x,est_ave_y,markersize=20,marker=markers[sub_zone],markerfacecolor='w',markeredgecolor=h2o_colours[h2o],markeredgewidth=2,)
				
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

for key in [0,2,4,6,8]:
	plt.plot(0,0,marker="s",c=h2o_colours[key],label="%s wt%% H$_2$O"%key)
for geotherm_sub_zone in["Tonga","Izu"]:
	try:	#print sub arc geotherm if available
	 	
		P,T,lab=pet_read_in.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/mantle_temp_cals/calculate_p_t_using_lee/pt_files/fluidity_mantle_geotherms/vwet_%s_sub_arc_geotherms.csv"%(geotherm_sub_zone))
	
		ax.plot(T,P,'-',linewidth=5,label=lab,color=colours[geotherm_sub_zone])
	except:
		print "error"

#Annotating plot
#solidi
plt.annotate("8 wt% H$_2$O solidus" ,xy = (1200,2.5),fontsize=20,color="blue",rotation=320)
plt.annotate("Dry solidus" ,xy = (1490,3.5),fontsize=20,rotation=320)
plt.annotate("Slab surface depth beneath arc" ,xy = (1200,3.95), xytext = (-20, 20),textcoords = 'offset points',fontsize=20)
plt.annotate("Crustal Thickness" ,xy = (1200,0.5), xytext = (-20, 20),textcoords = 'offset points',fontsize=20)
#adiabats
plt.annotate("1450 $^\circ$C" ,xy = (1480,0.5), xytext = (-20, 20),textcoords = 'offset points',fontsize=20,color='r')
plt.annotate("1300 $^\circ$C" ,xy = (1340,0.5), xytext = (-20, 20),textcoords = 'offset points',fontsize=20,color='r')
plt.annotate("Hollow - Mg# residue = 0.92" ,xy = (1470,1.5), xytext = (1488, 1.67),fontsize=30,arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Filled - Mg# residue = 0.90" ,xy = (1400,1), xytext = (1488, 1),fontsize=30,arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate("Bars - Uncertainty due to Fe$^{3+}$/Fe (0.1-0.2)" ,xy = (1400,2.2), xytext = (1350, 3),fontsize=30,arrowprops=dict(facecolor='black', shrink=0.05))
ax.invert_yaxis()
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])		
ax.legend(loc=3, numpoints=1)

plt.title("Range of P,T estimates for %s samples"%sub_zone.replace("_"," "))
cr_thickness=prem_pressure(-1000*all_params["Crustal Thickness (km) (12)"][sub_zone])*1e-9	#crustal thickness converted to pressure GPa
H=prem_pressure(-1000*all_params["H (km) (6)"][sub_zone])*1e-9 #H converted to pressure in GPa

for k in [cr_thickness,H]:	#plotting horizontal lines for slab and crustal depths
	crustal_d=[k,k]
	crustal_x=[0,2000]
	ax.plot(crustal_x,crustal_d,c="k",linestyle='--',linewidth=3)	
fs=20
#Plotting solidi
for h2o_sol,sol_col in zip([0.0,8.0],['k','b']):
	t_sols=[]
	p_sols=[]
	for p in np.linspace(0,6,1000):
		t_sols.append(katz_melt_frac.T_sol(p,h2o_sol))
		p_sols.append(p)
	plt.plot(t_sols,p_sols,'-',color='%s'%sol_col)
#plotting adiabat
for adiabat in [1300,1450]:
	adiabat_x=[]
	adiabat_y=[]
	for i in range(0,300,1):
	
		adiabat_x.append(adiabat+0.5*i)
	
		adiabat_y.append(prem_pressure(i*-1000)*1e-9)
	
	plt.plot(adiabat_x,adiabat_y,'-',color='r')
#plotting extreme geotherms
#plt.plot(max_T,max_P,'k')
#plt.plot(min_T,min_P,'k')
plt.xlim(1050,1650)
plt.ylim(6,0)
plt.tick_params(axis='both', which='major', labelsize=20)

ax.set_xlabel("Temperature ($^\circ$C)")
ax.set_ylabel("Pressure (GPa)")

fig1=plt.gcf()
fig1.set_size_inches(24, 12)
directory="figures/"+"p_t_plots/"#+"%s"%(comp.replace("=","_")) #%(sub_zone,comp.replace("=","_"))

if not os.path.exists(directory):
		os.makedirs(directory)



fig1.savefig("%sh2o_evaluation_%s.png"%(directory,sub_zone),bbox_inches='tight',dpi=(149))


#plt.show()
plt.clf()

	
