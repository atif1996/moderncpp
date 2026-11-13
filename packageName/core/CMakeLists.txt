add_library(packageName_core)
add_library(packageName::core ALIAS packageName_core)

generate_export_header(packageName_core
  BASE_NAME packageName_core
  EXPORT_FILE_NAME "${PROJECT_BINARY_DIR}/packageName/core/export.hpp")

# Generated headers get their own file set: the build directory is usually inside the source directory, and
# one file set cannot have a base directory nested in another.
target_sources(packageName_core
  PRIVATE
    dummy.cpp
  PUBLIC
    FILE_SET HEADERS
    BASE_DIRS "${PROJECT_SOURCE_DIR}"
    FILES
      dummy.hpp
  PUBLIC
    FILE_SET generated_headers
    TYPE HEADERS
    BASE_DIRS "${PROJECT_BINARY_DIR}"
    FILES
      "${PROJECT_BINARY_DIR}/packageName/core/export.hpp")

target_compile_features(packageName_core PUBLIC cxx_std_20)

if(NOT BUILD_SHARED_LIBS)
  target_compile_definitions(packageName_core PUBLIC PACKAGENAME_CORE_STATIC_DEFINE)
endif()

set_target_properties(packageName_core PROPERTIES
  EXPORT_NAME core
  CXX_EXTENSIONS OFF
  CXX_VISIBILITY_PRESET hidden
  VISIBILITY_INLINES_HIDDEN ON
  VERSION ${PROJECT_VERSION}
  SOVERSION ${PROJECT_VERSION_MAJOR})

packageName_target_warnings(packageName_core)

if(packageName_CLANG_TIDY)
  set_target_properties(packageName_core PROPERTIES CXX_CLANG_TIDY "${packageName_CLANG_TIDY_EXE}")
endif()

install(TARGETS packageName_core EXPORT packageName-targets FILE_SET HEADERS FILE_SET generated_headers)

if(packageName_BUILD_TESTS)
  add_executable(packageName_core_tests dummy.test.cpp)
  target_link_libraries(packageName_core_tests PRIVATE packageName::core Catch2::Catch2WithMain)
  packageName_target_warnings(packageName_core_tests)
  catch_discover_tests(packageName_core_tests DISCOVERY_MODE PRE_TEST)
endif()
