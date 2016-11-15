project (classifier)

cmake_minimum_required(VERSION 2.8)
find_package(OpenCV REQUIRED)
find_package(Caffe REQUIRED)
find_package(Boost REQUIRED)

set(CMAKE_CXX_FLAGS   "${CMAKE_CXX_FLAGS} -std=c++11 -Wall -g")
include_directories(/usr/local/include
	/usr/include)

link_directories(/usr/local/lib
	/usr/lib)

add_executable(classifier main.cpp Caffe_Detection.hpp Caffe_Detection.cpp)
target_link_libraries(classifier
	${OpenCV_LIBRARIES}
	${Caffe_LIBRARIES}
	${Boost_LIBRARIES})



