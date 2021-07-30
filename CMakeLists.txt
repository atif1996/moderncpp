cmake_minimum_required(VERSION 3.21)
project(packageName CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(cmake/conan.cmake)
conan_cmake_run(CONANFILE conanfile.txt  # or relative build/conanfile.txt
        BASIC_SETUP CMAKE_TARGETS)

if (CMAKE_GENERATOR STREQUAL "Unix Makefiles")
	set(CMAKE_EXPORT_COMPILE_COMMANDS ON)  # Enables cppcheck and clang-tidy
endif()


include(CTest)
enable_testing()
include(Catch)

add_subdirectory(packageName)
add_subdirectory(apps/example)
