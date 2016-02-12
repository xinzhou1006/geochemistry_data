#Plot mf difference vs P, to see if deeper samples match better.
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
def T_sol_solid_h2o(P,h2o,A1=1159):#calculate solidus given h2o in solid
	
	A2=132.9
	A3=-5.1
	K=43.0
	gam=0.75
	D_h2o=0.01
	#melt_h2o=h2o/(D_h2o+F*(1-D_h2o))
	dt=K*h2o**gam
	return A1+A2*P+A3*P**2-dt

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

volcano_TP={"Agrigan":[1330,1.87],"Guguan":[1356,1.9],"Pagan":[1346,1.61],"Sarigan":[1260,1.14]}
volcano_colours={"Agrigan":"b","Guguan":"r","Pagan":"g","Sarigan":"m"}
for sub_zone in["Southern_Marianas"]:# 
		
	samps1=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/get_lat_lon_data/sz_with_lat_lon/individual_files/individual_files_with_feo/%s_new.xls"%(sub_zone),1,sub_zone)[0]
	kelley_samps=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/sample_testing/southern_marianas/kelley/kelley_appendix_4_formatted.xls",0,sub_zone)[0]
	
	mineral_props={"Fo=92":{"ol":0.65,"opx":0.3,"cpx":0.05},"Fo=91":{"ol":0.65,"opx":0.25,"cpx":0.1},"Fo=90":{"ol":0.65,"opx":0.2,"cpx":0.15}}	#mineral proportions for fo90,fo91,fo92 mantle

	ax=plt.gca()
	#ax2=ax.twinx()
	melt_diffs=[]
	p_vals=[]
	mf_vals=[]
	for samps,symbol in zip([samps1,kelley_samps],["s","d"]):
	#for samps,symbol in zip([samps1],["s"]):
		
		
		
		
		for h2o in [4]:



			for comp in [0.9]:
			
				n=0#number of samples
			
				i=0
				for key,value in samps.iteritems():
#					if symbol=="d":
#							
#						h2o=value.pts["H2O(WT%)"]
					
					
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
							F=value.quick_mf(value.tio2,0.09,0.123)
							p_vals.append(l[0][1])
							melt_diffs.append(F-value.kelley_mf_arc(comp,l[0],h2o))
							print F,value.kelley_mf_arc(comp,l[0],h2o)
							v_col=volcano_colours[value.pts["Volcano"]]
							#plt.plot(l[0][1],F,color='k',markersize=30,marker=symbol,label="Ti kelley" if i==0 else "")
							print value.katz_mf(comp,0.12,l[0],h2o)
							katz_mf,cpx_out=value.katz_mf(comp,0.12,l[0],h2o)
							
							if cpx_out==1:
								plt.plot(l[0][0]-T_sol_solid_h2o(l[0][1],h2o,A1=1085.7),katz_mf,markeredgecolor='g',markerfacecolor='None',markersize=30,marker=symbol,label="Kelley samples, katz" if i==0 else "")
							elif cpx_out==0:
								plt.plot(l[0][0]-T_sol_solid_h2o(l[0][1],h2o,A1=1085.7),katz_mf,color='g',markersize=30,marker=symbol,label="Kelley samples,katz" if i==0 else "")
							plt.plot(l[0][0]-T_sol_solid_h2o(l[0][1],h2o,A1=1085.7),value.kelley_mf_arc(comp,l[0],h2o),color='r',markersize=30,marker=symbol,label="Kelley samples, kelley" if i==0 else "")
						elif symbol=="s":
							ti_corrected=value.get_ti_corrected(0.9,h2o,0.25)
							l=value.lee_pt_decimal(comp,h2o,[0.25,0.25])
							#plt.plot(l[0][1],value.quick_mf(ti_corrected,0.09,0.123),color='k',markersize=30,marker=symbol,label="My samples" if i==0 else "")
							print value.katz_mf(comp,0.12,l[0],h2o)
							katz_mf,cpx_out=value.katz_mf(comp,0.12,l[0],h2o)
							if cpx_out==1:
								plt.plot(l[0][0]-T_sol_solid_h2o(l[0][1],h2o,A1=1085.7),katz_mf,markeredgecolor='g',markerfacecolor='None',markersize=30,marker=symbol,label="My samples, Katz" if i==0 else "")
							elif cpx_out==0:
								plt.plot(l[0][0]-T_sol_solid_h2o(l[0][1],h2o,A1=1085.7),katz_mf,color='g',markersize=30,marker=symbol,label="My samples Katz" if i==0 else "")
							plt.plot(l[0][0]-T_sol_solid_h2o(l[0][1],h2o,A1=1085.7),value.kelley_mf_arc(comp,l[0],h2o),color='r',markersize=30,marker=symbol,label="My samples kelley" if i==0 else "")
					i+=1			
	plt.title("Kelley, katz MF, assumed cpx 0.12")
	
	print np.corrcoef(p_vals,melt_diffs)
	
		
		
#	print max(latitudes),max(latitudes)+(max(latitudes)-min(latitudes))*0.05
#	plt.xlim(min(latitudes)-(max(latitudes)-min(latitudes))*0.05,max(latitudes)+(max(latitudes)-min(latitudes))*0.05)
#	
#	plt.ylim(min(mf_vals)-(max(mf_vals)-min(mf_vals))*0.1,max(mf_vals)+(max(mf_vals)-min(mf_vals))*0.05)
	#setting up legend
#	for col,name in zip(["g",'none'],["Full symbol - Mg#=0.90","Hollow symbol - Mg#=0.92"]):
#		plt.scatter(0,0,label=name,marker="s",edgecolor="g",facecolors=col)
	#for col,name in zip(["g",'none'],["Full symbol - Mg#=0.90","Hollow symbol - Mg#=0.92"]):
	#plt.plot(l[0][1],value.quick_mf(ti_corrected,0.09,0.123)-value.kelley_mf_arc(comp,l[0],h2o),color='c',markersize=30,marker=symbol)
	
	
	ax=plt.gca()
	
	#box = ax.get_position()
	#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])		
	ax.legend(loc=4,numpoints=1,markerscale=1,fontsize=30,scatterpoints=1)
	
	plt.xlabel("T-Tsol 4wt%",fontsize=40)
	plt.ylabel("Melt fractions ",fontsize=40)
	
	plt.tick_params(axis='both', which='major', labelsize=30)
	fig1=plt.gcf()
	fig1.set_size_inches(24, 12)
	directory="figures/"+"melt_fractions/"#+"%s"%(comp.replace("=","_")) #%(sub_zone,comp.replace("=","_"))
	if not os.path.exists(directory):
			os.makedirs(directory)
	
	
	fig1.savefig("%skatz_kelley_mf_vs_t_minus_tsol.png"%(directory),bbox_inches='tight',dpi=(149))
	
	plt.show()
	
	#plt.show()
