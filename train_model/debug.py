import os, sys

root = '/Users/huangyingning/hyn/database/gender/female'
img_names = os.listdir(root)
img_path = os.path.join(root, img_names[0])
print img_path
