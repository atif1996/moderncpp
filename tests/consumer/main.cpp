#include <packageName/core/dummy.hpp>

#include <iostream>
#include <version>

// This project sets no C++ standard; the package's cxx_std_20 requirement must supply it.
#if !defined(__cpp_lib_concepts)
#error "consumer is not compiled as C++20: the package's cxx_std_20 requirement did not propagate"
#endif

int main() {
    if (packageName::dummy().empty()) {
        return 1;
    }
    std::cout << packageName::dummy() << '\n';
    return 0;
}
