#!/usr/bin/python     
# -*- coding:utf-8 -*-  
import numpy as np
import matplotlib.pyplot as plt
import os,sys,caffe
#import argparse


# 输入的数据为一个ndarray，尺寸可以为(n, height, width)或者是 (n, height, width, 3)
# 前者即为n个灰度图像的数据，后者为n个rgb图像的数据
# 在一个sqrt(n) by sqrt(n)的格子中，显示每一幅图像

def visualize(data, padsize=1, padval=1):
	# 对输入的图像进行normlization
	data = (data - data.min()) / (data.max() - data.min())

	# 强制性地使输入的图像个数为平方数，不足平方数时，手动添加几幅
	n = int(np.ceil(np.sqrt(data.shape[0])))
	# 强制性地使输入的图像个数为平方数，不足平方数时，手动添加几幅
	padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
	data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))

	# 将所有输入的data图像平复在一个ndarray-data中
	data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
	data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
	plt.imshow(data)
	#plt.axis('off')
	plt.show()

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "python visualize_model.py deploy_file_path model_file_path"
		sys.exit()
	
	caffe_deploy = sys.argv[1]
	caffe_model = sys.argv[2]
	net = caffe.Net(caffe_deploy, caffe_model, caffe.TEST)
	plt.rcParams['figure.figsize'] = (8, 8)
	plt.rcParams['image.interpolation'] = 'nearest'
	plt.rcParams['image.cmap'] = 'gray'
	print "paramerters can be show:"
	print [(k, v[0].data.shape) for k, v in net.params.items()]
	print "features can be show:"
	print [(k, v.data.shape) for k, v in net.blobs.items()]
	print net.blobs.items()[0][1].data.shape[2:]
	while True:
		r = raw_input('Input a layer name or input exit:\n ')
		if r == 'exit':
			sys.exit()
		t = raw_input('f for feature, p for parameter:\n')
		data_type = ''
		if t == 'p':
			weight = net.params[r][0].data
			visualize(weight.transpose(0, 2, 3, 1))
			data_type = 'parameter'
		if t == 'f':
			feature = net.blobs[r].data[0]
			visualize(feature)
			data_type = 'feature'
		print "show " + r + " layer as " + data_type


