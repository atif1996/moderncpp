![Build&Test](https://github.com/atif1996/moderncpp/workflows/Build&Test/badge.svg)

Modern C++20 CMake template
===========================

A starting point for a C++20 library project: target-based CMake, Conan 2 for dependencies, tests with
Catch2 v3, an installable CMake package, and CI on Linux, macOS and Windows in static and shared form.

Starting a project
------------------
Click **Use this template** on GitHub. On the new repository's first push, the `Template first use` workflow
renames the placeholder package after the repository (`my-project` becomes `my_project`), writes the
project's README, and removes the files only the template needs.

To do the same by hand in a copy of this repository:

```sh
python3 scripts/rename.py my_project --repo owner/my-project
```

What a project gets
-------------------
* `/packageName`: the directory name matches the package name, so headers are included as
  `<packageName/core/dummy.hpp>` both in the build tree and after installation.
    * Sub-directories are libraries. `packageName/core` builds the target `packageName::core`.
    * Headers and sources are together.
    * Unit tests sit next to the code they test, named `*.test.cpp`, and are registered with CTest.
* `/apps`: executables that use the libraries.
* `/tests`: tests that are not tied to one source file.
    * `tests/integration`: tests that use the libraries together through their public headers.
    * `tests/consumer`: a separate project that builds against the installed package with
      `find_package(packageName)`. `conan create` runs it as its package test.
* `/cmake`: `packageName_add_library`, the warning flags and the package config template.
* `.clang-format`, `.clang-tidy`, `.editorconfig`, and Dependabot updates for the workflow's actions.
* `Build&Test` workflow, which runs on pushes to `main`, pull requests, weekly, and on demand:
    * builds, tests and packages on Linux, macOS and Windows, static and shared, with warnings as errors
    * runs the tests under AddressSanitizer and UndefinedBehaviorSanitizer
    * checks formatting with clang-format and lints with clang-tidy

GitHub disables scheduled workflows in a public repository after 60 days without activity, and sends an
email first; re-enable the workflow from the Actions tab, or run it on demand.

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
for shared libraries, `-c user.project:werror=True` to treat warnings as errors, and
`-c user.project:clang_tidy=True` to run clang-tidy on the libraries.

To drive CMake yourself, install the dependencies first and use the presets Conan generates:

```sh
conan install . -s compiler.cppstd=20 --build=missing
cmake --preset conan-release
cmake --build --preset conan-release
ctest --preset conan-release
```

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

Adding a library
----------------
1. Create `packageName/<name>/CMakeLists.txt`:

   ```cmake
   packageName_add_library(<name>
     SOURCES thing.cpp
     HEADERS thing.hpp
     TESTS thing.test.cpp)
   ```

2. Add `add_subdirectory(<name>)` to `packageName/CMakeLists.txt`.
3. Add `"<name>"` to `_libraries` in `conanfile.py`.
4. Mark public functions and classes with the library's export macro, `PACKAGENAME_<NAME>_EXPORT` from
   `<packageName/<name>/export.hpp>`, which keeps shared-library builds working on Windows.

Maintaining the template
------------------------
The `Template check` workflow renames a checkout the way a new repository would be and then builds, tests,
packages and format-checks the result. The `Build&Test` workflow must not name the package, because a
repository's own token can delete workflow files but cannot push changes to them.
