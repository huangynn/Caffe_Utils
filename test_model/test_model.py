#!/usr/bin/python
# -*- coding:utf-8 -*-
import caffe
import numpy as np
import argparse
import fileinput
import matplotlib.pyplot as plt
import os
import json

def get_parser():
	parser = argparse.ArgumentParser(prog='caffe test warper')
	# SOURCE REQUIRED
	parser.add_argument('--src_path', required=True, help='Source path of the image list: image_path label')
	parser.add_argument('--dst_path', required=True, help='Dst path of image test result and roc curve')
	parser.add_argument('--draw_performance', action='store_true', default=False, help='Draw roc & precision-recall curve based on the test images')
	parser.add_argument('--model_def', help='Model definition file.')
	parser.add_argument('--pretrained_model', help='Trained model weights file.')
	parser.add_argument('--mean_file',help='Data set image mean of [Channels x Height x Width] dimensions ' + '(numpy array). Set to '' for no mean subtraction.')
	parser.add_argument( '--gpu',action='store_true', help='Switch for gpu computation.')
	return parser

def caffe_test(args):
	if args.gpu:
		caffe.set_mode_gpu()
		print('GPU mode')
	else:
		caffe.set_mode_cpu()
		print('CPU mode')
	mean = None
	args.src_path = os.path.expanduser(args.src_path)
	args.model_def = os.path.expanduser(args.model_def)
	args.pretrained_model = os.path.expanduser(args.pretrained_model)
	if args.mean_file:
		args.mean_file = os.path.expanduser(args.mean_file)
	if args.mean_file:
		if args.mean_file.endswith('npy'):
			mean = np.load(args.mean_file)
		if args.mean_file.endswith('binaryproto'):
			blob = caffe.proto.caffe_pb2.BlobProto()
			data = open(args.mean_file , 'rb' ).read()
			blob.ParseFromString(data)
			mean = np.array( caffe.io.blobproto_to_array(blob))[0]
	classifier = caffe.Classifier(args.model_def, args.pretrained_model, mean= mean,raw_scale=255)# channel_swap=(2,1,0),
	in_blob_name = classifier.inputs[0]
	channel_num = classifier.blobs[in_blob_name].data.shape[1]
	is_gray = channel_num == 1
	#如果channel为3则从RGB-》BGR
	if channel_num == 3:
		classifier.transformer.set_channel_swap(in_blob_name, (2,1,0))
	db = {}
	for line in fileinput.input(args.src_path):
		items = [k.strip() for k in line.split(' ') if k.strip()]
		#1*C ndarray C是类别数目
		prediction = classifier.predict([caffe.io.load_image(items[0], not is_gray), ], False)[0]
		lable_probs = {}
		for i, value in enumerate(prediction):
			lable_probs[str(i)] = str(value)
		db[items[0]] = {}
		db[items[0]]['label'] = items[1]
		db[items[0]]['predict'] = lable_probs
		#print items[1], lable_probs
	with open(args.dst_path+'/caffe_test_record.json', 'w') as f:
			json.dump(db, f)
	return db

#对摸一个lable做1vR的指标计算
def get_performance(db, threshold, lable):
	tp, tn, fp, fn = 0, 0, 0, 0
	for k,v in db.iteritems():
		#print v
		#print tp,tn,fp,fn
		if float(v['predict'][lable]) >= threshold:
			if v['label'] == lable:	tp += 1
			else:	fp += 1
		else:
			if v['label'] == lable:	fn += 1
			else:	tn += 1
	return tp, tn, fp, fn

#画roc曲线
def draw(db, lable, model):
	print 'Calculate roc & pr'

	roc_data = []
	pr_data = []
	for i in range(0, 100, 1):
		tp, tn, fp, fn = get_performance(db, float(i)/100, lable)
		tpr = float(tp) / (tp + fn)
		fpr = float(fp) /(tn + fp)
		roc_data.append([fpr, tpr])
		precision = float(tp)/(tp + fp)
		recall = float(tp)/(tp + fn)
		pr_data.append([recall, precision])
	auc = 0.
	prev_x = roc_data[0][0]
	for x,y in roc_data:
		if x != prev_x:
			print x,y,prev_x
			auc += (prev_x - x) * y
			prev_x = x
	print 'Draw roc with AUC='+str(auc)
	roc_x = [v[0] for v in roc_data]
	roc_y = [v[1] for v in roc_data]
	pr_x = [v[0] for v in pr_data]
	pr_y = [v[1] for v in pr_data]
	f, (ax1, ax2) = plt.subplots(1, 2)
	ax1.plot(roc_x, roc_y)
	ax1.set_title('ROC curve of %s (AUC = %.4f)' % (model.split('/')[-1],auc))
	ax1.set_xlabel('False Positive Rate')
	ax1.set_ylabel('True Positive Rate')
	ax2.plot(pr_x,pr_y)
	ax2.set_title('PR curve of %s ' % (model.split('/')[-1]))
	ax2.set_xlabel('Recall')
	ax2.set_ylabel('Precision')

	plt.show()

if __name__ == '__main__':
	parser = get_parser()
	args = parser.parse_args()

	if os.path.exists(args.dst_path+'/caffe_test_record.json'):
		db = json.load(file(args.dst_path+'/caffe_test_record.json'))
	else:
		db = caffe_test(args)
	if args.draw_performance:
		draw(db,'1', args.pretrained_model)


