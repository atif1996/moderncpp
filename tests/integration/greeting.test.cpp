#include <packageName/core/dummy.hpp>

#include <catch2/catch_test_macros.hpp>

#include <sstream>

TEST_CASE("the library's output can be composed by a caller", "[integration]") {
    std::ostringstream out;
    out << "printing the thing: " << packageName::dummy();
    REQUIRE(out.str() == "printing the thing: hello hello hello");
}
