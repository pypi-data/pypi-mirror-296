import sys
import os
import json
import pathlib
from biodata.baseio import get_text_file_extension
from biodata.delimited import DelimitedReader

from rmsp import rmsutils, rmsbuilder
from rmsp.rmstemplate import RMSTemplateLibrary
from rmsp.rmscore import ResourceManagementSystem
from commonhelper import convert_to_bool

import simplevc
simplevc.register(sys.modules[__name__])

@vt()
@vc
def _setup_wizard_20240430(dbpath : str, dbname : str):
	dbpath = dbpath + "/"
	p = pathlib.Path(dbpath + "RMSResources/")
	p.mkdir(parents=True, exist_ok=True)
	p = pathlib.Path(dbpath + "RMSLibrary/")
	p.mkdir(parents=True, exist_ok=True)
	rmsutils.create_new_db(dbpath + dbname)
	
@vt()
@vc
def _register_files_20240430(dbpath: str, dbname: str, files : list[str]):
	dbpath = dbpath + "/"
	dbfile = dbpath + dbname
	rms = ResourceManagementSystem(dbfile)
	for f in files:
		rms.register_file(os.path.abspath(f))
	
# @vt()
# @vc
# def _execute_template_section_20240430(
# 		dbfile : str, resource_dump_dir : str, 
# 		libpath : str, bookname : str, chaptername : str, bookmark: str, 
# 		parameter_file: str,
# 		builder_mode:convert_to_bool=True, nthread:int=4
# 		):
# # 	bookmark = list(map(int, bookmark.split(",")))
# 	bookmark = list(bookmark.split(","))
# 	if dbfile is None:
# 		rms= rmsutils.create_virtual_rms()
# 	else:
# 		rms = ResourceManagementSystem(dbfile, resource_dump_dir)
# 		
# 	if builder_mode:
# 		rmspool = rmsbuilder.RMSProcessWrapPool(rms, nthread)
# 		rmsb = rmsbuilder.RMSUnrunTasksBuilder(rmspool)
# 		rmstlib = RMSTemplateLibrary(rmsb, libpath)
# 	else:
# 		rmstlib = RMSTemplateLibrary(rms, libpath)
# 	
# 	extension = get_text_file_extension(parameter_file)
# 	if extension == "json":
# 		with open(parameter_file, "rt") as f:
# 			parameters_entries = json.load(f)
# 	else:
# 		raise Exception("Unimplemented")
# 		parameters_entries = DelimitedReader.read_all(list, parameter_file, header=True)
# 		print(dict(parameters_entries[0]))
# 	for parameters_entry in parameters_entries:
# 		rmstlib.run(bookname, chaptername, bookmark, parameters_entry["args"], parameters_entry["kwargs"])
# 	
# 	if builder_mode:
# 		rmsb.execute_builder()
# 		rmspool.close()
# 	

@vt()
@vc
def _execute_template_commands_20240430(
		dbpath: str, dbname: str, parameter_files: list[str],
		builder_mode:convert_to_bool=True, nthread:int=8
		):
# 	bookmark = list(map(int, bookmark.split(",")))
	if dbpath == "":
		rms= rmsutils.create_virtual_rms()
	else:
		dbpath = dbpath + "/"
		rms = ResourceManagementSystem(dbpath + dbname, dbpath + "RMSResources/")
	
	libpath = dbpath + "RMSLibrary/"
	
	if builder_mode:
		rmspool = rmsbuilder.RMSProcessWrapPool(rms, nthread)
		rmsb = rmsbuilder.RMSUnrunTasksBuilder(rmspool)
		rmstlib = RMSTemplateLibrary(rmsb, libpath)
	else:
		rmstlib = RMSTemplateLibrary(rms, libpath)
	
	for parameter_file in parameter_files:
		extension = get_text_file_extension(parameter_file)
		if extension == "json":
			with open(parameter_file, "rt") as f:
				parameters_entries = json.load(f)
		else:
			
			raise Exception("Unimplemented")
			parameters_entries = DelimitedReader.read_all(list, parameter_file, header=True)
			print(dict(parameters_entries[0]))
		for parameters_entry in parameters_entries["commands"]:
			rmstlib.run(parameters_entry["bookname"], parameters_entry["chaptername"], parameters_entry["bookmark"].split(","), [], parameters_entry["parameters"])
	
	if builder_mode:
		rmsb.execute_builder()
		rmspool.close()
	
		
if __name__ == "__main__":
	main()
