
tool_path="/Users/huangyingning/hyn/Mango/tools/train_model"
sample_list_path="/Users/huangyingning/hyn/database/train/head_1108"
lmdb_path="/Users/huangyingning/hyn/database/train/head_1108"

pos_path="/Users/huangyingning/hyn/database/head/pointing4_rotate;/Users/huangyingning/hyn/database/head/prd_head_rotate;/Users/huangyingning/hyn/database/head/adience_rotate"
neg_path="/Users/huangyingning/hyn/database/head/neg/common_neg_rotate;/Users/huangyingning/hyn/database/head/neg/human_part_neg_rotate;/Users/huangyingning/hyn/database/head/neg/cascade_neg_rotate;/Users/huangyingning/hyn/database/head/neg/unchoosen_human_part_neg_rotate;/Users/huangyingning/hyn/database/head/neg/prd_non_head_rotate"

need_gray=false

size_h=50
size_w=50

echo "Check sample list"
if [ -d "$sample_list_path/sample_list" ]; then
	echo "Clear $sample_list_path/sample_list"
	rm -rf $sample_list_path/sample_list
fi

python $tool_path/create_sample_list.py $pos_path $sample_list_path 0.1 0 1
python $tool_path/create_sample_list.py $neg_path $sample_list_path 0.1 0 0

echo "Check lmdb path"
if [ -d "$lmdb_path/train" ]; then
	echo "Clear $lmdb_path/train"
	rm -rf $lmdb_path/train
fi

if [ -d "$lmdb_path/val" ]; then
	echo "Clear $lmdb_path/val"
	rm -rf $lmdb_path/val
fi

sh $tool_path/convert_data_lmdb.sh $sample_list_path/sample_list $lmdb_path $size_h $size_w $need_gray


