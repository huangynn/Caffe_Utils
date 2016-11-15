#-e后写入select语句，修改文件存放地址即可
#mysql -h host_ip -P port -u user name -p密码 -e"命令" 数据库名称 > 输出结果存放地址
mysql -h 120.27.240.32 -P 3306 -u root -pExtremeVision2016 -e"select picPath from t_manual_copy where base_mark = 0 and picDate = '2016-03-17'" sys-dev > 0317_0.txt
