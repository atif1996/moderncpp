# packageName_add_library(<name> SOURCES <files> HEADERS <files> [TESTS <files>])
#
# Adds the library in packageName/<name> as the target packageName::<name>, with an export header at
# <packageName/<name>/export.hpp>, C++20 required of its consumers, and install rules. When tests are
# enabled, TESTS are built into one executable and registered with CTest. Paths are relative to the calling
# directory. Link other libraries afterwards with target_link_libraries(packageName_<name> ...).
function(packageName_add_library name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "" "" "SOURCES;HEADERS;TESTS")
  set(target packageName_${name})
  string(TOUPPER ${target} macro_prefix)
  set(export_header "${PROJECT_BINARY_DIR}/packageName/${name}/export.hpp")

  add_library(${target})
  add_library(packageName::${name} ALIAS ${target})
  generate_export_header(${target} BASE_NAME ${target} EXPORT_FILE_NAME "${export_header}")

  # Generated headers get their own file set: the build directory is usually inside the source directory,
  # and one file set cannot have a base directory nested in another.
  target_sources(${target}
    PRIVATE
      ${arg_SOURCES}
    PUBLIC
      FILE_SET HEADERS
      BASE_DIRS "${PROJECT_SOURCE_DIR}"
      FILES ${arg_HEADERS}
    PUBLIC
      FILE_SET generated_headers
      TYPE HEADERS
      BASE_DIRS "${PROJECT_BINARY_DIR}"
      FILES "${export_header}")

  target_compile_features(${target} PUBLIC cxx_std_20)
  if(NOT BUILD_SHARED_LIBS)
    target_compile_definitions(${target} PUBLIC ${macro_prefix}_STATIC_DEFINE)
  endif()
  set_target_properties(${target} PROPERTIES
    EXPORT_NAME ${name}
    CXX_EXTENSIONS OFF
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN ON
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR})
  packageName_target_warnings(${target})
  if(packageName_CLANG_TIDY)
    set_target_properties(${target} PROPERTIES CXX_CLANG_TIDY "${packageName_CLANG_TIDY_EXE}")
  endif()

  install(TARGETS ${target} EXPORT packageName-targets FILE_SET HEADERS FILE_SET generated_headers)

  if(packageName_BUILD_TESTS AND arg_TESTS)
    add_executable(${target}_tests ${arg_TESTS})
    target_link_libraries(${target}_tests PRIVATE packageName::${name} Catch2::Catch2WithMain)
    packageName_target_warnings(${target}_tests)
    catch_discover_tests(${target}_tests DISCOVERY_MODE PRE_TEST)
  endif()
endfunction()
