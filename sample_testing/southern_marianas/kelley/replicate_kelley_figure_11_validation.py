#Replicating figure 11, using kelley_mf_arc method in pet_read_in_with_labels
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


def kelley_mf_arc_their_format(F,cond):#finds melt fraction using eqn 4 from kelley 2010. cond in format [T,P], using the more "refractory" constants,Mantle source H2O as a function of P,T,F
			import math
			a=-5.1404654
			b=132.899012
			c=1159.66061#value from kelley 2010
			x=-136.88
			y=332.01
			Dh2o=0.012
			T=cond[0]
			P=cond[1]
			
			C0h2o=(Dh2o*(1-F)+F)*((T-(a*P**2+b*P+c)-(x*math.log(P)+y)*F)/-60)**1.85
			return C0h2o
def c0h2o(F,ClH2O):
	Dh2o=0.012
	return ClH2O*(Dh2o*(1-F)+F)
def kelley_mf_arc(props_name,cond,h2o):#finds melt fraction using eqn 4 from kelley 2010. cond in format [T,P], using the more "refractory" constants
			import math
			a=-5.1404654
			b=132.899012
			c=1159.66061#value from kelley 2010
			x=-136.88
			y=332.01
		
			
			return (-60.0*h2o**(1./1.85)-cond[0]+(a*cond[1]**2+b*cond[1]+c))/(-1*(x*math.log(cond[1])+y))

def kelley_mf_arc_root_finding(cond,h2o_bulk):#finds melt fraction using eqn 4 from kelley 2010. cond in format [T,P], using the more "refractory" constants
			import math
			from scipy.optimize import fsolve
			def mf_root_finding(Ff,P,T,h2o):#format for root finding for F
				a=-5.1404654
				b=132.899012
				
				c=1159.66061#value from kelley 2010
				x=-136.88
				y=332.01
		
			
				return Ff+(-60.0*(h2o/(0.012*(1-Ff)+Ff))**(1./1.85)-T+(a*P**2+b*P+c))/(math.log(P)+y)
			x0=fsolve(mf_root_finding,0,(cond[1],cond[0],h2o_bulk))[0]
			return x0

def kelley_mf_arc_root_finding_bulk_h2o(cond,h2o_bulk):#finds melt fraction using eqn 4 from kelley 2010. cond in format [T,P], using the more "refractory" constants
			import math
			from scipy.optimize import fsolve
			def mf_root_finding(Ff,P,T,h2o):#format for root finding for F
				a=-5.1404654
				b=132.899012
				
				c=1159.66061#value from kelley 2010
				x=-136.88
				y=332.01
		
				Dh2o=0.012
				return h2o_bulk-(Dh2o*(1-Ff)+Ff)*((T-(a*P**2+b*P+c)-(x*math.log(P)+y)*F)/-60)**1.85
			x0=fsolve(mf_root_finding,0,(cond[1],cond[0],h2o_bulk))[0]
			return x0
volcano_TP={"Agrigan":[1330,1.87],"Guguan":[1356,1.9],"Pagan":[1346,1.61],"Sarigan":[1260,1.14]}
volcano_colours={"Agrigan":"b","Guguan":"r","Pagan":"g","Sarigan":"m"}
for sub_zone in["Southern_Marianas"]:# 
		
	#samps1=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/get_lat_lon_data/sz_with_lat_lon/individual_files/individual_files_with_feo/%s_new.xls"%(sub_zone),1,sub_zone)[0]
	kelley_samps=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/sample_testing/southern_marianas/kelley/kelley_appendix_4_formatted.xls",0,sub_zone)[0]
	
	mineral_props={"Fo=92":{"ol":0.65,"opx":0.3,"cpx":0.05},"Fo=91":{"ol":0.65,"opx":0.25,"cpx":0.1},"Fo=90":{"ol":0.65,"opx":0.2,"cpx":0.15}}	#mineral proportions for fo90,fo91,fo92 mantle

	ax=plt.gca()
	#ax2=ax.twinx()
	latitudes=[]
	p_vals=[]
	mf_vals=[]
	for samps,symbol in zip([kelley_samps],["d"]):
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
							
							l=value.lee_pt_decimal_no_frac_correction(comp,h2o,[0.25,0.25])
							F=value.quick_mf(value.tio2,0.04,0.123)
							
							v_col=volcano_colours[value.pts["Volcano"]]
							#plt.plot(F,c0h2o(F,h2o),color=v_col,markersize=30,marker=symbol)
							
	plt.title("Source H2O versus melt fraction")
	
	fs=np.linspace(0,0.25,100)
	TP = volcano_TP["Guguan"]
	thermo_h2o=[]
	my_format_kelley_f=[]
	my_format_kelley_f_root=[]
	my_format_kelley_f_root_bulk_h2o=[]
	for f in fs:
		thermo_h2o.append(kelley_mf_arc_their_format(f,TP))
		h2o_liq=kelley_mf_arc_their_format(f,TP)/(f+0.012*(1-f))
		h2o_bulk=kelley_mf_arc_their_format(f,TP)
		print h2o_liq
		my_format_kelley_f_root.append(kelley_mf_arc_root_finding(TP,h2o_bulk))
		my_format_kelley_f_root_bulk_h2o.append(kelley_mf_arc_root_finding_bulk_h2o(TP,h2o_bulk))
		my_format_kelley_f.append(kelley_mf_arc(0.9,TP,h2o_liq))
	plt.plot(fs,thermo_h2o,"%s-"%volcano_colours["Guguan"])
	plt.plot(my_format_kelley_f_root,thermo_h2o,"%s*"%volcano_colours["Guguan"],markersize=7)
	plt.plot(my_format_kelley_f_root_bulk_h2o,thermo_h2o,"%s^"%volcano_colours["Guguan"],markersize=7)
	plt.plot(my_format_kelley_f,thermo_h2o,"b.",markersize=2)
		
#	print max(latitudes),max(latitudes)+(max(latitudes)-min(latitudes))*0.05
#	plt.xlim(min(latitudes)-(max(latitudes)-min(latitudes))*0.05,max(latitudes)+(max(latitudes)-min(latitudes))*0.05)
#	
#	plt.ylim(min(mf_vals)-(max(mf_vals)-min(mf_vals))*0.1,max(mf_vals)+(max(mf_vals)-min(mf_vals))*0.05)
	#setting up legend
#	for col,name in zip(["g",'none'],["Full symbol - Mg#=0.90","Hollow symbol - Mg#=0.92"]):
#		plt.scatter(0,0,label=name,marker="s",edgecolor="g",facecolors=col)
	
	plt.annotate("Sarigan",xy = (16.7,3),fontsize=30)
	plt.annotate("Guguan",xy = (17.4,3),fontsize=30)
	plt.annotate("Pagan",xy = (18,3),fontsize=30)
	plt.annotate("Agrigan",xy = (18.5,3),fontsize=30)
	plt.annotate("Hollow symbol",xy = (17.4,4),fontsize=30)
	ax=plt.gca()
	
	#box = ax.get_position()
	#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])		
	ax.legend(loc=3,numpoints=1,markerscale=6,fontsize=30,scatterpoints=1)
	
	plt.xlabel("Melt fraction",fontsize=40)
	plt.ylabel("C$_0$H2O",fontsize=40)
	
	plt.tick_params(axis='both', which='major', labelsize=30)
	fig1=plt.gcf()
	fig1.set_size_inches(24, 12)
	directory="figures/"+"mf_vs_lat/"+"dataset_comparison/"#+"%s"%(comp.replace("=","_")) #%(sub_zone,comp.replace("=","_"))
	if not os.path.exists(directory):
			os.makedirs(directory)
	
	print "%s%s.png"%(directory,sub_zone)
	#fig1.savefig("%s%s.png"%(directory,sub_zone),bbox_inches='tight',dpi=(149))
	
	plt.show()
	
	#plt.show()
