def calculate_adiabat(P,T,comp,mineral_props,h2o):
	import katz_adiabatic_eqns as ka
	import katz_mf
	dP=0.005
	est_ave_x=T
	est_ave_y=P
	adi_T=[]
	adi_P=[]
	adi_T.append(est_ave_x)
	adi_P.append(est_ave_y)
	while True:
		f=katz_mf.katz_mf(comp,mineral_props,[est_ave_x,est_ave_y],h2o)


		if f==0.0:
			break

		est_ave_x=est_ave_x+ka.dt_dp(f,est_ave_y,est_ave_x,h2o)*dP
	
		est_ave_y=est_ave_y+dP
		adi_T.append(est_ave_x)
		adi_P.append(est_ave_y)

	return est_ave_y,est_ave_x
