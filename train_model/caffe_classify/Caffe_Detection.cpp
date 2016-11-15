//
//  Caffe_Detection.cpp
//  DetectionTracking
//
//  Created by 黄缨宁 on 3/16/16.
//  Copyright © 2016 Yingning Huang. All rights reserved.
//

#include "Caffe_Detection.hpp"


#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace caffe;
using namespace ev;

Caffe_Classifier::Caffe_Classifier(const string& model_file,
                                   const string& trained_file,
                                   const string& mean_file)
{
#ifdef CPU_ONLY
    Caffe::set_mode(Caffe::CPU);
#else
    Caffe::set_mode(Caffe::GPU);
#endif
	fLI::FLAGS_minloglevel = google::ERROR;
    //加载网络
    net_.reset(new Net<float>(model_file, TEST));
    net_->CopyTrainedLayersFrom(trained_file);
    
    CHECK_EQ(net_->num_inputs(), 1) << "Network should have only one input.";
    CHECK_EQ(net_->num_outputs(), 1) << "Network should have only one input.";
    
    Blob<float>* input_layer = net_->input_blobs()[0];
    num_channels_ = input_layer->channels();
    
    CHECK(num_channels_ == 3 || num_channels_ == 1) << "Input layer should have 1 or 3 channels";
    input_size_ = cv::Size(input_layer->width(), input_layer->height());
    
    if (!mean_file.empty())
        set_mean(mean_file);
	fLI::FLAGS_minloglevel = google::INFO;
}

void Caffe_Classifier::set_mean(const string& mean_file)
{
    //把mean_file转成二进制的proto
    BlobProto blob_proto;
    ReadProtoFromBinaryFileOrDie(mean_file.c_str(), &blob_proto);
    
    Blob<float> mean_blob;
    mean_blob.FromProto(blob_proto);
    
    CHECK_EQ(mean_blob.channels(), num_channels_)
    << "Number of channels of mean file doesn't match input layer.";
    
    //32位 BGR 或者 Gray ，用于图像没问题
    std::vector<cv::Mat> channels;
    float* data = mean_blob.mutable_cpu_data();
    for (int i = 0; i < num_channels_; ++i) {
        //逐个通道获取数据
        cv::Mat channel(mean_blob.height(), mean_blob.width(), CV_32FC1, data);
        channels.push_back(channel);
        data += mean_blob.height() * mean_blob.width();
    }
    
    //通道图像融合
    cv::Mat mean;
    cv::merge(channels, mean);
    
    //计算平均图像
    cv::Scalar channel_mean = cv::mean(mean);
    mean_ = cv::Mat(input_size_, mean.type(), channel_mean);
    
}

void Caffe_Classifier::wrap_input_layer(std::vector<cv::Mat> *input_channels)
{
    Blob<float>* input_layer = net_->input_blobs()[0];
    
    int width = input_layer->width();
    int height = input_layer->height();
    
    float* input_data = input_layer->mutable_cpu_data();
    
    for (int i = 0; i < input_layer->channels(); ++i) {
        cv::Mat channel(height, width, CV_32FC1, input_data);
        input_channels->push_back(channel);
        input_data += width * height;
    }
}

void Caffe_Classifier::preprocess(const cv::Mat &img, std::vector<cv::Mat> *input_channels)
{
    cv::Mat sample;
    if (img.channels() == 3 && num_channels_ == 1)
        cv::cvtColor(img, sample, cv::COLOR_BGR2GRAY);
    else if (img.channels() == 4 && num_channels_ == 1)
        cv::cvtColor(img, sample, cv::COLOR_BGRA2GRAY);
    else if (img.channels() == 4 && num_channels_ == 3)
        cv::cvtColor(img, sample, cv::COLOR_BGRA2BGR);
    else if (img.channels() == 1 && num_channels_ == 3)
        cv::cvtColor(img, sample, cv::COLOR_GRAY2BGR);
    else
        sample = img;
    
    cv::Mat sample_resized;
    if (sample.size() != input_size_)
        cv::resize(sample, sample_resized, input_size_);
    else
        sample_resized = sample;
    
    cv::Mat sample_float;
    if (num_channels_ == 3)
        sample_resized.convertTo(sample_float, CV_32FC3);
    else
        sample_resized.convertTo(sample_float, CV_32FC1);
    
    cv::Mat sample_normalized;
    
    if (mean_.empty())
        sample_normalized = sample_float;
    else
        cv::subtract(sample_float, mean_, sample_normalized);
    
    cv::split(sample_normalized, *input_channels);
    
    CHECK(reinterpret_cast<float*>(input_channels->at(0).data)
          == net_->input_blobs()[0]->cpu_data())
    << "重新组织图像通道失败";
    
}

std::vector<float> Caffe_Classifier::predict(const cv::Mat& img)
{
    Blob<float>* input_layer = net_->input_blobs()[0];
    input_layer->Reshape(1, num_channels_,
                         input_size_.height, input_size_.width);
    //前向计算所有层
    net_->Reshape();
    
    std::vector<cv::Mat> input_channels;
    
    wrap_input_layer(&input_channels);
    
    preprocess(img, &input_channels);
     
    net_->ForwardPrefilled();
    
    /* Copy the output layer to a std::vector */
    Blob<float>* output_layer = net_->output_blobs()[0];
    const float* begin = output_layer->cpu_data();
    const float* end = begin + output_layer->channels();
    return std::vector<float>(begin, end);
}

static bool prediction_cmp(const std::pair<float, int>& lhs,
                           const std::pair<float, int>& rhs)
{
    return lhs.first >rhs.first;
}

std::vector<Prediction> Caffe_Classifier::classify(const cv::Mat &img)
{
    vector<Prediction> pairs;
    std::vector<float> output = predict(img);
    size_t len = output.size();
    for (size_t i = 0; i < len; i++)
        pairs.push_back(std::make_pair(output[i], i));
    std::sort(pairs.begin(), pairs.end(), prediction_cmp);
    return pairs;
}

