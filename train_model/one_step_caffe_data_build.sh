#!/usr/bin/env sh
# Create the image to lmdb inputs

pos_data_path='/Users/huangyingning/Desktop/火焰标图/火焰;/Users/huangyingning/Desktop/FLAME_TRAINING/yes'
neg_data_path='/Users/huangyingning/Desktop/火焰标图/不是火焰;/Users/huangyingning/Desktop/FLAME_TRAINING/no'

echo $pos_data_path $neg_data_path
valid_percent=0.1
test_percent=0.1
dst_path=/Users/huangyingning/hyn/models/flame_cnn
size_h=40
size_w=40
python create_sample_list.py $pos_data_path $dst_path $valid_percent $test_percent 1
python create_sample_list.py $neg_data_path $dst_path $valid_percent $test_percent 0
python create_sample_list.py $neg_data_path $dst_path $valid_percent $test_percent 0
python create_sample_list.py $neg_data_path $dst_path $valid_percent $test_percent 0
bash convert_data_lmdb.sh $dst_path/sample_list  $dst_path $size_h $size_w


