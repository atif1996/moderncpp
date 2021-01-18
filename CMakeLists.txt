cmake_minimum_required(VERSION 3.17)
project(packageName CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Conan setup
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

include(CTest)
enable_testing()
include(Catch)

#add_executable(main main.cpp)
#target_link_libraries(main ${CONAN_LIBS})

add_subdirectory(packageName)
add_subdirectory(apps/example)
