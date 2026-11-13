cmake_minimum_required(VERSION 3.25)

project(packageName_consumer LANGUAGES CXX)

find_package(packageName CONFIG REQUIRED)

add_executable(consumer main.cpp)
target_link_libraries(consumer PRIVATE packageName::core)
