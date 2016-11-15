#!/usr/bin/python     
# -*- coding:utf-8 -*-  

address = "/Users/huangyingning/hyn/database/ucsd/ucsdpeds_gt/gt"
v_type = "/vidd"

import sys
import glob
import scipy.io as scio


mat_files = glob.glob(address + v_type + '/*.mat')

if __name__ == "__main__":
	for mat_name in mat_files:
		if "frame_full" not in mat_name:
			continue;
		outfile_name = mat_name.replace("_frame_full.mat", ".out")
		outfile = open(outfile_name, "wb")
		mat = scio.loadmat(mat_name)
		data = mat['fgt'][0][0][0][0]
		for line in data:
			real_line = line[0][0][0]
			for person in real_line:
				x = person[0]
				y = person[1]
				frame_id = person[2]
				outfile.write(str(x))
				outfile.write(" ")
				outfile.write(str(y))
				outfile.write(" ")
				outfile.write(str(frame_id))
				outfile.write("\n")
		outfile.close()


