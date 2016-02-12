def find_lithospheric_thickness(lon,lat,model):#find lithospheric thickness from given model of lon,lat,z
	import numpy as np	
	from scipy.interpolate import RectSphereBivariateSpline
	
	lat_min=int(lat)
	lat_max=int(lat)+1
	lon_min=int(lon)
	lon_max=int(lon)+1
	lats=np.array([lat_min,lat_max])
	lons=np.array([lon_min,lon_max])
	
	xx,yy=np.meshgrid(lats, lons)
	print xx,yy
	sys.exit()
	

##RectSphereBivariateSpline  - not working, trying linear
	lats = np.arange(0,180,1) * np.pi / 180.
	lons = np.arange(0, 360, 1) * np.pi / 180.
	data = model
#	lats = np.linspace(10, 170, 9) * np.pi / 180.
#	lons = np.linspace(0, 350, 18) * np.pi / 180.
#	data = np.dot(np.atleast_2d(90. - np.linspace(-80., 80., 18)).T,
#        np.atleast_2d(180. - np.abs(np.linspace(0., 350., 9)))).T
#	print lats.size
#	print lons.size
#	print data.shape
#	lut = RectSphereBivariateSpline(lats, lons, data)
	
	
#	lat_min=int(lat)
#	lat_max=int(lat)+1
#	lon_min=int(lon)
#	lon_max=int(lon)+1
#	

