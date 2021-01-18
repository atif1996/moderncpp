#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file

#include <catch2/catch.hpp>
#include <riot/core/dummy.hpp>

TEST_CASE("dummy return a string", "[dummy]") {
    REQUIRE(dummy().size() > 0);
    REQUIRE(dummy().size() < 0);
//    REQUIRE( Factorial(2) == 2 );
//    REQUIRE( Factorial(3) == 6 );
//    REQUIRE( Factorial(10) == 3628800 );
}

//std::string dummy() {
//    return "hello world";
//}
