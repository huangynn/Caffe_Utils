#!/usr/bin/env sh
# Create the image to lmdb inputs

echo "sh convert_data_lmdb.sh image_list_path lmdb_path size_h size_w need_gray"
TOOLS=/Users/huangyingning/hyn/downloads/caffe/build/tools

#图像文件的存放位置,写了绝对位置，这里用根目录就可以
TRAIN_DATA_ROOT=/
VAL_DATA_ROOT=/

IMAGE_LIST_ROOT=$1
ROOT_LMDB=$2
SIZE_H=$3
SIZE_W=$4
NEED_GRAY=$5

echo "sh convert_data_lmdb.sh $1 $2 $3 $4 $5"
#IMAGE_LIST_ROOT=/Users/huangyingning/hyn/database/train/gender/sample_list
#LMDB文件的存放位置
#ROOT_LMDB=/Users/huangyingning/hyn/database/train/gender

# Set RESIZE=true to resize the images to 256x256. Leave as false if images have
# already been resized using another tool.

#是否剪切为相同的大小
RESIZE=true
if $RESIZE; then
	RESIZE_HEIGHT=$SIZE_H
	RESIZE_WIDTH=$SIZE_W
else
	RESIZE_HEIGHT=0
	RESIZE_WIDTH=0
fi

if [ ! -d "$TRAIN_DATA_ROOT" ]; then
	echo "Error: TRAIN_DATA_ROOT is not a path to a directory: $TRAIN_DATA_ROOT"
	echo "Set the TRAIN_DATA_ROOT variable in create_imagenet.sh to the path" \
		"where the ImageNet training data is stored."
	exit 1
fi

if [ ! -d "$VAL_DATA_ROOT" ]; then
	echo "Error: VAL_DATA_ROOT is not a path to a directory: $VAL_DATA_ROOT"
	echo "Set the VAL_DATA_ROOT variable in create_imagenet.sh to the path" \
		"where the ImageNet validation data is stored."
	exit 1
fi

echo "Creating train lmdb..."

if $NEED_GRAY; then
	echo "Convert all image to be gray"
	GLOG_logtostderr=1 $TOOLS/convert_imageset \
		-resize_height=$RESIZE_HEIGHT \
		-resize_width=$RESIZE_WIDTH \
		-shuffle \
		-gray \
		$TRAIN_DATA_ROOT \
		$IMAGE_LIST_ROOT/train_samples.txt \
		$ROOT_LMDB/train

	echo "Creating val lmdb..."
	GLOG_logtostderr=1 $TOOLS/convert_imageset \
		-resize_height=$RESIZE_HEIGHT \
		-resize_width=$RESIZE_WIDTH \
		-shuffle \
		-gray \
		$VAL_DATA_ROOT \
		$IMAGE_LIST_ROOT/val_samples.txt \
		$ROOT_LMDB/val

$TOOLS/compute_image_mean $ROOT_LMDB/train \
	$ROOT_LMDB/mean.binaryproto
else
	GLOG_logtostderr=1 $TOOLS/convert_imageset \
		-resize_height=$RESIZE_HEIGHT \
		-resize_width=$RESIZE_WIDTH \
		-shuffle \
		$TRAIN_DATA_ROOT \
		$IMAGE_LIST_ROOT/train_samples.txt \
		$ROOT_LMDB/train

	echo "Creating val lmdb..."
	GLOG_logtostderr=1 $TOOLS/convert_imageset \
		-resize_height=$RESIZE_HEIGHT \
		-resize_width=$RESIZE_WIDTH \
		-shuffle \
		$VAL_DATA_ROOT \
		$IMAGE_LIST_ROOT/val_samples.txt \
		$ROOT_LMDB/val

$TOOLS/compute_image_mean $ROOT_LMDB/train \
	$ROOT_LMDB/mean.binaryproto
fi
echo "Done."
