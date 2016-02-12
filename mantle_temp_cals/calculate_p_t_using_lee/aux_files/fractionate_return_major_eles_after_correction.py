#Python version of vba macro in Lee et al 2009 spreadsheet
def fractionate(ele_d,H2Omelt1,fo2,Fomax,mass_inc=0.00005,Kd_var=1,MgO_min=6.0):#ele_d=dict of element concentrations,h2o=h2o content of melt, fo2=oxidation of mantle,Fo=forsterite content of mantle,Kd_var (1=variable Kd, 0 =non variable Kd)
	import math
	import try_strings
	Iteration=0
	
	#pdb.set_trace()
	SiO2melt1 = try_strings.try_strings(["SIO2(WT%)","SIO2(WT%): altern. values or methods","SIO2(WT%): altern. values and methods"],ele_d)
	TiO2melt1 = try_strings.try_strings(["TIO2(WT%)","TIO2(WT%): altern. values or methods","TIO2(WT%): altern. values and methods"],ele_d)
	Al2O3melt1 = try_strings.try_strings(["AL2O3(WT%)","AL2O3(WT%): altern. values or methods","AL2O3(WT%): altern. values and methods"],ele_d)
	Cr2O3melt1 = 0.0#try_strings.try_strings(["CR2O3(WT%)","CR2O3(WT%): altern. values or methods","CR2O3(WT%): altern. values and methods"],ele_d)
	FeOmelt1 = try_strings.try_strings(["FEOT(WT%)","FEOT(WT%): altern. values or methods","FEOT(WT%): altern. values and methods"],ele_d)
	MnOmelt1 = try_strings.try_strings(["MNO(WT%)","MNO(WT%): altern. values or methods","MNO(WT%): altern. values and methods"],ele_d)
	MgOmelt1 = try_strings.try_strings(["MGO(WT%)","MGO(WT%): altern. values or methods","MGO(WT%): altern. values and methods"],ele_d)
	CaOmelt1 = try_strings.try_strings(["CAO(WT%)","CAO(WT%): altern. values or methods","CAO(WT%): altern. values and methods"],ele_d)
	Na2Omelt1 = try_strings.try_strings(["NA2O(WT%)","NA2O(WT%): altern. values or methods","NA2O(WT%): altern. values and methods"],ele_d)
	K2Omelt1 = try_strings.try_strings(["K2O(WT%)","K2O(WT%): altern. values or methods","K2O(WT%): altern. values and methods"],ele_d)
	
	#H2Omelt1 = ele_d["H2O"]
	for maj in [SiO2melt1,TiO2melt1,Al2O3melt1,FeOmelt1,MnOmelt1,MgOmelt1,CaOmelt1,Na2Omelt1,K2Omelt1]:
		
		if type(maj) is not float:#if one of major elements values is not a float
			#print "heree",ele_d["AL2O3(WT%)"],"blah"
			major_eles_corrected={"MGO":'nan',"FEO":'nan',"FE2O3":'nan',"SIO2":'nan',"TIO2":'nan',"AL2O3":'nan',"CAO":'nan',"MNO":'nan',"NA2O":'nan',"K2O":'nan',"H2O":'nan'}	
	
			return major_eles_corrected
	
	SumMelt1 = SiO2melt1 + TiO2melt1 + Al2O3melt1 + Cr2O3melt1 + FeOmelt1 + MnOmelt1 + MgOmelt1 + CaOmelt1 + Na2Omelt1 + K2Omelt1 + H2Omelt1

	FeOmelt1x = FeOmelt1 * (1 - fo2)#??
	Fe2O3melt1x = FeOmelt1 * (fo2) * 159.69 /( 71.84 * 2)#??

	Sum = SiO2melt1 + TiO2melt1 + Al2O3melt1 + Cr2O3melt1 + FeOmelt1x + Fe2O3melt1x + MnOmelt1 + MgOmelt1 + CaOmelt1 + Na2Omelt1 + K2Omelt1 + H2Omelt1
	
	if MgOmelt1<MgO_min:
		print MgOmelt1,"no this is"
		K=0
	else:
		K=1
	
	#Normalize to 100%
	SiO2melt = SiO2melt1 / Sum * 100
        TiO2melt = TiO2melt1 / Sum * 100
        Al2O3melt = Al2O3melt1 / Sum * 100
        Cr2O3melt1 = Cr2O3melt1 / Sum * 100
        FeOmelt = FeOmelt1x / Sum * 100
        Fe2O3melt = Fe2O3melt1x / Sum * 100
        MnOmelt = MnOmelt1 / Sum * 100
        MgOmelt = MgOmelt1 / Sum * 100
        CaOmelt = CaOmelt1 / Sum * 100
        Na2Omelt = Na2Omelt1 / Sum * 100
        K2Omelt = K2Omelt1 / Sum * 100
        H2Omelt = H2Omelt1 / Sum * 100

	#ANHYDROUS cation percents for original sample (note: we include H2O)
        cat0 = (SiO2melt1 / 60.08) + (TiO2melt1 / 79.86) + ((2 * Al2O3melt1) / 101.96) + ((2 * Cr2O3melt1) / 151.99) + (FeOmelt1 / 71.84) + (MnOmelt1 / 70.94) + (MgOmelt1 / 40.3) + (CaOmelt1 / 56.08) + ((2 * Na2Omelt1) / 61.98) + ((2 * K2Omelt1) / 94.2)+((2 * Fe2O3melt1x) / 159.59) #2* ? Total number of moles?
	Si0 = SiO2melt1 / (60.08 * cat0) * 100
	Ti0 = TiO2melt1 / (79.86 * cat0) * 100
	Al0 = 2 * Al2O3melt1 / (101.96 * cat0) * 100
	Cr0 = 2 * Cr2O3melt1 / (151.99 * cat0) * 100
	Fe20 = FeOmelt1x / (71.84 * cat0) * 100
	Mn0 = MnOmelt1 / (70.94 * cat0) * 100
	Mg0 = MgOmelt1 / (40.3 * cat0) * 100
	Ca0 = CaOmelt1 / (56.08 * cat0) * 100
	Na0 = 2 * Na2Omelt1 / (61.98 * cat0) * 100
	K0 = 2 * K2Omelt1 / (94.2 * cat0) * 100
	
	Fe30 = ((2 * Fe2O3melt1x) / (159.69 * cat0)) * 100
	Fe30 = 2 * Fe2O3melt1x / 159.69 / cat0 * 100
	if Kd_var == 0:
		KD = 0.32
	elif Kd_var==1:
		KD = 0.25324 + 0.0033663 * (Mg0 + 0.33 * Fe20) #Tamura(19xx)
	
	FoZ = 1 / (1 + KD * Fe20 / Mg0)

	
	
	if FoZ>Fomax:
		dm=-1*mass_inc
	else:
		dm=mass_inc
	
	Fo=FoZ
	if SumMelt1<97:
		print "Sum of major elements < 97%; returning 0,0"
		K1=0
		
	else:
		K1=1
	
	if K1==0 or K==0:
		#print K1,K,"blah"
		major_eles_corrected={"MGO":'nan',"FEO":'nan',"FE2O3":'nan',"SIO2":'nan',"TIO2":'nan',"AL2O3":'nan',"CAO":'nan',"MNO":'nan',"NA2O":'nan',"K2O":'nan',"H2O":'nan'}	
	
		return major_eles_corrected
	try:
		while True:
			MWol = 2 * Fo * 40.3 + 2.0 * (1.0 - Fo) * 71.85 + 60.08#calculating composition of olivine to add in
			FeOol = ((2 * (1 - Fo) * 71.85) / MWol) * 100
			MgOol = (2 * Fo * 40.3 / MWol) * 100
			SiO2ol = (60.08 / MWol) * 100
			
			MgOmelt = (MgOol * dm + MgOmelt) / (1 + dm)
			FeOmelt = (FeOol * dm + FeOmelt) / (1 + dm)
			Fe2O3melt = Fe2O3melt / (1 + dm)
			SiO2melt = (SiO2ol * dm + SiO2melt) / (1 + dm)
			TiO2melt = TiO2melt / (1 + dm)
			Al2O3melt = Al2O3melt / (1 + dm)
			MnOmelt = MnOmelt / (1 + dm)
			CaOmelt = CaOmelt / (1 + dm)
			Na2Omelt = Na2Omelt / (1 + dm)
			K2Omelt = K2Omelt / (1 + dm)
			H2Omelt = H2Omelt / (1 + dm)
			#Cr2O3melt = Cr2O3melt / (1 + dm)
			if Kd_var == 0:
				KD = 0.32
			if Kd_var == 1: 
				KD = 0.25324 + 0.0033663 * (Mg0 + 0.33 * Fe20) #Tamura(19xx)
			Fo = 1 / (1 + KD * (FeOmelt / 71.85) / (MgOmelt / 40.3))
			Sum = (SiO2melt + TiO2melt + Al2O3melt + FeOmelt + Fe2O3melt + MnOmelt + MgOmelt + CaOmelt + Na2Omelt + K2Omelt + H2Omelt)#removed Cr2O3
			Iteration+=1
			totaloliv = (1 + dm) ** (Iteration)
			#print abs(Fo-Fomax)
			#print Iteration
#			if Iteration%100==0:
#				print Fo
#				c=raw_input("helo")
			if abs(Fo-Fomax)<0.0005:
				
				break
#			if Iteration>10000:
#				return [0.0,0.0],0.0
			
			
			
	except:
		major_eles_corrected={"MGO":'nan',"FEO":'nan',"FE2O3":'nan',"SIO2":'nan',"TIO2":'nan',"AL2O3":'nan',"CAO":'nan',"MNO":'nan',"NA2O":'nan',"K2O":'nan',"H2O":'nan'}	
	
		return major_eles_corrected
	#pdb.set_trace()
	
	 #oxide mole percent
	Ox = SiO2melt / 60.08 + TiO2melt / 79.86 + Al2O3melt / 101.96 + FeOmelt / 71.84 + MnOmelt / 70.94 + MgOmelt / 40.3 + CaOmelt / 56.08 + Na2Omelt / 61.98 + K2Omelt / 94.2 + H2Omelt / 18.02 + Fe2O3melt / 159.59 #Cr2O3melt / 151.99  removed
	moleSiO2 = SiO2melt / 60.08 / Ox * 100
	moleTiO2 = TiO2melt / 79.86 / Ox * 100
	moleAl2O3 = Al2O3melt / 101.96 / Ox * 100
	#moleCr2O3 = Cr2O3melt / 151.99 / Ox * 100
	moleFeO = FeOmelt / 71.84 / Ox * 100
	moleMnO = MnOmelt / 70.94 / Ox * 100
	moleMgO = MgOmelt / 40.3 / Ox * 100
	moleCaO = CaOmelt / 56.08 / Ox * 100
	moleNa2O = Na2Omelt / 61.98 / Ox * 100
	moleK2O = K2Omelt / 94.2 / Ox * 100
	moleH2O = H2Omelt / 18.02 / Ox * 100
	moleFe2O3 = Fe2O3melt / (159.69 * Ox) * 100
	SumOxmole = moleSiO2 + moleTiO2 + moleAl2O3 + moleFeO + moleMnO + moleMgO + moleCaO + moleNa2O + moleK2O + moleH2O + moleFe2O3 #+ moleCr2O3 removed
	
	
	
	#ANHYDROUS cation mole percent
	cat = moleSiO2 + moleTiO2 + moleAl2O3 * 2 + moleFeO + moleMnO + moleMgO + moleCaO + moleNa2O * 2 + moleK2O * 2 + moleFe2O3 * 2# + moleCr2O3
	Si = moleSiO2 / cat * 100
	Ti = moleTiO2 / cat * 100
	Al = moleAl2O3 * 2 / cat * 100
	#Cr = moleCr2O3 * 2 / cat * 100
	Fe2 = moleFeO / cat * 100
	Mn = moleMnO / cat * 100
	Mg = moleMgO / cat * 100
	Ca = moleCaO / cat * 100
	Na = moleNa2O * 2 / cat * 100
	Ks = moleK2O * 2 / cat * 100
	#?? No one for H2O
	
	Fe3 = moleFe2O3 * 2 / cat * 100
	catsum = Si + Ti + Al + Fe2 + Mn + Mg + Ca + Na + Ks + Fe3#remover+Cr and +H
	
	#Mole Species - Cin-Ty's formulation
	Si4O8 = 0.25 * (moleSiO2 - 0.5 * (moleFeO + moleMgO + moleCaO + moleMnO) - moleNa2O - moleK2O)
	Ti4O8 = 0.25 * moleTiO2
	Al163O8 = 3 / 8. * (moleAl2O3 - moleNa2O)
	#Cr163O8 = 3 / 8 * moleCr2O3
	Fe163O8 = 3 / 8. * moleFe2O3
	Fe4Si2O8 = 0.25 * moleFeO
	Mn4Si2O8 = 1 / 4. * moleMnO
	Mg4Si2O8 = 1 / 4. * moleMgO
	Ca4Si2O8 = 1 / 4. * moleCaO
	Na2Al2Si2O8 = moleNa2O
	K2Al2Si2O8 = moleK2O
	H16O8 = 0.125 * moleH2O
	sum8 = Si4O8 + Ti4O8 + Al163O8  + Fe163O8 + Fe4Si2O8 + Mg4Si2O8 + Mn4Si2O8 + Ca4Si2O8 + Na2Al2Si2O8 + K2Al2Si2O8 + H16O8  #+ Cr163O8

	Sim = Si4O8 / sum8 * 100
	Tim = Ti4O8 / sum8 * 100
	Alm = Al163O8 / sum8 * 100
	#Crm = Cr163O8 / sum8 * 100
	FeIIIm = Fe163O8 / sum8 * 100
	FeIIm = Fe4Si2O8 / sum8 * 100
	Mnm = Mn4Si2O8 / sum8 * 100
	Mgm = Mg4Si2O8 / sum8 * 100
	Cam = Ca4Si2O8 / sum8 * 100
	Nam = Na2Al2Si2O8 / sum8 * 100
	Km = K2Al2Si2O8 / sum8 * 100
	Hm = H16O8 / sum8 * 100
	sum8b = Sim + Tim + Alm + FeIIIm + FeIIm + Mnm + Mgm + Cam + Nam + Km + Hm # + Crm
	#CALCULATION OF PRESSURES AND TEMPERATURES
            
            #PLee parameters
	b0 = 4.019    #basic constant
        b1 = -770   #temperature 1/T
        b2 = 0.0058 #temperature T^0.5
        b3 = 0.0165    #Fe
        b4 = 0.0005     #Ca
        b5 = 0.003      #water
               
                #Putirka 2005 with Na, K, H2O
                   #T is in Celsius, P is GPa
        #Tp = 3063.2 / (math.log(Fo * 100 * 2. / 3. / Mg) + 2.106193 - 0.019 * SiO2melt - 0.08 * (Na2Omelt + K2Omelt) + 0.028 * H2Omelt)
        #Pa = 0.1 * (math.exp(0.00252 * Tp - 0.12 * SiO2melt + 5.027))
        #PLee = (math.log(Sim) - b0 + b3 * FeIIm + b4 * Cam**2) / (b1 / (Tp + 273.15) + b2 * (Tp + 273.15)**0.5 - b5 * Hm)
                    
                
#                'Putirka 2005 without compositional effects
#                    'T is in Celsius, P is GPa
#                    If K = 0 Then Tpx = 0 Else Tpx = 4490.5 / (Log(Fo * 100 * 2 / 3 / Mg) + 2.02)
#                    If Tpx = 0 Then Pax = 0 Else Pax = 0.1 * Exp(0.00252 * Tpx - 0.12 * SiO2melt + 5.027)
#                    If Pax = 0 Then PLeex = 0 Else PLeex = (Log(Sim) - b0 + b3 * FeIIm + b4 * Cam ^ 2) / (b1 / (Tpx + 273.15) + b2 * (Tpx + 273.15) ^ 0.5 - b5 * Hm)
#                    
#                        ActiveCell.Offset(x, 79) = Tpx
#                        ActiveCell.Offset(x, 80) = PLeex
#                        ActiveCell.Offset(x, 81) = Pax
#            
#                'Lee T-independent barometer
#                    c0 = 4.05
#                    c3 = 0.012
#                    
#                    If K = 0 Then PLeez = 0 Else PLeez = (Log(Sim) - c0 + c3 * FeIIm) / (c1 / (Mgm ^ (1 / 3)) + c2 * Mgm ^ (1 / 2))
#                    
#                        ActiveCell.Offset(x, 89) = PLeez
#                
	#LEE BAROMETER AND THERMOMETER
	     
	TLee = 916.45 + 13.68 * Mgm + 4580 / Sim - 0.509 * Hm * Mgm
	   
	PLeeTLee = (math.log(Sim) - b0 + b3 * FeIIm + b4 * Cam**2) / (b1 / (TLee + 273.15) + b2 * (TLee + 273.15)**0.5 - b5 * Hm)
	
	major_eles_corrected={"MGO":MgOmelt,"FEO":FeOmelt,"FE2O3":Fe2O3melt,"SIO2":SiO2melt,"TIO2":TiO2melt,"AL2O3":Al2O3melt,"CAO":CaOmelt,"MNO":MnOmelt,"NA2O":Na2Omelt,"K2O":K2Omelt,"H2O":H2Omelt}	
	
	return major_eles_corrected
	#                     ActiveCell.Offset(x, 91) = PLeeTLee
#       
         
#                'Sugawara, Lee, Albarede
#                On Error GoTo 50
#        
#                     If K = 0 Then ActiveCell.Offset(x, 83) = 0 Else ActiveCell.Offset(x, 95).GoalSeek Goal:=0, ChangingCell:=ActiveCell.Offset(x, 83)
#                        Tsug1 = ActiveCell.Offset(x, 83)
#                        If Tsug1 < 0 Then GoTo 50
#                        If Tsug1 > 2000 Then GoTo 50
#                     If K = 0 Then PLeeSug = 0 Else PLeeSug = (Log(Sim) - b0 + b3 * FeIIm + b4 * Cam ^ 2) / (b1 / (Tsug1 + 273.15) + b2 * (Tsug1 + 273.15) ^ 0.5 - b5 * Hm)
#                     If K = 0 Then ActiveCell.Offset(x, 84) = 0 Else ActiveCell.Offset(x, 84) = PLeeSug
#
#                     If K = 0 Then ActiveCell.Offset(x, 86) = 0 Else ActiveCell.Offset(x, 96).GoalSeek Goal:=0, ChangingCell:=ActiveCell.Offset(x, 86)
#                        Tsug2 = ActiveCell.Offset(x, 86)
#                        If Tsug2 < 0 Then GoTo 60
#                        If Tsug2 > 2000 Then GoTo 60
#                     If K = 0 Then PAlbSug = 0 Else PAlbSug = 0.1 * Exp(0.00252 * Tsug2 - 0.12 * SiO2melt + 5.027)
#                     If K = 0 Then ActiveCell.Offset(x, 87) = 0 Else ActiveCell.Offset(x, 87) = PAlbSug
#               
#50
#
#               
#                  
#60
#                   
#                    
#                    Iteration = Iteration + 1
#                    Range("K14") = Iteration
#                    
#                    
#                    Counter = Counter + 1
#                    Range("L14") = Counter
#                
#                    Range("M14") = KD
