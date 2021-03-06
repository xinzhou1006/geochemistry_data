#equation 19 for melt fraction with hydrous melting Katz 2003
	
def mf_root_finding(F,P,T,h2o,A1=1085.7):#format for root finding for F
	
	 
	#A1=1085.7
	#A1=1159.6#from kelley 2010 for a more refractory composition	
	A2=132.9
	A3=-5.1
	B1=1475.0
	B2=80.0
	B3=-3.2
	K=43.0#from table 2 Katz 2003
	gam=0.75
	D_h2o=0.01
	beta1=1.5
	
	
	
	melt_h2o=h2o
	#melt_h2o=h2o/(D_h2o+F*(1-D_h2o))
	dt=K*melt_h2o**gam
	T_lherz_liq=B1+B2*P+B3*P**2
	T_sol=A1+A2*P+A3*P**2
	
	if (T-(T_sol-dt))<0.0 or (T_lherz_liq-T_sol)<0:
		
		return 0.0
	else:
		
		return F-((T-(T_sol-dt))/(T_lherz_liq-T_sol))**beta1
def mf_root_finding_numpy(F,P,T,h2o,A1=1085.7):#format for root finding for F assuming numpy array input 
	
	 
	#A1=1085.7
	#A1=1159.6#from kelley 2010 for a more refractory composition	
	A2=132.9
	A3=-5.1
	B1=1475.0
	B2=80.0
	B3=-3.2
	K=43.0#from table 2 Katz 2003
	gam=0.75
	D_h2o=0.01
	beta1=1.5
	
	
	
	melt_h2o=h2o
	#melt_h2o=h2o/(D_h2o+F*(1-D_h2o))
	dt=K*melt_h2o**gam
	T_lherz_liq=B1+B2*P+B3*P**2
	T_sol=A1+A2*P+A3*P**2
	
	if (T.any()-(T_sol-dt))<0.0 or (T_lherz_liq-T_sol)<0:
		
		return 0.0
	else:
		
		return F-((T-(T_sol-dt))/(T_lherz_liq-T_sol))**beta1
def mf_F_contour(T,P,F,h2o):#find P,T condition for a constant F
	A1=1085.7
	A2=132.9
	A3=-5.1
	B1=1475.0
	B2=80.0
	B3=-3.2
	K=43#from table 2 Katz 2003
	gam=0.75
	D_h2o=0.01
	beta1=1.5
	#melt_h2o=h2o/(D_h2o+F*(1-D_h2o))
	#print melt_h2o
	melt_h2o=h2o
	dt=K*melt_h2o**gam
	T_lherz_liq=B1+B2*P+B3*P**2
	T_sol=A1+A2*P+A3*P**2
	return (F**(1/beta1)*(T_lherz_liq-T_sol)+(T_sol-dt))-T
def mf(T,P,h2o):	#actual format in Katz 2003
	A1=1085.7
	A2=132.9
	A3=-5.1
	B1=1475.0
	B2=80.0
	B3=-3.2
	K=43#from table 2 Katz 2003
	gam=0.75
	D_h2o=0.01
	beta1=1.5
	melt_h2o=h2o/(D_h2o+F*(1-D_h2o))
	dt=K*melt_h2o**gam
	T_lherz_liq=B1+B2*P+B3*P**2
	T_sol=A1+A2*P+A3*P**2
	#c=raw_input("hello")
	return ((T-(T_sol-dt))/(T_lherz_liq-T_sol))**beta1
def mf_opx(P,T,fcpx_out,h2o,A1):#melt fraction for cpx out
	
	#A1=1159.6#from kelley 2010 for a more refractory composition
	A2=132.9
	A3=-5.1
	B1=1475.0
	B2=80.0
	B3=-3.2
	beta2=1.5
	C1=1780.0
	C2=45.0
	C3=-2.0
	K=43
	gam=0.75
	D_h2o=0.01
	melt_h2o=h2o
	#melt_h2o=h2o/(D_h2o+F*(1-D_h2o))
	dt=K*melt_h2o**gam
	Tliquidus=C1+C2*P+C3*P**2-dt
	T_lherz_liq=B1+B2*P+B3*P**2-dt
	T_sol=A1+A2*P+A3*P**2-dt
	
	
	Tcpx_out=fcpx_out**(1/beta2)*(T_lherz_liq-T_sol)+T_sol
	#print (T-Tcpx_out),Tliquidus-Tcpx_out,T_lherz_liq-T_sol
#	print Tliquidus-Tcpx_out
#	print 1-fcpx_out
#	print "y"
	if T-Tcpx_out>0:
		return fcpx_out+(1-fcpx_out)*((T-Tcpx_out)/(Tliquidus-Tcpx_out))**beta2
	else:	
		print "error in opx calc"
def mf_opx_t_solve(P,F,fcpx_out,h2o):#rearranged to solve for temperature
	A1=1085.7
	A2=132.9
	A3=-5.1
	B1=1475.0
	B2=80.0
	B3=-3.2
	beta2=1.5
	C1=1780.0
	C2=45.0
	C3=-2.0
	K=43.0
	gam=0.75
	melt_h2o=h2o
	dt=K*melt_h2o**gam
	Tliquidus=C1+C2*P+C3*P**2-dt
	T_lherz_liq=B1+B2*P+B3*P**2-dt
	T_sol=A1+A2*P+A3*P**2-dt
	Tcpx_out=fcpx_out**(1/beta2)*(T_lherz_liq-T_sol)+T_sol
	return Tcpx_out+(Tliquidus-Tcpx_out)*((F-fcpx_out)/(1-fcpx_out))**(1/beta2)
def mf_opx_unknown_melt_h2o(F,P,T,fcpx_out,h2o):#melt fraction for cpx out when bulk h2o is known
	A1=1085.7
	#A1=1159.6#from kelley 2010 for a more refractory composition
	A2=132.9
	A3=-5.1
	B1=1475.0
	B2=80.0
	B3=-3.2
	beta2=1.5
	C1=1780.0
	C2=45.0
	C3=-2.0
	K=43
	gam=0.75
	D_h2o=0.01
	melt_h2o=h2o
	melt_h2o=h2o/(D_h2o+F*(1-D_h2o))
	dt=K*melt_h2o**gam
	Tliquidus=C1+C2*P+C3*P**2-dt
	T_lherz_liq=B1+B2*P+B3*P**2-dt
	T_sol=A1+A2*P+A3*P**2-dt
	Tcpx_out=fcpx_out**(1/beta2)*(T_lherz_liq-T_sol)+T_sol
	return F-(fcpx_out+(1-fcpx_out)*((T-Tcpx_out)/(Tliquidus-Tcpx_out))**beta2)	
def mf_opx_unknown_melt_h2o_change_A1(F,P,T,fcpx_out,h2o,A1):#melt fraction for cpx out when bulk h2o is known
	#A1=1085.7
	#A1=1159.6#from kelley 2010 for a more refractory composition
	A2=132.9
	A3=-5.1
	B1=1475.0
	B2=80.0
	B3=-3.2
	beta2=1.5
	C1=1780.0
	C2=45.0
	C3=-2.0
	K=43
	gam=0.75
	D_h2o=0.01
	melt_h2o=h2o
	melt_h2o=h2o/(D_h2o+F*(1-D_h2o))
	dt=K*melt_h2o**gam
	Tliquidus=C1+C2*P+C3*P**2-dt
	T_lherz_liq=B1+B2*P+B3*P**2-dt
	T_sol=A1+A2*P+A3*P**2-dt
	Tcpx_out=fcpx_out**(1/beta2)*(T_lherz_liq-T_sol)+T_sol
	return F-(fcpx_out+(1-fcpx_out)*((T-Tcpx_out)/(Tliquidus-Tcpx_out))**beta2)
def T_lherz_liq(P,h2o):
	B1=1475.0
	B2=80.0
	B3=-3.2
	gam=0.75
	K=43.0
	melt_h2o=h2o
	dt=K*melt_h2o**gam
	return B1+B2*P+B3*P**2-dt

def T_sol(P,h2o,A1=1085.7):
	
	A2=132.9
	A3=-5.1
	K=43.0
	gam=0.75
	melt_h2o=h2o
	dt=K*melt_h2o**gam
	return A1+A2*P+A3*P**2 -dt
def T_sol_solid_h2o(P,h2o,A1=1085.7):#calculate solidus given h2o in solid
	
	A2=132.9
	A3=-5.1
	K=43.0
	gam=0.75
	D_h2o=0.01
	melt_h2o=h2o/(D_h2o+F*(1-D_h2o))
	dt=K*melt_h2o**gam
	return A1+A2*P+A3*P**2 -dt
