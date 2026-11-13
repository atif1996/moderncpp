![Build&Test](https://github.com/atif1996/moderncpp/workflows/Build&Test/badge.svg)

Modern C++20 CMake template
===========================

A starting point for a C++20 library project: target-based CMake, Conan 2 for dependencies, tests with
Catch2 v3, an installable CMake package, and CI on Linux, macOS and Windows in static and shared form.

Directory layout
----------------
* `/packageName`: the directory name matches the package name, so headers are included as
  `<packageName/core/dummy.hpp>` both in the build tree and after installation.
    * Sub-directories correspond to libraries. `packageName/core` builds the target `packageName::core`.
    * Headers and sources are together.
    * Unit tests sit next to the code they test, named `*.test.cpp`, and are registered with CTest.
* `/apps`: executables that use the libraries.
* `/tests`: tests that are not tied to one source file.
    * `tests/integration`: tests that use the libraries together through their public headers.
    * `tests/consumer`: a separate project that builds against the installed package with
      `find_package(packageName)`. `conan create` runs it as its package test.
* `/cmake`: the package config template and the warning flags.

Requirements
------------
* A C++20 compiler. CI builds with GCC, Apple Clang and MSVC 2022.
* CMake 3.25+
* Conan 2

Build and test
--------------
```sh
conan profile detect                      # once per machine
conan build . -s compiler.cppstd=20 --build=missing
```

`conan build` installs the dependencies, configures, builds and runs the tests. Add `-o "&:shared=True"`
for shared libraries and `-c user.packagename:werror=True` to treat warnings as errors, as CI does.

To drive CMake yourself, install the dependencies first and use the presets Conan generates:

```sh
conan install . -s compiler.cppstd=20 --build=missing
cmake --preset conan-release
cmake --build --preset conan-release
ctest --preset conan-release
```

Add `-DpackageName_CLANG_TIDY=ON` to the configure step to run clang-tidy on the libraries.

Package and consume
-------------------
```sh
conan create . -s compiler.cppstd=20 --build=missing
```

builds the package, runs its tests, and builds and runs `tests/consumer` against it. Another project uses
the package with:

```cmake
find_package(packageName CONFIG REQUIRED)
target_link_libraries(app PRIVATE packageName::core)
```

The same works without Conan after `cmake --install`, or with `add_subdirectory`. The libraries require
C++20 and pass that requirement to the targets that link them.

Starting a project from this template
-------------------------------------
1. Rename the `packageName` directory, and replace `packageName`, `packagename` and `PACKAGENAME` in the
   CMake files, `conanfile.py`, the sources and the workflow.
2. Add a library by copying `packageName/core` and listing it in `packageName/CMakeLists.txt`; add its
   component to `package_info()` in `conanfile.py`.
3. Mark public functions and classes with the library's export macro (`PACKAGENAME_CORE_EXPORT`), which
   keeps shared-library builds working on Windows.
