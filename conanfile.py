import os
import re

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import load, rmdir


class PackageNameConan(ConanFile):
    name = "packagename"
    description = "Modern C++20 + CMake template"
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    exports_sources = "CMakeLists.txt", "cmake/*", "packageName/*", "apps/*", "tests/*", "!tests/consumer/*"
    test_package_folder = "tests/consumer"

    def set_version(self):
        cmakelists = load(self, os.path.join(self.recipe_folder, "CMakeLists.txt"))
        self.version = re.search(r"project\(packageName\s+VERSION\s+(\S+)", cmakelists).group(1)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def build_requirements(self):
        self.test_requires("catch2/3.16.1")

    def validate(self):
        check_min_cppstd(self, 20)

    def _skip_tests(self):
        return self.conf.get("tools.build:skip_test", default=False, check_type=bool)

    def generate(self):
        CMakeDeps(self).generate()
        tc = CMakeToolchain(self)
        tc.cache_variables["packageName_BUILD_TESTS"] = not self._skip_tests()
        tc.cache_variables["packageName_WARNINGS_AS_ERRORS"] = self.conf.get(
            "user.packagename:werror", default=False, check_type=bool)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        if not self._skip_tests():
            cmake.test()

    def package(self):
        CMake(self).install()
        # Consumers get Conan-generated config files; the ones CMake installs would shadow them.
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "packageName")
        core = self.cpp_info.components["core"]
        core.set_property("cmake_target_name", "packageName::core")
        core.libs = ["packageName_core"]
        if not self.options.shared:
            core.defines = ["PACKAGENAME_CORE_STATIC_DEFINE"]
