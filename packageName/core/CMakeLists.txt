project(core CXX)

add_library(${PROJECT_NAME})
target_sources(${PROJECT_NAME}
        PRIVATE
        dummy.cpp
        PUBLIC dummy.hpp
        )
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_SOURCE_DIR})
#target_link_libraries(${PROJECT_NAME} PRIVATE CONAN_PKG::catch2)


add_executable(${PROJECT_NAME}UnitTests
        dummy.test.cpp)
target_link_libraries(${PROJECT_NAME}UnitTests PRIVATE CONAN_PKG::catch2 ${PROJECT_NAME})
catch_discover_tests(${PROJECT_NAME}UnitTests)

include(CPack)