#!/usr/bin/python     
# -*- coding:utf-8 -*-

import cv2
import glob
import os
import random
import sys

#输入图像目录
data_path ="/Users/huangyingning/hyn/database/pos/HeadPoseImageDatabase"
#输出图像目录
dst_path ="/Users/huangyingning/hyn/database/pos/pointing4_data"

if __name__ == "__main__":
	image_count = 0
	#ensure base dir
	if not os.path.exists(dst_path):
			os.makedirs(dst_path)
	for i in os.walk(data_path):
		image_files = glob.glob(i[0] + '/*.jpg')
		for item in image_files:
			#crop image using skin color information
			img = cv2.imread(item, 1)
			txt = item[:-3] + "txt"
			if not os.path.exists(txt): continue
			file = open(txt, "r")
			x_c = 0
			y_c = 0
			width = 0
			height = 0
			while 1:
				line = file.readline()
				line = file.readline()
				line = file.readline()
				x_c = int(file.readline())
				y_c = int(file.readline())
				width = int(file.readline())
				height = int(file.readline())
				print x_c, y_c, width, height	
				break
			file.close()
			half_width = width / 2 + 50
			half_height = height /2 + 50
			
			ly = 0
			lx = 0
			hy, hx = img.shape[:2]
			if y_c - half_height >= 0:
				ly = y_c - half_height
			if y_c + half_height <= hy:
				hy = y_c + half_height
			if x_c - half_width >= 0:
				lx = x_c - half_width
			if x_c + half_width <= hx:
				hx = x_c + half_width
			cropped_img = img[ly:hy, lx:hx, : ]

			path = dst_path 
			#ensure base_dir/category
			if not os.path.exists(path): 
				os.makedirs(path)
			file_name = path + '/' + str(image_count) + '.jpg'
			#ensure base_dir/category/flag
			if not os.path.exists(os.path.dirname(file_name)):
				os.makedirs(os.path.dirname(file_name))			
			cv2.imwrite(file_name, cropped_img)
			image_count += 1
	
