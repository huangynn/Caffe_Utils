import os
import sys

#
dst_server='http://labelme.extremevision.com.cn:'

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "Usage: python "+ sys.argv[0] + " file_contains_all_image_paths"
		exit(-1)
	file_name = sys.argv[1]
	dir_name = file_name.split('.')[0]
	dir_name = '/mnt/database/required/' + dir_name
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
	f = open(file_name, 'r')
	while 1:
		line = f.readline()
		if not line:
			break
		file_to_get = dst_server + line
		cmd = 'wget -P ' + dir_name + ' ' + file_to_get
		os.system(cmd)
	

		

	
	
	
