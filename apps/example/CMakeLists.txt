add_executable(example main.cpp)
target_link_libraries(example PRIVATE packageName::core)
packageName_target_warnings(example)
