#Reads in T,P estimates at various conditions (estimated using Lee 2009) for individual samples and plots melt fractions calculated using the method of Katz 2003 versus melt fractions using Ti concs
import numpy as np
import matplotlib.pyplot as plt
import heapq
import operator
import sys
import os
import katz_adiabatic_eqns as ka
sys.path.insert(0, '/data/ap4909/30.10.2013-hot_cold_geochem/mantle_temp_cals/calculate_p_t_using_lee')
import pet_read_in_with_labels,katz_melt_frac,fractionate
import pet_read_in
from scipy.optimize import fsolve
dP=0.005 #pressure increment in GPa
point_size=100
annotate_samps=0#annotate samples by name
plot_aves=1
def annotate():
	plt.annotate(key[-10:],xy = (est_ave_x,est_ave_y), xytext = (-20, 20),textcoords = 'offset points', ha = 'right', va = 'bottom',arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
thickness_tp={}	#Dictionary to hold single subduction parameter
H_param={}

params_file=open("/data/ap4909/30.10.2013-hot_cold_geochem/code/sub_zone_params.csv",'r')
lines=params_file.readlines()
params=lines[0].split("\t")
for line in lines[1:]:
	words=line.split('\t')
	thickness_tp[words[0].replace("_"," ")]=float(eval(words[12]))
	H_param[words[0].replace("_"," ")]=float(eval(words[6]))
#USER INPUT#
for zone in ["Southern_Marianas"]:#,"South_Sandwich","Costa_Rica","Central_Aleutians","Izu","Kermadec","South_Lesser_Antilles","Tonga","West_Aleutians"]:
	ti_vals={}#dictionary to store average ti estimate 
	katz_vals={}
	fo_best={}
	pt_best={}
	samp_errors={} #stores lowest for each sample 
	done=0	#indicating whether first composition has been run through
	sub_zone="%s"%zone
	#Pressure function
	d_a=[ 0.,     3000.,    15000.,    24400.,    71000.,   171000.,   220000.,271000.,   371000.,   400000.,   471000.,   571000.,  670000.,   771000., 871000.,   971000.,  1071000.,  1171000.,  1271000.,  1371000.,  1471000.,1571000.,  1671000.,  1771000.,  1871000.,  1971000.,  2071000.,  2171000.,2271000.,  2371000., 2471000.,  2571000.,  2671000.,  2771000.,  2871000.,2891000.]	#PREM depths

	p_a=[  0.00000000e+00,   0.00000000e+00,   3.00000000e+08,   6.00000000e+08,  2.20000000e+09,   5.50000000e+09 ,  7.10000000e+09,   8.90000000e+09,   1.23000000e+10,   1.34000000e+10,   1.60000000e+10,   1.99000000e+10,   2.38000000e+10,   2.83000000e+10,  3.28000000e+10,   3.73000000e+10,   4.19000000e+10 ,  4.65000000e+10,   5.12000000e+10,  5.59000000e+10,  6.07000000e+10,   6.55000000e+10,7.04000000e+10,   7.54000000e+10,   8.04000000e+10,   8.55000000e+10,   9.06000000e+10,   9.58000000e+10,   1.01100000e+11,   1.06400000e+11,   1.11900000e+11,   1.17400000e+11,   1.23000000e+11,   1.28800000e+11 ,  1.34600000e+11,   1.35800000e+11]	#PREM pressures
	def prem_pressure(height):
		for prem_depth in range(1,len(d_a)):	#loops through depths, starting at index one
			if -height<=d_a[prem_depth]: #checks in which depth interval the height is 
				Pressure=((p_a[prem_depth]-p_a[prem_depth-1])/(d_a[prem_depth]-d_a[prem_depth-1]))*((-height)-d_a[prem_depth-1])+p_a[prem_depth-1]
				break
		return Pressure
	labels=[]
	index=1
	samps=pet_read_in_with_labels.pet_read_in("pt_files/%s_calculate_pt.csv"%(sub_zone))
	#samps=pet_read_in_with_labels.pet_read_in("testing/test1.csv")
	mineral_props={"Fo=92":{"ol":0.65,"opx":0.3,"cpx":0.05},"Fo=91":{"ol":0.65,"opx":0.25,"cpx":0.1},"Fo=90":{"ol":0.65,"opx":0.2,"cpx":0.15}}	#mineral proportions for fo90,fo91,fo92 mantle
	mant_vals={"Fo=92":{"Y":3.129,"La":0.134,"Ti":650.0},"Fo=91":{"Y":3.328,"La":0.192,"Ti":716.3},"Fo=90":{"Y":3.548,"La":0.253,"Ti":792.0}}#mantle concentrations for DDMM, Ave DMM and enriched DMM from workman and Hart 2005


	for comp in mant_vals.keys():
		
		for key,value in samps.iteritems():
			
			ti_est=[]# list to store ti melt fraction estimates at different h2os
			Y_est=[]# list to store Y melt fraction estimates at different h2os
			katz_est=[]# list to store major element melt fraction estimates at different h2os
			pt_sample={}
			
			#Plotting F estimates from element concs 	
			for h2o,h_col in zip([0.0,8.0],["g","b"]):	
				
				for l,marker,est_list in zip(value.mf(comp,mineral_props,mant_vals,h2o),["*","d","."],[ti_est,Y_est,katz_est]):
					
					#c=raw_input("h")
					
					if l[0]==0 and l[1]==0:
						
						est_list.append(0.0)
					elif l[0]==0 or l[1]==0:
						
						for i in l:
							if i !=0:
								
								est_list.append(i)
					else:
						
						katz_est_ave=(l[0]+l[1])/2.
						x=np.array([index])
						y=np.array([katz_est_ave])
						ytop=np.array([abs(l[0]-katz_est_ave)])
						ybot=ytop
						
								
						#plt.plot(index,katz_est_ave,"%s"%marker,markersize=10,c=h_col)
						
						est_list.append(katz_est_ave)
					#getting P,T conditions for sample
					cond=value.lee_pt(comp,h2o)
					
					if cond[0][0]==0 and cond[1][0]==0:
						pt_sample[h2o]=[0,0]
					if cond[0][0]==0 or cond[1][0]==0:	#sometimes lee algorithm returns 0.0 for an oxygen fugacity - therefore average turns out to be half of the other fo2 P,T
								
						for i in cond:
							if i[0]!=0:
							
								est_ave_x=i[0]
								est_ave_y=i[1]
								
								pt_sample[h2o]=[est_ave_x,est_ave_y]
					else:	#if two values are available for two different fo2's
						
						est_ave_x=(cond[0][0]+cond[1][0])/2.
						est_ave_y=(cond[0][1]+cond[1][1])/2.
						
						pt_sample[h2o]=[est_ave_x,est_ave_y]
			
			
			for lis,dic in zip((ti_est,katz_est),[ti_vals,katz_vals]):
				#print value.name, lis
				if len(lis)>1:
					dic[value.name]=(lis[0]+lis[1])/2.
				else:
					dic[value.name]=lis[0]
			error=abs(ti_vals[value.name]-katz_vals[value.name])
			if done==1:#samples have been looped through once already
				
				if error<samp_errors[value.name]:#smaller error
					
					for wa in (0.0,8.0):
						 
						pt_best[value.name][wa]=pt_sample[wa]
						print value.name,pt_best[value.name]
					fo_best[value.name]=comp
					samp_errors[value.name]=error
			elif done==0:
				pt_best[value.name]={}
				for wa in (0.0,8.0):
					#print pt_sample,value.name
					#c=raw_input("hel")
					
					
					pt_best[value.name][wa]=pt_sample[wa]
					fo_best[value.name]=comp
				#print pt_best[value.name]
				samp_errors[value.name]=error				
				
				
			index+=1
			labels.append(value.name[-10:])
		done=1#gone through samples once
	ax=plt.gca()
	if plot_aves==1:#plot average P,T for all samples that were formed at each Mg#
		for depl,col in zip(["Fo=90","Fo=91","Fo=92"],['b','r','k']):
			all_values_P=0
			all_values_T=0
			n=0
			for key,values in pt_best.iteritems():
				
				if fo_best[key]==depl and values[0.0][1]!=0:
					all_values_P+=values[0.0][1]
					all_values_T+=values[0.0][0]
					n+=1.0
			try:
				aveP=all_values_P/n
				aveT=all_values_T/n
				print depl, aveP,aveT
			except:
				continue
			plt.plot(aveT,aveP,c="%s"%col,marker='^',markersize=20)
	for key,values in pt_best.iteritems():
		print key,value, fo_best[key]
		
		c=raw_input("hello")
		if fo_best[key]=="Fo=90":
			for hyd in [0.0,8.0]:
				adi_T=[]
				adi_P=[]
				if hyd==0.0:
					ax.scatter(values[0.0][0],values[0.0][1],facecolors="r", edgecolors="r",s=point_size)
				elif hyd==8.0:
					ax.scatter(values[8][0],values[8][1],facecolors="b", edgecolors="b",s=point_size)
				est_ave_x=values[hyd][0]
				est_ave_y=values[hyd][1]
				adi_T.append(est_ave_x)
				adi_P.append(est_ave_y)
				if annotate_samps==1:
					annotate()
				while True:
					f=value.katz_mf(fo_best[key],mineral_props,[est_ave_x,est_ave_y],hyd)
		#						if comp=="Fo=90" and h2o==8 and f<0.3:
		#							print f,est_ave_x,ka.dt_dp(f,est_ave_y,est_ave_x,h2o)*dP
		#							c=raw_input('hello')

					if f==0.0:
						break
		#						print "hello"
		#						print ka.dt_dp(f,est_ave_y,est_ave_x,h2o)*dP
					est_ave_x=est_ave_x+ka.dt_dp(f,est_ave_y,est_ave_x,hyd)*dP
		
					est_ave_y=est_ave_y+dP
					adi_T.append(est_ave_x)
					adi_P.append(est_ave_y)
				
				plt.plot(adi_T,adi_P,"--",c="b")
		if fo_best[key]=="Fo=91":
			for hyd in [0.0,8.0]:
				adi_T=[]
				adi_P=[]
				if hyd==0.0:
					ax.scatter(values[0.0][0],values[0.0][1],facecolors="w", edgecolors="r",s=point_size)
				elif hyd==8.0:
					ax.scatter(values[8.0][0],values[8.0][1],facecolors="w", edgecolors="b",s=point_size)
				est_ave_x=values[hyd][0]
				est_ave_y=values[hyd][1]
				adi_T.append(est_ave_x)
				adi_P.append(est_ave_y)
				if annotate_samps==1:
					annotate()
				while True:
					f=value.katz_mf(fo_best[key],mineral_props,[est_ave_x,est_ave_y],hyd)
		#						if comp=="Fo=90" and h2o==8 and f<0.3:
		#							print f,est_ave_x,ka.dt_dp(f,est_ave_y,est_ave_x,h2o)*dP
		#							c=raw_input('hello')

					if f==0.0:
						break
		#						print "hello"
		#						print ka.dt_dp(f,est_ave_y,est_ave_x,h2o)*dP
					est_ave_x=est_ave_x+ka.dt_dp(f,est_ave_y,est_ave_x,hyd)*dP
		
					est_ave_y=est_ave_y+dP
					adi_T.append(est_ave_x)
					adi_P.append(est_ave_y)
	
				plt.plot(adi_T,adi_P,"--",c="b")
		
		
		if fo_best[key]=="Fo=92":
			for hyd in [0.0,8.0]:
				adi_T=[]
				adi_P=[]
				if hyd==0.0:
					ax.scatter(values[0.0][0],values[0.0][1],facecolors="r",marker="*", edgecolors="r",s=point_size)
				elif hyd==8.0:
					ax.scatter(values[8.0][0],values[8.0][1],facecolors="b",marker="*", edgecolors="b",s=point_size)
				est_ave_x=values[hyd][0]
				est_ave_y=values[hyd][1]
				adi_T.append(est_ave_x)
				adi_P.append(est_ave_y)
				if annotate_samps==1:
					annotate()
				while True:
					f=value.katz_mf(fo_best[key],mineral_props,[est_ave_x,est_ave_y],hyd)
		#						if comp=="Fo=90" and h2o==8 and f<0.3:
		#							print f,est_ave_x,ka.dt_dp(f,est_ave_y,est_ave_x,h2o)*dP
		#							c=raw_input('hello')

					if f==0.0:
						break
		#						print "hello"
		#						print ka.dt_dp(f,est_ave_y,est_ave_x,h2o)*dP
					est_ave_x=est_ave_x+ka.dt_dp(f,est_ave_y,est_ave_x,hyd)*dP
		
					est_ave_y=est_ave_y+dP
					adi_T.append(est_ave_x)
					adi_P.append(est_ave_y)
	
				plt.plot(adi_T,adi_P,"--",c="b")

	cr_thickness=prem_pressure(-1000*thickness_tp[sub_zone.replace("_"," ")])*1e-9	#crustal thickness converted to pressure GPa
	H=prem_pressure(-1000*H_param[sub_zone.replace("_"," ")])*1e-9 #H converted to pressure in GPa

	for k in [cr_thickness,H]:	#plotting horizontal lines for slab and crustla depths
		crustal_d=[k,k]
		crustal_x=[0,2000]
		ax.plot(crustal_x,crustal_d,c="k",linestyle='--',linewidth=3)	
	fs=20

	for h2o in [0.0,8.0]:
		t_sols=[]
		p_sols=[]
		for p in np.linspace(0,6,1000):
			t_sols.append(katz_melt_frac.T_sol(p,h2o))
			p_sols.append(p)
		plt.plot(t_sols,p_sols,'k')
	
	try:	#print sub arc geotherm if available
		
		P,T,lab=pet_read_in.pet_read_in("pt_files/fluidity_mantle_geotherms/vwet_%s_sub_arc_geotherms.csv"%(sub_zone))
		
		ax.plot(T,P,'-',c="y",linewidth=5,label=lab)
	except:
		print "error"
	ax.invert_yaxis()
	plt.xlim(900,1600)
	plt.ylim(6,0)
	ax.set_xlabel("Temperature ($^\circ$C)",fontsize=fs)
	ax.set_ylabel("Pressure (GPa)",fontsize=fs)
	plt.title("%s"%sub_zone.replace("_"," "))
	fig1=plt.gcf()
	directory="figures/best_fit"#+"%s"%(comp.replace("=","_")) #%(sub_zone,comp.replace("=","_"))
	if not os.path.exists(directory):
    			os.makedirs(directory)
	
	fig1.savefig("/home/ap4909/Dropbox/%s.png"%(zone))
	#fig1.savefig("%s/%s.png"%(directory,zone))
	plt.clf()
	#plt.show()		

