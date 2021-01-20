cmake_minimum_required(VERSION 3.17)

add_executable(example)
target_sources(example
        PRIVATE main.cpp
        )
target_link_libraries(example core)

