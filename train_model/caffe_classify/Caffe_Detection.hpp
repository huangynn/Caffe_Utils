//
//  Caffe_Detection.hpp
//  DetectionTracking
//
//  Created by 黄缨宁 on 3/16/16.
//  Copyright © 2016 Yingning Huang. All rights reserved.
//

#ifndef Caffe_Detection_hpp
#define Caffe_Detection_hpp

#define CPU_ONLY
#include <caffe/caffe.hpp>
#include <opencv2/core/core.hpp>

#include <stdio.h>
#include <string>
#include <vector>

#include <memory>

using namespace std;
using namespace caffe;

namespace ev{
    typedef pair<float/*probability*/, int/*label*/> Prediction;
    class Caffe_Classifier
    {
    public:
        Caffe_Classifier(const string& model_file, const string& trained_file, const string& mean_file = "");
        std::vector<Prediction> classify(const cv::Mat& img);
        
    private:
        void set_mean(const string& mean_file);
        void preprocess(const cv::Mat& img, std::vector<cv::Mat>* input_channels);
        void wrap_input_layer(std::vector<cv::Mat>* input_channels);
        std::vector<float> predict(const cv::Mat& img);
        
        std::shared_ptr< Net<float> > net_;
        int num_channels_;
        cv::Mat mean_;
        cv::Size input_size_;
        
    };
};
#endif /* Caffe_Detection_hpp */