def write_to_latex_as_subfigures(filename,directories):	#function for writing latex code for including image in document to file. All images as subfigures in  one figure            
	import os,sys
	
	if not os.path.exists("latex_files/"):
		os.makedirs("latex_files/")
	outfile=open("latex_files/%s"%filename,'w')
	outfile.write("%segin{figure}\n"%(r"\b"))
	for name in directories:
		outfile.write("""%segin{subfigure}[h]{0.6%sextwidth}
\includegraphics[width=0.8%sextwidth]{%s}\n\end{subfigure}\n"""%(r"\b",r"\t",r"\t",name))
	outfile.write("\caption{}\n\end{figure}\n")
	outfile.close()

