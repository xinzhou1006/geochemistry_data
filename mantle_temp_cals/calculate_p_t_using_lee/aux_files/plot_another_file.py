plot_another_file(sub_zone,outfile):
	samps=pet_read_in_with_labels.pet_read_in("/data/ap4909/30.10.2013-hot_cold_geochem/get_lat_lon_data/sz_with_lat_lon/individual_files/individual_files_with_feo/%s_new.xls"%(sub_zone))[0]
	for key,value in samps.iteritems():
			
			
		for h2o in [4.0]:
			
			error=1000000
			
			for comp in mant_vals.keys():
				
				
				
			
				ti_melt_est=sum(value.mf(comp,mineral_props,mant_vals,h2o)[0])/len(value.mf(comp,mineral_props,mant_vals,h2o)[0])	#ti estimation of melt
			
				katz_melt_est=sum(value.mf(comp,mineral_props,mant_vals,h2o)[2])/len(value.mf(comp,mineral_props,mant_vals,h2o)[2])	#katz estimation of melt
				 
				#katz_melt_est=(value.mf(comp,mineral_props,mant_vals,0.0)[2])+np.mean(value.mf(comp,mineral_props,mant_vals,8.0)[2]))/2
			
				new_error=abs(ti_melt_est-katz_melt_est)
				if new_error<error:
					error=new_error
					l=value.lee_pt(comp,h2o)
					
					best_fit_comp=comp
				
			if l[0][0]==0 and l[1][0]==0:
				est_ave_x=0
				est_ave_y=0
			elif l[0][0]==0 or l[1][0]==0:	#sometimes lee algorithm returns 0.0 for an oxygen fugacity - therefore average turns out to be half of the other fo2 P,T
				for i in l:
					if i[0] !=0:
		
						est_ave_x=i[0]
						est_ave_y=i[1]
				
					
					
					
						ax.plot(est_ave_x,est_ave_y,markersize=20,marker=markers[zone],c=comp_colours[best_fit_comp])#"%s"%comp_style
						x_vals.append(est_ave_x)
						y_vals.append(est_ave_y)
			else:	#if two values are available for two different fo2's
				est_ave_x=(l[0][0]+l[1][0])/2.
				est_ave_y=(l[0][1]+l[1][1])/2.		
				ax.plot(est_ave_x,est_ave_y,'.',marker=markers[zone],markersize=20,c=comp_colours[best_fit_comp])
				x_vals.append(est_ave_x)
				y_vals.append(est_ave_y)
	
				x=np.array([est_ave_x])
				y=np.array([est_ave_y])
				ytop=np.array([abs(l[0][1]-est_ave_y)])
				ybot=ytop
				xtop=np.array([abs(l[0][0]-est_ave_x)])
				xbot=xtop
				ax.errorbar(x,y,yerr=(ytop,ybot),xerr=(xtop,xbot),lw=1,linestyle="None",color='r')
		latitude=(value.pts["LATITUDE (MIN.)"]+value.pts["LATITUDE (MAX.)"])/2.
		longitude=(value.pts["LONGITUDE (MIN.)"]+value.pts["LONGITUDE (MAX.)"])/2.
		
		file_string="%s\t%s\t%s\n"%(latitude,longitude,est_ave_y)

		outfile.write("%s"%file_string)
