import tarfile
import zipfile

class Compress:

	@staticmethod
	def open(file, mode):

		ext = file.split('.')[-1]
		if ext == "zip":
			i =  CompressZip()
		else:
			mode += ":gz"
			i = CompressTar()
		
		i.open(file, mode)

		return i
	
	@staticmethod
	def check(file):
		if CompressTar.check(file):
			return True

		if CompressZip.check(file):
			return True
		
		return False




class CompressInterface():
	
	def __init__(self):
		'''Init'''
		raise NotImplemented()

	def open(self,file, mode):
		'''init compress instance'''
		raise NotImplemented()

	def add (self, file):
		''' add file'''
		raise NotImplemented()

	def close(self):
		'''close it'''
		raise NotImplemented()

	@staticmethod
	def check(file):
		'''validate pack format'''
		raise NotImplemented()
		

	def extract(self, file):
		'''uncompress file'''
		raise NotImplemented()

	def __iter__(self):
		raise NotImplemented()



class CompressTar(CompressInterface):
	def __init__(self):
		self.__instance = None

	def open(self, file, mode):
		self.__instance = tarfile.open(file, mode)
	
	def add(self, file):
		self.__instance.add(file)

	@staticmethod
	def check(file):
		return tarfile.is_tarfile(file)

	def extract(self, file):
		return self.__instance.extractfile(file).read()

	def __iter__(self):
		return iter(self.__instance.getnames())

	def close(self):
		self.__instance.close()





class CompressZip(CompressInterface):
	
	def __init__(self):
		self.__instance = None

	def open(self, file, mode):
		self.__instance = zipfile.ZipFile(file, mode)
	
	def add(self, file):
		self.__instance.write(file)

	@staticmethod
	def check(file):
		return zipfile.is_zipfile(file)

	def extract(self, file):
		return self.__instance.read(file)

	def __iter__(self):
		for item in self.__instance.namelist():
			if item.endswith('/'):
				continue

			yield item


	def close(self):
		self.__instance.close()


