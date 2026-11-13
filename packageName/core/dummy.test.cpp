#include <packageName/core/dummy.hpp>

#include <catch2/catch_test_macros.hpp>

TEST_CASE("dummy returns a string", "[dummy]") {
    REQUIRE_FALSE(packageName::dummy().empty());
}
