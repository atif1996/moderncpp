#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file

#include <catch2/catch.hpp>
#include <packageName/core/dummy.hpp>

TEST_CASE("dummy return a string", "[dummy]") {
    REQUIRE(dummy().size() > 0);
}

