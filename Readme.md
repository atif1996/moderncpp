![Build&Test](https://github.com/atif1996/moderncpp/workflows/Build&Test/badge.svg)

Modern C++17/20 Cmake template
==============================

Directory layout
----------------
* /packageName : Directory name matches the package name.  
    * Sub directories correspond to libraries.  
    * Unit tests match their cpp, with the naming convention of *.test.cpp
    * Unit tests are registered with ctest
    * Headers and C++'s are together
* /apps: Contains executables generated using the packages
* /tests: Contains integration and end to end tests

Dependency Management
---------------------
Dependency management is managed through conan.  New dependancies can be added by editing conanfile.txt

Kicking off a build
-------------------
CMake uses out of source build directories.  In theory these are outside of the project, but 
can also be in a cmake-build-* directory inside of the source.  You kick off a build as follows
```bash
  mkdir cmake-build-debug
  cd cmake-build-debug
  conan install ..  # --build to build dependancies whose prebuild artifacts aren't available
  cmake ..          # Use -G Xcode flag for an Xcode project.  CLion seems to use the makefile 
  make all          # Build everyting
  make test         # test everything
  
```
