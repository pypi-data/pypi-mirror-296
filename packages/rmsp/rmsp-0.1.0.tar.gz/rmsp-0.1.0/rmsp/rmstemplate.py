import glob
import json
import os
import importlib
import inspect

def _load_func(path, funcname):
	spec = importlib.util.spec_from_file_location("__main__", path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	func = getattr(module, funcname)
	return func

class InputFileType():
	pass
class OutputFileType():
	pass

class RMSTemplateBook:
	def __init__(self, name, content):
		self.name = name
		self.content = content
		

class RMSTemplateLibrary:
	
	def __init__(self, rms, libpath):
		self.rms = rms
		rmsbookpaths = {} # Separated from book to avoid leaking path information
		rmschapterpaths = {}
		chaptermanifests_dict = {}
		for manifest_json_path in glob.glob(f"{libpath}/**/**/manifest.json"):
			with open(manifest_json_path, "rt") as f:
				manifest_json = json.load(f)
			
			chapterpath = os.path.dirname(manifest_json_path)
			chaptername = os.path.basename(chapterpath)
			bookpath = os.path.dirname(chapterpath)
			bookname = os.path.basename(bookpath)
			rmsbookpaths[bookname] = bookpath
			if bookname not in rmschapterpaths:
				chaptermanifests_dict[bookname] = {}
			chaptermanifests_dict[bookname][chaptername] = manifest_json
			if bookname not in rmschapterpaths:
				rmschapterpaths[bookname] = {}
			rmschapterpaths[bookname][chaptername] = chapterpath
			
		rmsbooks = {bookname: RMSTemplateBook(bookname, chaptermanifests) for bookname, chaptermanifests in chaptermanifests_dict.items()}   
		self.rmsbooks = rmsbooks
		self.rmsbookpaths = rmsbookpaths
		self.rmschapterpaths = rmschapterpaths
			
	def get_books(self):
		return self.rmsbooks

	def get_section(self, bookname, chaptername, bookmark):
		c = self.rmsbooks[bookname].content[chaptername]
		for idx in bookmark:
			if isinstance(idx, str):
				target_idx = []
				for tidx, t in enumerate(c["content"]):
					if "contentid" in t:
						if idx == t["contentid"]:
							target_idx.append(tidx)
				if len(target_idx) == 0:
					raise Exception("Cannot find bookmark")
				elif len(target_idx) > 1:
					raise Exception("Ambitious bookmark")
				else:
					idx = target_idx[0]
			c = c["content"][idx]
		return c
	
	def get_doc(self, bookname, chaptername, bookmark):
		section = self.get_section(bookname, chaptername, bookmark)
		if "doc" in section:
			with open(self.rmschapterpaths[bookname][chaptername] + "/" + section["doc"]["source"], "rt") as f:
				content = f.read()
			return {"type": section["doc"]["type"], "content": content}
		else:
			return None
	
	def load_template_func(self, bookname, chaptername, bookmark):
		bookpath = self.rmschapterpaths[bookname][chaptername]
		section = self.get_section(bookname, chaptername, bookmark)
		sourcepath = section["source"]
		funcname = section["name"]
		return _load_func(bookpath + "/" + sourcepath, funcname)

	
	def get_func_signature(self, bookname, chaptername, bookmark):
		s = inspect.signature(self.load_template_func(bookname, chaptername, bookmark))
		s = s.replace(parameters=tuple(s.parameters.values())[1:])
		return s
	
	def simulate(self, bookname, chaptername, bookmark, args=[], kwargs={}):
		func = self.load_template_func(bookname, chaptername, bookmark)
		return self.rms.simulate_template(func, args, kwargs)
		
	def run(self, bookname, chaptername, bookmark, args=[], kwargs={}):
		func = self.load_template_func(bookname, chaptername, bookmark)
		return self.rms.run_template(func, args, kwargs)
	
	def execute_builder(self):
		self.rms.execute_builder()
		
		
		
