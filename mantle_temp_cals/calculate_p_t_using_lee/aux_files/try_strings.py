def try_strings(strings, dictionary):#takes in list of strings and a dictionary and looks for dictionary key that is same as one of strings - necessary for georoc files as element concentrations sometimes have different headers
	
	for string in strings:
		try:
			value=dictionary[string]
			#print type(float(value))

			if type(float(value)) is not float:
				return float('nan')
			else:
				
				return float(value)
		except:
			continue
	#print "%s value not found!"%strings[0],dictionary
	
	#sys.exit()
	
