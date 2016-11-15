#!/usr/bin/python     
# -*- coding:utf-8 -*-  

import cv2
import glob
import os
import random
import sys
import numpy as np
#输入的样本目录,可以拼接
#data_path = '/Users/huangyingning/hyn/database/caffe_sample/0;/Users/huangyingning/hyn/database/caffe_sample/2;/Users/huangyingning/hyn/database/neg/scene/zhuhai/neg_sample'
#data_path = '/Users/huangyingning/hyn/database/neg/human_part_neg'
#data_path = '/Users/huangyingning/hyn/database/pos/prd_head;/Users/huangyingning/hyn/database/caffe_sample/1'
#data_path = '/Users/huangyingning/hyn/database/outputGender/1'
#;/Users/huangyingning/hyn/database/pos/pointing4_data;/Users/huangyingning/hyn/database/gender_data'
#data_path = "/Users/huangyingning/hyn/database/neg/scene/elevator/neg_elevator_scene;/Users/huangyingning/hyn/database/neg/common_neg"
#data_path =  "/Users/huangyingning/hyn/database/gender/crop_male;/Users/huangyingning/hyn/database/gender/rotate_male;/Users/huangyingning/hyn/database/gender/resize_male_70_70"
#输出目录，只能有一个
#dst_path = "/Users/huangyingning/hyn/database/train/gender_1027"
#图像resize到所需尺寸
#image_size = (40, 40)
#训练时validate样本比例
#validation_percent = 0.1
#用于测试的样本比例
#test_percent = 0.1
#样本标签
#flag = 1

#输出图片到新文件夹
create_image = False

if __name__ == "__main__":
	image_count = 0
	if len(sys.argv) != 6:
		print "Usage: python create_sample_list.py data_path dst_path validation_percent test_percent flag"
	data_path = sys.argv[1]
	dst_path = sys.argv[2]
	validation_percent = sys.argv[3]
	test_percent = sys.argv[4]
	flag = sys.argv[5]
	#ensure base dir
	if not os.path.exists(dst_path):
		os.makedirs(dst_path)
	if not os.path.exists(dst_path+'/sample_list'):
		os.makedirs(dst_path+'/sample_list')
	paths = data_path.split(';')
	for j in paths:
		j = os.path.expanduser(j)
		for root, dirs, files in os.walk(j):
			for item in files:
				item = root + '/' + item
				img = cv2.imread(item)
				if img is None: continue
				random_val = random.random()
				#calculate category
				category = 'train_samples'
				if random_val >= 0 and random_val < float(validation_percent):
					category = 'val_samples'
				if random_val >= float(validation_percent) and random_val < float(validation_percent) + float(test_percent):
					category = 'test_samples'
				file_name = item
				#如果要创建图像文件
				if create_image == True:
					path = dst_path + '/' + category
					#ensure base_dir/category
					if not os.path.exists(path): 
						os.makedirs(path)
					subdir = str(flag)
					#ensure base_dir/category/flag
					if not os.path.exists(os.path.dirname(path + '/' + subdir)):
						os.makedirs(os.path.dirname(path + '/' + subdir))	
					file_name = path + '/' + subdir + '/' + str(image_count) + '.jpg'
					#resize image
					img = cv2.imread(item, 1)
					img_resized = cv2.resize(img, dsize = image_size, interpolation = cv2.INTER_LINEAR)
					cv2.imwrite(file_name, img_resized)
				f = open(dst_path+'/sample_list' + '/' + category + '.txt', 'a+')
				f.write(file_name + ' '+ str(flag) + '\n')
				f.close()
				#print file_name + "  process done"
				image_count += 1
	print "add " + str(image_count) + " file names to " + dst_path + " as flag "+ str(flag)
	





					

	
	
	
