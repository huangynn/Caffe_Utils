#include "Caffe_Detection.hpp"
#include <opencv2/highgui.hpp>
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <boost/filesystem.hpp>

using namespace std;
using namespace ev;

void travel_files(const std::string& root,  const std::string& file_type, std::vector<std::string>& file_names)
{
	if (!boost::filesystem::exists(root)) return;
	boost::filesystem::directory_iterator end_itr;
	for (boost::filesystem::directory_iterator itr(root); itr != end_itr; ++itr)
	{
		if (boost::filesystem::is_directory(itr->status()))
			travel_files(itr->path().string(), file_type, file_names);

		std::string cur_name = itr->path().string() ;
		int len = int(cur_name.size() - file_type.size());
		if (cur_name.substr(len) == file_type)
			file_names.push_back(cur_name);
	}
	return;
}

int main(int argc, char** argv)
{
	if(argc != 5 && argc != 6)
	{
		std::cout<<"Usage:"<<endl
			<<argv[0]<<" deploy.prototxt network.caffemodel img_dir flag mean.binaryproto(if exists mean)"<<endl;
		return -1;
	}

	string deploy= argv[1];
	string model = argv[2];
	string img_dir = argv[3];
	string s_flag = argv[4];
	int flag = atoi(s_flag.c_str());
	string mean = "";
	if(argc == 6)
		mean = argv[5];

	ev::Caffe_Classifier classifier(deploy, model, mean);

	vector<string> files;
	travel_files(img_dir, ".jpg", files);
	cout << "flag is "<< flag << " and below is wrong classification"<<endl;
	size_t right_times = 0, wrong_times = 0;

	for(auto item:files)
	{
		cv::Mat img=cv::imread(item);
		std::vector<ev::Prediction>  cnn_result = classifier.classify(img);
		if(cnn_result[0].second != flag)
		{
			cout<<item+' '<< endl ;
			wrong_times++;
		}
		else
			right_times++;

	}
	cout << "right times:" << right_times<< "  wrong times:"<< wrong_times << endl;

	return 0;

}
