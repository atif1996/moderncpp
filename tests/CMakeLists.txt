# Integration tests exercise the libraries together through their public headers. Unit tests live next to the
# code they test, as <name>.test.cpp. tests/consumer is a separate project, built against an installed package.
add_executable(packageName_integration_tests integration/greeting.test.cpp)
target_link_libraries(packageName_integration_tests PRIVATE packageName::core Catch2::Catch2WithMain)
packageName_target_warnings(packageName_integration_tests)
catch_discover_tests(packageName_integration_tests DISCOVERY_MODE PRE_TEST)
