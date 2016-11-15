#!/usr/bin/python     
# -*- coding:utf-8 -*-  
import cv2
import os
import sys
import glob

#运行脚本前设置好
src_image_dir = '/Users/huangyingning/hyn/database/neg/scene/zhuhai/origin'
output_dir = '/Users/huangyingning/hyn/database/neg/scene/zhuhai/neg_sample'
#输出为灰度
load_flag = 1 # 0为灰度
#样本resize
sample_resize_size = (45,45)
#每次改变的尺度
scale_factor = 1.1
#最小size
min_size = (20,20)
#最大size
max_size = (85,85)
#步长
step_size = 6

#(height, width)
resize_size = (640, 320)
#after resize (ymin, xmin, ymax, xmax)
#detect_region = (25, 125, 250, 600) 
detect_region = ()

if __name__ == "__main__":
	#存储所需要的样本尺度
	min_h = min_size[0]
	min_w = min_size[1]
	max_h = max_size[0] if max_size[0] > 0 else height
	max_w = max_size[1] if max_size[1] > 0 else width
	i = min_h
	j = min_w
	scales = []
	while(i <= max_h and j <= max_w):
		scales.append((i,j))
		i = round(i * scale_factor)
		j = round(j * scale_factor)
	print scales
	image_files = glob.glob(src_image_dir + '/*.png')
	print "process "+ src_image_dir + ", contains " + str(len(image_files)) + " images."
	sample_cnt = 0
	image_cnt = 0
	for image_name in image_files:
		image = cv2.imread(image_name, load_flag)
		height, width, channels = image.shape
		if len(resize_size) == 2:
			image = cv2.resize(image,resize_size)
			print image.shape
		if len(detect_region) == 4:
			image = image[detect_region[0]:detect_region[2], detect_region[1]:detect_region[3], :] #crop frame
		height, width, channels = image.shape
		i = 0 + image_cnt*step_size
		#滑动窗口
		while (i< height):
			j = 0 + image_cnt*step_size/len(image_files)
			while (j < width):
				for scale in scales:
					m_h = i + scale[0]
					m_w = j + scale[1]
					if m_h < height and m_w < width:
						sample = image[i:m_h, j:m_w, :]
						if sample_resize_size[0] > 0 and sample_resize_size[1] >0 :
							sample = cv2.resize(sample, sample_resize_size)
						sample_name = output_dir + '/' + str(i)+'_'+str(j)+'_'+str(m_h)+'_'+str(m_w) + '.jpg'
						cv2.imwrite(sample_name, sample)
						sample_cnt += 1
				j = j + step_size
			i = i + step_size
		image_cnt += 1

	print "generate " + str(sample_cnt) + " samples."





