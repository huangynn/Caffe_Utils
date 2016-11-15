import os
import sys

#
sample_file_name='/Users/huangyingning/Downloads/gender_male_picpath.txt'
dir_name='/Users/huangyingning/hyn/database/gender/male'

if __name__ == "__main__":
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
	f = open(sample_file_name, 'r')
	while 1:
		line = f.readline()
		if not line:
			break
		line = line.replace('"', '').replace('\'','').replace('\n','')
		file_to_get = line
		new_file_name = line.replace('/', '_')
		new_file_nmae = new_file_name.lstrip().lstrip('_')
		cmd = 'wget -O ' + dir_name + '/' + new_file_name + ' ' + file_to_get
		print cmd
		os.system(cmd)
	

		

	
	
	
