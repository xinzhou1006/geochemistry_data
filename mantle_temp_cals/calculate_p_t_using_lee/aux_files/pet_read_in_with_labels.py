def pet_read_in(pet_file,sample_subset,sub_zone):#takes in file containing samples with estimates of P,T using various assumptions of H2O, fo2
	import try_strings
	import numpy as np
	class Sample:	#class for a rock sample; stores the different P,T estimates, F, TiO2
		def __init__(self,name,pts):#,fo90_0,fo90_8,fo92_0,fo92_8,name):#,fo92_0,fo92_8,tio2):
			
			self.pts=pts
			self.name=name
			self.tio2=try_strings.try_strings(["TIO2(WT%)","TIO2(WT%): altern. values or methods","TIO2(WT%): altern. values and methods"],self.pts)
			#self.eu_anomaly()
			self.fo2_vals=[0.15,0.15]
			#self.tio2=self.pts[]
			self.Y=try_strings.try_strings(["Y(PPM)","Y(PPB)","Y(PPM): altern. values or methods","Y(PPB): altern. values or methods","Y(PPB): altern. values and methods","Y(PPM): altern. values and methods"],self.pts)
			#self.La=self.pts["La"]
			self.La_D={"ol":0.0,"opx":0.0008,"cpx":0.071}#distribution coeffs 
			self.Y_D={"ol":1e-3,"opx":0.086,"cpx":0.76}
			self.ti_D={"ol":0.01,"opx":0.24,"cpx":0.34}
		def lee_pt(self,props_name,h2o):	#method to calculate lee p and t only
			self.values=[]#store P,T calculations at fo2=0.05,0.15
			
			for fo2 in self.fo2_vals: 
				vals,ticorrected=self.frac(h2o,fo2,float(props_name[3:])*0.01)
				self.values.append(vals)
			return self.values
		def lee_pt_decimal(self,props_name,h2o,fo2_values):	#method to calculate lee p and t only; takes mg# input as decimal not e.g. "Fo=90"
			self.values=[]#store P,T calculations at fo2=0.05,0.15
			self.fo2_vals=fo2_values
			for fo2 in self.fo2_vals:
#				if self.pts["H2O(WT%)"]!='':
#					h2o=float(self.pts["H2O(WT%)"])
					
				vals,ticorrected=self.frac(h2o,fo2,float(props_name))
				self.values.append(vals)
			return self.values
		def lee_pt_decimal_no_frac_correction(self,props_name,h2o,fo2_values):	#method to calculate lee p and t only; takes mg# input as decimal not e.g. "Fo=90"
			self.values=[]#store P,T calculations at fo2=0.05,0.15
			self.fo2_vals=fo2_values
			import fractionate_without_ol_correction
			for fo2 in self.fo2_vals:
#				if self.pts["H2O(WT%)"]!='':
#					h2o=float(self.pts["H2O(WT%)"])
				
			
				vals,ticorrected=fractionate_without_ol_correction.fractionate(self.pts,h2o,fo2,props_name)	#fractionate(ele_d,h2o,fo2,Fo,Kd_var=1,mass_inc):#ele_d=dict of element concentrations,h2o=h2o content of melt, fo2=oxidation of mantle,Fo=forsterite content of mantle,Kd_var (1=variable Kd, 0 =non variable Kd), mass increment
					
				
				self.values.append(vals)
			return self.values
		def get_ti_corrected(self,props_name,h2o,fo2_val):#find ti after fractionation correction
			
					
			vals,ticorrected=self.frac(h2o,fo2_val,float(props_name))
			
			return ticorrected
		def get_majors_corrected(self,props_name,h2o,fo2):#return major elements after fractionation correction  
			import fractionate_return_major_eles_after_correction	
			
			majors=fractionate_return_major_eles_after_correction.fractionate(self.pts,h2o,fo2[0],props_name)	#fractionate(ele_d,h2o,fo2,Fo,Kd_var=1,mass_inc):#ele_d=dict of element concentrations,h2o=h2o content of melt, fo2=oxidation of mantle,Fo=forsterite content of mantle,Kd_var (1=variable Kd, 0 =non variable Kd), mass increment
			
			return majors
		def quick_mf(self,tio2_val,bulk_ti_D,mantle_conc):#quick melt fraction calculation. tio2/mantle conc in WT%
			mantle_conc=(((47.87/79.87)*mantle_conc)/100.)*1000000.
			ti_ppm=(((47.87/79.87)*tio2_val)/100.)*1000000.
			if tio2_val!=0:	#checking to see if sample has an associated measurement; if not then F=0
					ti_F=(((mantle_conc/ti_ppm)-bulk_ti_D)/(1-bulk_ti_D))

			else:
					ti_F=(0.0)
			return ti_F
		def mineral_mode(self,F,P,mineral):#determine modal percentage of mineral in peridotite as function of P and F, from Kimura 2014 HAMMS paper
			constants={"ol":{"a1":0.00613623096805815,"b1":-0.142729577262952,"c1":0.307582515267056,"a2":-0.000449696957517176,"b2":0.331962655891289,"c2":52.0537726003922},"cpx":{"a1":0.0070784855111945,"b1":-0.0663641108143835,"c1":-0.71962524540918,"a2":-0.0747969128013182,"b2":4.31230108067626,"c2":14.0009285227413},"opx":{"a1":0.0519974059012713,"b1":-0.0614682207223662,"c1":-0.352497204418404,"a2":-2.17575579689427,"b2":3.09302747908336,"c2":27.920850943118}}
			
			a=constants[mineral]["a1"]*P**2+constants[mineral]["b1"]*P+constants[mineral]["c1"]
			b=constants[mineral]["a2"]*P**2+constants[mineral]["b2"]*P+constants[mineral]["c2"]
			Xa=a*F*100+b
			if Xa>0:
				return Xa/100.
			else:
				return 0.0
		def best_fit_fo_graded(self,h2o):#finds best fit Fo content 
			self.mant_vals={"Fo=92":{"Y":3.129,"La":0.134,"Ti":650.0},"Fo=91":{"Y":3.328,"La":0.192,"Ti":716.3},"Fo=90":{"Y":3.548,"La":0.253,"Ti":792.0}}
			self.mineral_props={"Fo=92":{"ol":0.65,"opx":0.3,"cpx":0.05},"Fo=91":{"ol":0.65,"opx":0.25,"cpx":0.1},"Fo=90":{"ol":0.65,"opx":0.2,"cpx":0.15}}
			
			errors=[]
			melt_vals=[]
			P_vals=[]
			T_vals=[]
			fo_vals=[0.90,0.91,0.92]
			for comp in ["Fo=90","Fo=91","Fo=92"]:
				ti_melt_est_vals,Y_est,katz_melt_est_vals=self.mf(comp,self.mineral_props,self.mant_vals,h2o)
				if 0 in ti_melt_est_vals:
					for z in ti_melt_est_vals:
						if z!=0:
							ti_melt_est=z
				else:
					ti_melt_est=(ti_melt_est_vals[0]+ti_melt_est_vals[1])/2.
				
				
				if 0 in katz_melt_est_vals:
					for z in katz_melt_est_vals:
						if z!=0:
							katz_melt_est=z
				else:
					katz_melt_est=(katz_melt_est_vals[0]+katz_melt_est_vals[1])/2.
			
				
				#print value.mf(comp,mineral_props,mant_vals,h2o)[2]
				#katz_melt_est=(value.mf(comp,mineral_props,mant_vals,0.0)[2])+np.mean(value.mf(comp,mineral_props,mant_vals,8.0)[2]))/2
				melt_vals.append(ti_melt_est)
				new_error=ti_melt_est-katz_melt_est
				errors.append(new_error)
				ave_p=(self.lee_pt(comp,h2o)[0][1]+self.lee_pt(comp,h2o)[1][1])/2.
				ave_t=(self.lee_pt(comp,h2o)[0][0]+self.lee_pt(comp,h2o)[1][0])/2.
				P_vals.append(ave_p)
				T_vals.append(ave_t)
				
			
			
			graded_fo=np.interp(0,errors,fo_vals)
			
			melt_interp=np.interp(graded_fo,fo_vals,melt_vals)
			P_interp=np.interp(graded_fo,fo_vals,P_vals)
			T_interp=np.interp(graded_fo,fo_vals,T_vals)
			return graded_fo,melt_interp,P_interp,T_interp
		def kelley_best_fit_fo_graded(self,h2o):#finds best fit Fo content using equation 4 from Kelley 2010 for F(P,T,h2o); used to compare against Katz parametrization
			self.mant_vals={"Fo=92":{"Y":3.129,"La":0.134,"Ti":650.0},"Fo=91":{"Y":3.328,"La":0.192,"Ti":716.3},"Fo=90":{"Y":3.548,"La":0.253,"Ti":792.0}}
			self.mineral_props={"Fo=92":{"ol":0.65,"opx":0.3,"cpx":0.05},"Fo=91":{"ol":0.65,"opx":0.25,"cpx":0.1},"Fo=90":{"ol":0.65,"opx":0.2,"cpx":0.15}}
			
			errors=[]
			melt_vals=[]
			P_vals=[]
			T_vals=[]
			fo_vals=[0.90,0.91,0.92]
			for comp in ["Fo=90","Fo=91","Fo=92"]:
				ti_melt_est_vals,Y_est,katz_melt_est_vals=self.mf(comp,self.mineral_props,self.mant_vals,h2o)
				a=self.kelley_mf(comp,self.lee_pt(comp,h2o)[1][::-1],h2o)
				kelley_melt_est_vals=[a,a]
				if 0 in ti_melt_est_vals:
					for z in ti_melt_est_vals:
						if z!=0:
							ti_melt_est=z
				else:
					ti_melt_est=(ti_melt_est_vals[0]+ti_melt_est_vals[1])/2.
				
				
				if 0 in kelley_melt_est_vals:
					for z in kelley_melt_est_vals:
						if z!=0:
							kelley_melt_est=z
				else:
					kelley_melt_est=(kelley_melt_est_vals[0]+kelley_melt_est_vals[1])/2.
			
				
				#print value.mf(comp,mineral_props,mant_vals,h2o)[2]
				#katz_melt_est=(value.mf(comp,mineral_props,mant_vals,0.0)[2])+np.mean(value.mf(comp,mineral_props,mant_vals,8.0)[2]))/2
				melt_vals.append(ti_melt_est)
				new_error=ti_melt_est-kelley_melt_est
				errors.append(new_error)
				ave_p=(self.lee_pt(comp,h2o)[0][1]+self.lee_pt(comp,h2o)[1][1])/2.
				ave_t=(self.lee_pt(comp,h2o)[0][0]+self.lee_pt(comp,h2o)[1][0])/2.
				P_vals.append(ave_p)
				T_vals.append(ave_t)
				
			
			
			graded_fo=np.interp(0,errors,fo_vals)
			
			melt_interp=np.interp(graded_fo,fo_vals,melt_vals)
			P_interp=np.interp(graded_fo,fo_vals,P_vals)
			T_interp=np.interp(graded_fo,fo_vals,T_vals)
			return graded_fo,melt_interp,P_interp,T_interp
		def mf(self,props_name,props,mantle_concs,h2o):#method to calculate melt fractions from Ti,Y,La concs
			
			self.katz_est=[]
			self.ti_F=[]	
			self.Y_F=[]	
			for fo2 in self.fo2_vals: 	
			
				vals,self.ticorrected=self.frac(h2o,fo2,float(props_name[3:])*0.01)	
				
				self.ti=(((47.87/79.87)*self.ticorrected)/100.)*1000000.#converting to ppm
					
				self.bulk_ti_D=props[props_name]["ol"]*self.ti_D["ol"]+props[props_name]["opx"]*self.ti_D["opx"]+props[props_name]["cpx"]*self.ti_D["cpx"]
			 	#self.bulk_ti_D=0.04	
				#self.bulk_La_D=props[props_name]["ol"]*self.La_D["ol"]+props[props_name]["opx"]*self.La_D["opx"]+props[props_name]["cpx"]*self.La_D["cpx"]
				
				self.bulk_Y_D=props[props_name]["ol"]*self.Y_D["ol"]+props[props_name]["opx"]*self.Y_D["opx"]+props[props_name]["cpx"]*self.Y_D["cpx"]
				
				if self.ti!=0:	#checking to see if sample has an associated measurement; if not then F=0
					self.ti_F.append(((mantle_concs[props_name]["Ti"]/self.ti)-self.bulk_ti_D)/(1-self.bulk_ti_D))

				else:
					self.ti_F.append(0.0)
				#if self.La!=0:#checking to see if sample has an associated measurement; if not then F=0
				#	self.La_F[props_name]=((mantle_concs[props_name]["La"]/self.La)-self.bulk_La_D)/(1-self.bulk_La_D)
					
				#c=raw_input("hello")	
				#else:
				#	self.La_F[props_name]=0.0
				if self.Y!=0 and self.Y!='' and self.Y is not None:
					
					self.Y_F.append(((mantle_concs[props_name]["Y"]/self.Y)-self.bulk_Y_D)/(1-self.bulk_Y_D))
				else:
					self.Y_F.append(0.0)
				
				self.katz_est.append(self.katz_mf(props_name,props,vals,h2o))	
				#self.katz_est.append(self.kelley_mf(props_name,vals,h2o))
#				if props_name=="Fo=92" and h2o==8.0:

#					c=raw_input("hello")
			return self.ti_F,self.Y_F,self.katz_est
			#return self.ti_F,self.La_F,self.Y_F
		def mf_non_modal_batch(self,props_name,mantle_conc,h2o):#method to calculate melt fractions from Ti concs using non-modal batch melting
			self.katz_est=[]
			self.ti_F=[]	
				
			for fo2 in self.fo2_vals: 	
				
				vals,self.ticorrected=self.frac(h2o,fo2,props_name)	
				
				self.ti=(((47.87/79.87)*self.ticorrected)/100.)*1000000.#converting to ppm
				
				#self.bulk_ti_D_0=mineral_mode(f,P,"ol")*self.ti_D["ol"]+mineral_mode(f,P,"opx")*self.ti_D["opx"]+mineral_mode(f,P,"cpx")*self.ti_D["cpx"]
			 	self.bulk_ti_D=0.09	
				
				
				if self.ti!=0:	#checking to see if sample has an associated measurement; if not then F=0
					self.ti_F.append(((mantle_conc/self.ti)-self.bulk_ti_D)/(1-self.bulk_ti_D))

				else:
					self.ti_F.append(0.0)
				
				
				#self.katz_est.append(self.katz_mf(props_name,props,vals,h2o))	
				#self.katz_est.append(self.kelley_mf(props_name,vals,h2o))
#				if props_name=="Fo=92" and h2o==8.0:
#					print self.pts,fo2,h2o,float(props_name[3:])*0.01
#					print self.ti_F, self.name,vals
#					print self.ti,ticorrected
#					c=raw_input("hello")
			return self.ti_F#,self.Y_F,self.katz_est
			#return self.ti_F,self.La_F,self.Y_F
			
		def katz_mf(self,mg_num,cpx_mode,cond,h2o):	#calculates melt fraction as in Katz 2003. props_name=mineralogy of mantle 
			from scipy.optimize import fsolve
			import katz_melt_frac
			if cond[0]!=0.0 or cond[1]!=0.0:# if not an empty P,T,H2O estimate in file
				CPX_OUT=0
				A_val=1085.7	
				
				self.x0=fsolve(katz_melt_frac.mf_root_finding,0,(cond[1],cond[0],h2o,A_val))[0]
				if self.x0==0:
					print "Katz_melt_frac_error",self.name,cond[1],cond[0],h2o,props_name
					
		
				if self.x0>self.fcpx_out(cond[1],{"cpx":cpx_mode}):
					CPX_OUT=1
					self.x0=katz_melt_frac.mf_opx(cond[1],cond[0],self.fcpx_out(cond[1],{"cpx":cpx_mode}),h2o,A_val)
				
			else:
				return 0.0
			return self.x0,CPX_OUT
		def katz_mf_kelley_solidus(self,mg_num,cpx_mode,cond,h2o):	#calculates melt fraction as in Katz 2003. props_name=mineralogy of mantle 
			from scipy.optimize import fsolve
			import katz_melt_frac
			if cond[0]!=0.0 or cond[1]!=0.0:# if not an empty P,T,H2O estimate in file
				
				A_val=1159.66061	
				
				self.x0=fsolve(katz_melt_frac.mf_root_finding,0,(cond[1],cond[0],h2o,A_val))[0]
				if self.x0==0:
					print "Katz_melt_frac_error",self.name,cond[1],cond[0],h2o,props_name
					
		
				if self.x0>self.fcpx_out(cond[1],{"cpx":cpx_mode}):
					
					self.x0=katz_melt_frac.mf_opx(cond[1],cond[0],self.fcpx_out(cond[1],{"cpx":cpx_mode}),h2o,A_val)
				
			else:
				return 0.0
			return self.x0
		def katz_mf_without_cpx_out(self,mg_num,cpx_mode,cond,h2o):	#calculates melt fraction as in Katz 2003. props_name=mineralogy of mantle 
			from scipy.optimize import fsolve
			import katz_melt_frac
			if cond[0]!=0.0 or cond[1]!=0.0:# if not an empty P,T,H2O estimate in file
				CPX_OUT=0
				A_val=1085.7	
				
				self.x0=fsolve(katz_melt_frac.mf_root_finding,0,(cond[1],cond[0],h2o,A_val))[0]
				if self.x0==0:
					print "Katz_melt_frac_error",self.name,cond[1],cond[0],h2o,props_name
		
		
				
			else:
				return 0.0
			return self.x0
		def katz_mf_new(self,mg_num,cpx_mode,cond,h2o):	#calculates melt fraction as in Katz 2003. props_name=mineralogy of mantle 
			from scipy.optimize import fsolve
			import katz_melt_frac
			mg_nums=[0.893419654,0.9010621194,0.9184344261]
			A_vals=[1085.7,1122.65,1159.6]
			
			if cond[0]!=0.0 or cond[1]!=0.0:# if not an empty P,T,H2O estimate in file
				A_val=np.interp(mg_num,mg_nums,A_vals)
				
				self.x0=fsolve(katz_melt_frac.mf_root_finding,0,(cond[1],cond[0],h2o,A_val))[0]
				
				if self.x0==0:
					print "Katz_melt_frac_error",self.name,cond[1],cond[0],h2o,mg_num
					
		
				if self.x0>self.fcpx_out(cond[1],{"cpx":cpx_mode}):
					
					self.x0=katz_melt_frac.mf_opx(cond[1],cond[0],self.fcpx_out(cond[1],{"cpx":cpx_mode}),h2o,A_val)
			else:
				return 0.0
			return self.x0
		def graded_kelley_mf(self,best_props,cond,h2o):#takes in best fit Mg# and finds melt fraction using eqn 4 from kelley 2010
			import math
			a=-5.1404654
			b=132.899012
			c=np.interp(best_props,[0.90,0.92],[1120.66061,1159.6])
			x=np.interp(best_props,[0.90,0.92],[-221.34,-136.88])
			y=np.interp(best_props,[0.90,0.92],[536.86,332.01])
			
			return (-60.0*h2o**(1./1.85)-cond[0]+(a*cond[1]**2+b*cond[1]+c))/(-1*(math.log(cond[1])+y))	
		def kelley_mf(self,props_name,cond,h2o):#finds melt fraction using eqn 4 from kelley 2010. cond in format [T,P]
			import math
			a=-5.1404654
			b=132.899012
			if cond[0]!=0.0 or cond[1]!=0.0:# if not an empty P,T,H2O estimate in file
				if props_name==0.92:
						c=1159.66061#value from kelley 2010
						x=-136.88
						y=332.01
				else:
						c=1120.66061
						x=-221.34
						y=536.86
			else:
				return 0.0
			return (-60.0*h2o**(1./1.85)-cond[0]+(a*cond[1]**2+b*cond[1]+c))/(-1*(math.log(cond[1])+y))
		def kelley_mf_arc(self,props_name,cond,h2o):#finds melt fraction using eqn 4 from kelley 2010. cond in format [T,P], using the more "refractory" constants
			import math
			a=-5.1404654
			b=132.899012
			
			if cond[0]!=0.0 or cond[1]!=0.0:# if not an empty P,T,H2O estimate in file
				
				c=1159.66061#value from kelley 2010
				x=-136.88
				y=332.01
		
			else:
				return 0.0
			return (-60.0*h2o**(1./1.85)-cond[0]+(a*cond[1]**2+b*cond[1]+c))/(-1*(x*math.log(cond[1])+y))
		def kelley_mf_arc_root_finding(self,props_name,cond,h2o):#finds melt fraction using eqn 4 from kelley 2010. cond in format [T,P], using the more "refractory" constants
			import math
			from scipy.optimize import fsolve
			def mf_root_finding(F,P,T,h2o):#format for root finding for F
				a=-5.1404654
				b=132.899012
				
				c=1159.66061#value from kelley 2010
				x=-136.88
				y=332.01
		
			
				return F+(-60.0*h2o**(1./1.85)-T+(a*P**2+b*P+c))/(math.log(P)+y)
			x0=fsolve(mf_root_finding,0,(cond[1],cond[0],h2o))[0]
			
		def kelley_mf_arc_their_format(self,F,cond):#finds melt fraction using eqn 4 from kelley 2010. cond in format [T,P], using the more "refractory" constants,Mantle source H2O as a function of P,T,F
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
		def kelley_mf_arc_with_cpx_out(self,props_name,cond,h2o,cpx_mode):#finds melt fraction using eqn 4 from kelley 2010. cond in format [T,P], using the more "refractory" constants
			import math
			
			import katz_melt_frac
			a=-5.1404654
			b=132.899012
			
			
				
			c=1159.66061#value from kelley 2010
			x=-136.88
			y=332.01
		
			print cond[1]
			print math.log(cond[1])
			x0= (-60.0*h2o**(1./1.85)-cond[0]+(a*cond[1]**2+b*cond[1]+c))/(-1*(x*math.log(cond[1])+y))
			if x0>self.fcpx_out(cond[1],{"cpx":cpx_mode}):
				print x0	
				x0=katz_melt_frac.mf_opx(cond[1],cond[0],0.1,h2o,1085)
			
			return x0	
		def eu_anomaly(self): #Eu anomaly as defined in Turner and Langmuir 2015, test for mixed evolved and primitive magmas
			import chondrite_comp
			
			Eu=try_strings.try_strings(["EU(PPM)","EU(PPB)","EU(PPM): altern. values or methods","EU(PPB): altern. values or methods","EU(PPB): altern. values and methods","EU(PPM): altern. values and methods"],self.pts)
			Sm=try_strings.try_strings(["SM(PPM)","SM(PPB)","SM(PPM): altern. values or methods","SM(PPB): altern. values or methods","SM(PPB): altern. values and methods","SM(PPM): altern. values and methods"],self.pts)
			Gd=try_strings.try_strings(["GD(PPM)","GD(PPB)","GD(PPM): altern. values or methods","GD(PPB): altern. values or methods","GD(PPB): altern. values and methods","GD(PPM): altern. values and methods"],self.pts)
			Tb=try_strings.try_strings(["TB(PPM)","TB(PPB)","TB(PPM): altern. values or methods","TB(PPB): altern. values or methods","TB(PPB): altern. values and methods","TB(PPM): altern. values and methods"],self.pts)
			
			if Gd is not None and Sm is not None and Eu is not None: #np.isnan(Gd)== False:
				self.eu_anom=(Eu/chondrite_comp.concs["EU"])/(((Sm/chondrite_comp.concs["SM"])+(Gd/chondrite_comp.concs["GD"]))/2.)
				
			elif  Gd is None and Tb is not None and Eu is not None:#np.isnan(Gd)== True:
				self.eu_anom=chondrite_comp.concs["EU"]/((2*(Sm/chondrite_comp.concs["SM"])+(Tb/chondrite_comp.concs["TB"]))/3.)
				
			else:
				self.eu_anom=np.nan	
				
		def fcpx_out(self,P,comp):
			
			#print comp
			Mcpx=comp["cpx"]
				
			#r0=0.446
			
			self.r0=0.45	
			self.r1=0.08
			return Mcpx/(self.r0+self.r1*P)
		def frac(self,h2o,fo2,Fo):
			import fractionate
			
			prt,TiO2_corrected=fractionate.fractionate(self.pts,h2o,fo2,Fo)	#fractionate(ele_d,h2o,fo2,Fo,Kd_var=1,mass_inc):#ele_d=dict of element concentrations,h2o=h2o content of melt, fo2=oxidation of mantle,Fo=forsterite content of mantle,Kd_var (1=variable Kd, 0 =non variable Kd), mass increment
			return prt,TiO2_corrected
		def return_trace_ele_ratio(self,ratio):#takes in ratio that wants to found as string and calculates
			
			try:
				up,low=ratio.split('/')
				up=up.strip()
			
				low=low.strip()
				up= up.upper()
				low=low.upper()
				
				up_val=try_strings.try_strings(["%s(PPM)"%up,"%s(PPB)"%up,"%s(PPM): altern. values or methods"%up,"%s(PPB): altern. values or methods"%up,"%s(PPB): altern. values and methods"%up,"%s(PPM): altern. values and methods"%up],self.pts)
				low_val=try_strings.try_strings(["%s(PPM)"%low,"%s(PPB)"%low,"%s(PPM): altern. values or methods"%low,"%s(PPB): altern. values or methods"%low,"%s(PPB): altern. values and methods"%low,"%s(PPM): altern. values and methods"%low],self.pts)
				if up_val is None or low_val is None:
					return np.nan
				if up_val ==0 or low_val ==0:
					return np.nan
				else:
					return up_val/low_val
			except ValueError:#when only one element is specified:ratio.split('/')returns ValueError
				ratio=ratio.strip()
				ratio= ratio.upper()
				print ratio
				up_val=try_strings.try_strings(["%s(PPM)"%ratio,"%s(PPB)"%ratio,"%s(PPM): altern. values or methods"%ratio,"%s(PPB): altern. values or methods"%ratio,"%s(PPB): altern. values and methods"%ratio,"%s(PPM): altern. values and methods"%ratio,"%s(WT%%): altern. values and methods"%ratio,"%s(WT%%)"%ratio],self.pts)
				
				if up_val is None:
					return np.nan
				if up_val ==0:
					return np.nan
				else:
					return up_val
			
	import matplotlib.pyplot as plt
	import samples_to_use,samples_not_to_use
	from collections import OrderedDict
	from xlrd import open_workbook
	wb = open_workbook('%s'%pet_file, on_demand=True)#on_demand=True means sheets are only loaded in if requested
	sheet = wb.sheet_by_name("Sheet1")
	
	samples={}
	samples=OrderedDict(samples)
	
	eles_index={}
	eles_index=OrderedDict(eles_index)
	header=[]
	index=0
	for cell in sheet.row(0):#looping through first row to get header and indices
		val=cell.value
		header.append(val.strip())
		
		if val!='':
			eles_index[val]=index
			
		index+=1
	

	
	for row_index in range(sheet.nrows)[1:]:#looping through the rows of sheet
		
		eles={}
		eles=OrderedDict(eles)
		row=sheet.row(row_index)
		 
		
		row_list=[]	
		for u in row:#getting values for the rows
			row_list.append(u.value)
		
		if sample_subset==1:#if only want subset of samples from a particular zone; defined in samples_to_use file
			#print "hello"
			
			
		
			if (row[eles_index['SAMPLE NAME']].value in samples_to_use.samples_to_use[sub_zone] or row[eles_index['SAMPLE NAME']].value not in samples_not_to_use.samples_not_to_use[sub_zone]):
				
				#if row[eles_index['SAMPLE NAME']].value not in samples_not_to_use.samples_not_to_use[sub_zone]:
				
				for col_name,ind in eles_index.iteritems():#looping through header and indices
				
					eles[col_name]=row_list[ind]
				ID=eles['SAMPLE NAME']
				#print eles
			
				s=Sample(ID,eles)#creates sample object for sample
				samples[ID]=s#puts sample object in dictionary which contains all samples
		else:
			 
			for col_name,ind in eles_index.iteritems():
				
				eles[col_name]=row_list[ind]
			ID=eles['SAMPLE NAME']


			s=Sample(ID,eles)
			samples[ID]=s

	
	return samples, eles
