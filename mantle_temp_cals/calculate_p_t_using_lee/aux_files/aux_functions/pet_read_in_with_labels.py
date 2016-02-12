def pet_read_in(pet_file):#takes in file containing samples with estimates of P,T using various assumptions of H2O, fo2
	class Sample:	#class for a rock sample; stores the different P,T estimates, F, TiO2
		def __init__(self,tio2,Y,La,name,pts):#,fo90_0,fo90_8,fo92_0,fo92_8,name):#,fo92_0,fo92_8,tio2):
			self.name=name
			self.tio2=tio2
			self.Y=Y
			self.La=La
			self.pts=pts
			self.La_D={"ol":0.0,"opx":0.0008,"cpx":0.071}#distribution coeffs 
			self.Y_D={"ol":1e-3,"opx":0.086,"cpx":0.76}
			self.ti_D={"ol":0.01,"opx":0.24,"cpx":0.34}
			
		def mf(self,props,mantle_concs):#method to calculate melt fractions from Ti,Y,La concs
			self.ti=(((47.87/79.87)*self.tio2)/100.)*1000000.#converting to ppm
			
			self.ti_F={}	#store melt fractions 		
			self.La_F={}
			self.Y_F={}
			self.ti_F_error={}
			for props_name in props:#looping through depleted-fertile compositions and corresponding mineralogical comps
				
				
				
				
				self.bulk_ti_D=props[props_name]["ol"]*self.ti_D["ol"]+props[props_name]["opx"]*self.ti_D["opx"]+props[props_name]["cpx"]*self.ti_D["cpx"]
				
				self.bulk_La_D=props[props_name]["ol"]*self.La_D["ol"]+props[props_name]["opx"]*self.La_D["opx"]+props[props_name]["cpx"]*self.La_D["cpx"]
				self.bulk_Y_D=props[props_name]["ol"]*self.Y_D["ol"]+props[props_name]["opx"]*self.Y_D["opx"]+props[props_name]["cpx"]*self.Y_D["cpx"]
				if self.ti!=0:	#checking to see if sample has an associated measurement; if not then F=0
					self.ti_F[props_name]=((mantle_concs[props_name]["Ti"]/self.ti)-self.bulk_ti_D)/(1-self.bulk_ti_D)

					self.ti_F_error[props_name]=((mantle_concs[props_name]["Ti"]/self.ti)-0.04)/(1-0.04)
				else:
					self.ti_F[props_name]=0.0
				if self.La!=0:#checking to see if sample has an associated measurement; if not then F=0
					self.La_F[props_name]=((mantle_concs[props_name]["La"]/self.La)-self.bulk_La_D)/(1-self.bulk_La_D)
				else:
					self.La_F[props_name]=0.0
				if self.Y!=0:
					self.Y_F[props_name]=((mantle_concs[props_name]["Y"]/self.Y)-self.bulk_Y_D)/(1-self.bulk_Y_D)
				else:
					self.Y_F[props_name]=0.0

			#return self.ti_F,self.La_F,self.Y_F
		def katz_mf(self,props):	#calculates melt fraction as in Katz 2003. props_name=mineralogy of mantle 
			from scipy.optimize import fsolve
			import katz_melt_frac
			self.fracs={}
			for props_name in props:
				
				for self.con,self.est in self.pts.iteritems():#looping through conditions(fo,h2o,fo2) - self.con and corresponding P,T,Estimate - self.est
					if self.est!=0.0:# if not an empty P,T,H2O estimate in file
						if props_name=="Fo=92":
							A_val=1159.6#value from kelley 2010
						else:
							A_val=1085.7
			
						self.x0=fsolve(katz_melt_frac.mf_root_finding,0,(self.est[0],self.est[1],self.est[2],A_val))[0]
		
		
						if self.x0>self.fcpx_out(self.est[0],props[props_name]):
			
							self.x0=katz_melt_frac.mf_opx(self.est[0],self.est[1],self.fcpx_out(self.est[0],props[props_name]),self.est[2],A_val)
						self.fracs[self.con]=self.x0
				
#						elif props_name=="p3" and self.con[:5]=="Fo=90" and self.est[2]!=4 and self.est[2]!=2:
#						
#					
#			
#							self.x0=fsolve(katz_melt_frac.mf_root_finding,0,(self.est[0],self.est[1],self.est[2]))[0]
#			
#			
#							if self.x0>self.fcpx_out(self.est[0],props_name):
#				
#								self.x0=katz_melt_frac.mf_opx(self.est[0],self.est[1],self.fcpx_out(self.est[0],props_name),self.est[2])
#							self.fracs[self.con]=self.x0
			
			#return self.fracs
		def fcpx_out(self,P,comp):
			
			#print comp
			Mcpx=comp["cpx"]
				
			#r0=0.446
			
			self.r0=0.45	
			self.r1=0.08
			return Mcpx/(self.r0+self.r1*P)
			
	import matplotlib.pyplot as plt
	infile=open(pet_file,'r')
	lines=infile.readlines()
	
	samples={}
	header=lines[0].split("\t")[4:]
	header=[i.strip() for i in header]
			
	#print header,"hello"
	
	for line in lines[1:]:
		d = dict.fromkeys(header, 0)#creates dictionary with the header P,T,H2O conditions as keys  
		print d
		c=raw_input("h")
		nums=line.split("\t")
		
		#if '' not in nums and '\n' not in nums:
			
		ID=nums[0].strip()
		#print nums[1]
		tio2=float((nums[1].strip()))
		Y=float((nums[2].strip()))
		La=float((nums[3].strip()))
		#print nums
		
		#c=raw_input("hello")
		for k in d.keys():
			ke=header.index(k)
			
			try:#if repr(nums[2:][ke])!='' or repr(nums[2:][ke])!='\n':
				d[k]=eval(nums[4:][ke])
			except SyntaxError:
				d[k]=0.0

		s=Sample(tio2,Y,La,ID,d)
		samples[ID]=s
	return samples
