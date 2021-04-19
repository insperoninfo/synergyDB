from .models import CommonDocument, Document, Directory
import os


def check_if_file_exists(directory, file):
	file_path = os.path.join(directory.str(), file.name)
	print(file_path)
	docs = Document.objects.filter(directory=directory).filter(file=file_path)
	
	
	if not docs :
		print('Does NOT EXIST')
		return False
	else:
		print("EXIST")
		return True
		


