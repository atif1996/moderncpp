# packageName

[![Build&Test](https://github.com/OWNER/REPOSITORY/actions/workflows/build-test.yaml/badge.svg)](https://github.com/OWNER/REPOSITORY/actions/workflows/build-test.yaml)

Modern C++20 + CMake template

## Requirements

- A C++20 compiler. CI builds with GCC, Apple Clang and MSVC 2022.
- CMake 3.25+
- Conan 2

## Build and test

```sh
conan profile detect                      # once per machine
conan build . -s compiler.cppstd=20 --build=missing
```

`conan build` installs the dependencies, configures, builds and runs the tests. Add `-o "&:shared=True"`
for shared libraries and `-c user.project:werror=True` to treat warnings as errors, as CI does.

To drive CMake yourself, install the dependencies first and use the presets Conan generates:

```sh
conan install . -s compiler.cppstd=20 --build=missing
cmake --preset conan-release
cmake --build --preset conan-release
ctest --preset conan-release
```

## Use from another project

```sh
conan create . -s compiler.cppstd=20 --build=missing
```

builds the package, runs its tests, and builds `tests/consumer` against it. Another project then uses:

```cmake
find_package(packageName CONFIG REQUIRED)
target_link_libraries(app PRIVATE packageName::core)
```

## Layout

- `packageName/<library>`: one directory per library, with headers and sources together. Unit tests sit
  next to the code they test as `*.test.cpp`.
- `apps/`: executables that use the libraries.
- `tests/integration`: tests that use the libraries together through their public headers.
- `tests/consumer`: a separate project built against the installed package.

To add a library, create `packageName/<name>/CMakeLists.txt` that calls `packageName_add_library`, add the
directory to `packageName/CMakeLists.txt`, and add its name to `_libraries` in `conanfile.py`.
