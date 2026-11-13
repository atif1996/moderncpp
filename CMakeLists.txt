cmake_minimum_required(VERSION 3.25)

project(packageName
  VERSION 0.1.0
  DESCRIPTION "Modern C++20 + CMake template"
  LANGUAGES CXX)

include(GNUInstallDirs)
include(GenerateExportHeader)
include(CMakePackageConfigHelpers)
include(cmake/Warnings.cmake)
include(cmake/AddLibrary.cmake)

option(packageName_BUILD_TESTS "Build the unit and integration tests" ${PROJECT_IS_TOP_LEVEL})
option(packageName_BUILD_APPS "Build the applications under apps/" ${PROJECT_IS_TOP_LEVEL})
option(packageName_WARNINGS_AS_ERRORS "Treat compiler warnings as errors" OFF)
option(packageName_CLANG_TIDY "Run clang-tidy on the libraries" OFF)

if(PROJECT_IS_TOP_LEVEL)
  set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
  # Shared-library tests on Windows find the DLLs only when they sit next to the executables.
  set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/bin")
endif()

if(packageName_CLANG_TIDY)
  find_program(packageName_CLANG_TIDY_EXE NAMES clang-tidy REQUIRED)
endif()

if(packageName_BUILD_TESTS)
  enable_testing()
  find_package(Catch2 3 CONFIG REQUIRED)
  include(Catch)
endif()

add_subdirectory(packageName)

if(packageName_BUILD_APPS)
  add_subdirectory(apps/example)
endif()

if(packageName_BUILD_TESTS)
  add_subdirectory(tests)
endif()

install(EXPORT packageName-targets
  NAMESPACE packageName::
  DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/packageName")
configure_package_config_file(cmake/packageNameConfig.cmake.in "${PROJECT_BINARY_DIR}/packageNameConfig.cmake"
  INSTALL_DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/packageName")
write_basic_package_version_file("${PROJECT_BINARY_DIR}/packageNameConfigVersion.cmake"
  COMPATIBILITY SameMajorVersion)
install(FILES
    "${PROJECT_BINARY_DIR}/packageNameConfig.cmake"
    "${PROJECT_BINARY_DIR}/packageNameConfigVersion.cmake"
  DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/packageName")
