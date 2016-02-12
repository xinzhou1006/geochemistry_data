#Reproducing figure
import numpy as np
def melting_model():
	cpx_D={"Tb":0.44,"Yb":0.43,"La":0.054}#From Halliday 1995 used Gd for Tb
	ol_D={"Tb":0.0011,"Yb":0.024,"La":0.0002}
	opx_D={"Tb":0.0065,"Yb":0.038,"La":0.0031}
	gar_D={"Tb":1.2,"Yb":6.4,"La":0.0007}


	cpx_D={"Tb":1.1,"Yb":1.43,"La":0.089}#From Blundy 1998 used Gd for Tb
	ol_D={"Tb":0.0011,"Yb":0.024,"La":0.0002}
	opx_D={"Tb":0.0065,"Yb":0.038,"La":0.0031}
	gar_D={"Tb":1.2,"Yb":6.4,"La":0.0007}

	#mantle_conc={"Tb":0.108,"Yb":0.493,"La":0.687} #PUM
	mantle_conc={"Tb":0.07,"Yb":0.365,"La":0.192} #DMM
	props={"ol":0.55,"opx":0.25}


	def cl_frac(f,D,c0):
		brac=1-(1-f)**(1/D)
		cl = (1/f)*brac*c0
		return cl

	tb_yb=[]
	la_yb=[]

	for f in np.arange(0,0.4,0.02):
		tb_yb.append([])
		la_yb.append([])
		for gar_frac in np.arange(0,0.2,0.02):
			D_tb=props["ol"]*ol_D["Tb"]+props["opx"]*opx_D["Tb"]+(0.2-gar_frac)*cpx_D["Tb"]+gar_frac*gar_D["Tb"]
			D_yb=props["ol"]*ol_D["Yb"]+props["opx"]*opx_D["Yb"]+(0.2-gar_frac)*cpx_D["Yb"]+gar_frac*gar_D["Yb"]
			D_la=props["ol"]*ol_D["La"]+props["opx"]*opx_D["La"]+(0.2-gar_frac)*cpx_D["La"]+gar_frac*gar_D["La"]

		
			tb=cl_frac(f,D_tb,mantle_conc["Tb"])
			yb=cl_frac(f,D_yb,mantle_conc["Yb"])
			la=cl_frac(f,D_la,mantle_conc["La"])
	

			tb_yb[-1].append(tb/yb)
			la_yb[-1].append(la/yb)
	const_f_tb_yb=[]
	const_f_la_yb=[]
	for gar_frac in np.arange(0,0.2,0.02):
		const_f_tb_yb.append([])
		const_f_la_yb.append([])
		for f in np.arange(0,0.4,0.02):
			D_tb=props["ol"]*ol_D["Tb"]+props["opx"]*opx_D["Tb"]+(0.2-gar_frac)*cpx_D["Tb"]+gar_frac*gar_D["Tb"]
			D_yb=props["ol"]*ol_D["Yb"]+props["opx"]*opx_D["Yb"]+(0.2-gar_frac)*cpx_D["Yb"]+gar_frac*gar_D["Yb"]
			D_la=props["ol"]*ol_D["La"]+props["opx"]*opx_D["La"]+(0.2-gar_frac)*cpx_D["La"]+gar_frac*gar_D["La"]

	
			tb=cl_frac(f,D_tb,mantle_conc["Tb"])
			yb=cl_frac(f,D_yb,mantle_conc["Yb"])
			la=cl_frac(f,D_la,mantle_conc["La"])


			const_f_tb_yb[-1].append(tb/yb)
			const_f_la_yb[-1].append(la/yb)
	
	return la_yb,tb_yb,const_f_la_yb,const_f_tb_yb
	
		
		
