data_path = '/Users/huangyingning/hyn/database/outputGender/1/'
flag = 1
bin_file = 'caffe_classify/build/classifier'
deploy_file = '/Users/huangyingning/hyn/database/train/gender/deploy.prototxt'
model_file = '/Users/huangyingning/hyn/database/train/gender/_iter_111382.caffemodel'

cmd = './'+bin_file+' '+deploy_file+' '+model_file+ ' '

import os
import glob

wrong_time = 0
right_time = 0
wrong_file = []
if __name__ == "__main__":
	paths = data_path.split(';')
	print paths
	for j in paths:
		for i in os.walk(j):
			image_files = glob.glob(i[0] + '/*.jpg')
			for item in image_files:
				output = os.popen(cmd + str(item))
				if (output.read() == flag):
					right_time += 1
					print output.read()
					print "hahaha1"
				else:
					wrong_time += 1
					wrong_file.append(i)
					print 'hahaha'
			print wrong_time, right_time
	print wrong_file
			
	
