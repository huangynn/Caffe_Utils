#!usr/bin/python
# -*- coding: utf-8 -*-
''' author: inory '''
import os, sys
import argparse
import cv2
import numpy as np
import os

global total_count
total_count = 0
def get_parser():
	parser = argparse.ArgumentParser(prog='Data augmentation tool')

	# SOURCE REQUIRED
	src_group = parser.add_argument_group('SOURCE')
	src_group.add_argument('--src_path', required=True, help='source path of the images')

	# DESTINATION REQUIRED
	dst_group = parser.add_argument_group('DESTINATION')
	dst_group.add_argument('--dst_path', required=True, help='destinate path to save processed images')

	# PROCESS OPTIONAL
	process_group = parser.add_argument_group('PROCESS')
	## gray
	process_group.add_argument('--gray', action='store_true', default=False, help='Convert images to grayscale')
	## flip
	process_group.add_argument('--flip', action='store_true', default=False, help='Horizontally flip the images')
	## rotate
	process_group.add_argument('--rotate', nargs=2, type=float, metavar=('ANGLE_MIN', 'ANGLE_MAX'), help='Randomly rotate the images by angle specified by 2 arguments [angle_min, angle_max]')

	## blur
	### avg_blur
	process_group.add_argument('--avg_blur', nargs=2, type=int, metavar=('KERNEL_W', 'KERNEL_H'), help='Blurring the images by taking the average of all the pixels under kernel area and replacing the central element with this average')
	### gaussian_blur
	process_group.add_argument('--gaussian_blur', nargs=4, type=int, metavar=('KERNEL_W', 'KERNEL_H', 'SIGMAX', 'SIGMAY'), help='Apply a gaussian filter to blur the images')
	### median_blur
	process_group.add_argument('--median_blur', type=int, default=0, metavar='KERNEL_SIZE', help='Apply a median filter to blur the images')

	## scale_size
	process_group.add_argument('--scale_size', nargs=2, type=int, metavar=('WIDTH', 'HEIGHT'), help='Scale the images to a specified size')
	## scale_factor
	process_group.add_argument('--scale_factor', nargs=2, type=float, metavar=('FX', 'FY'), help='Scale the images by factors')

	## translation
	process_group.add_argument('--translation', nargs=4, type=int, metavar=('TX_MIN', 'TX_MAX', 'TY_MIN', 'TY_MAX'), help='Randomly shifting the images in a range of [TX_MIN, TX_MAX] and a range of [TY_MIN, TY_MAX] through both directions')

	## affine transformation
	process_group.add_argument('--affine', default=None, help='Applyparameters of affine transformation including a pair of three points and the output size')
	## crop
	process_group.add_argument('--random_crop', nargs=3, type=int, metavar=('CROP_NUM', 'CROP_WIDTH', 'CROP_HEIGHT'), help='Randomly crop the images to a specified size given by crop_size=(crop_num, crop_width, crop_height)')

	return parser

def random_crop(img, setting, path):
	crop_num, crop_width, crop_height = setting
	img_h, img_w = img.shape[:2]
	global total_count
	for i in xrange(crop_num):
		crop_x = np.random.randint(img_w - crop_width)
		crop_y = np.random.randint(img_h - crop_height)
		crop_img = img[crop_y : crop_y + crop_height, crop_x : crop_x + crop_width, ...]
		cv2.imwrite(path[:-4]+'_crop_%d' % (i+1) + path[-4:], crop_img)
		total_count += 1

def process(args, src, dst):
	if not os.path.exists(dst):
		os.makedirs(dst)
	if os.listdir(dst):
		for f in [os.path.join(dst, img_name) for img_name in os.listdir(dst)]:
			os.remove(f)

	global total_count
	for root, dirs, files in os.walk(src):
		for file in files:
			img_name = root + '/' + file

			img = cv2.imread(img_name)
			if img is None:
				continue
			save_path = os.path.join( dst, str(total_count) + os.path.basename(img_name) )
			# process
			if args.gray:
				img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			if args.flip:
				img = img[:,::-1,...]

			if args.random_crop:
				random_crop(img, args.random_crop, save_path)

			if args.rotate:
				angle_min, angle_max = args.rotate
				angle = np.random.randint(angle_min*10, angle_max*10)*1.0/10
				rows, cols = img.shape[:2]
				M = cv2.getRotationMatrix2D(( cols/2, rows/2 ), angle, 1)
				img =  cv2.warpAffine(img, M, (cols, rows))

			if args.avg_blur:
				kernel_size = tuple(args.avg_blur)
				img = cv2.blur(img, kernel_size)

			if args.gaussian_blur:
				kernel_size = tuple(args.gaussian_blur[:2])
				sigmaX, sigmaY = args.gaussian_blur[2:]
				img = cv2.GaussianBlur(img, kernel_size, sigmaX, sigmaY, -1)

			if args.median_blur:
				kernel_size = args.median_blur
				img = cv2.medianBlur(img, kernel_size)

			if args.scale_size:
				width, height = args.scale_size
				img = cv2.resize(img, (width, height))

			if args.scale_factor:
				fx, fy = args.scale_factor
				img = cv2.resize(img, (0,0), fx=fx, fy=fy)

			if args.translation:
				tx_min, tx_max = args.translation[:2]
				ty_min, ty_max = args.translation[2:]
				tx = np.random.randint(tx_min, tx_max)
				ty = np.random.randint(ty_min, ty_max)
				rows, cols = img.shape[:2]
				M = np.float32([[1,0,tx], [0,1,ty]])
				img = cv2.warpAffine(img, M, (cols, rows))
			cv2.imwrite(save_path, img)
			total_count += 1

	print "Process " + str(total_count) + " complete."

def main():
	parser = get_parser()
	args = parser.parse_args()
	dst_path = args.dst_path
	if args.src_path:
		src_path = args.src_path
		if src_path[-1] != '/':
			src_path += '/'
		process(args, src_path, dst_path)

if __name__ == '__main__':
	main()
