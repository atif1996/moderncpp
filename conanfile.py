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
    exports_sources = (
        "CMakeLists.txt", ".clang-tidy", "cmake/*", "packageName/*", "apps/*", "tests/*", "!tests/consumer/*")
    test_package_folder = "tests/consumer"
    # One entry per directory under packageName/ that calls packageName_add_library.
    _libraries = ("core",)

    def set_version(self):
        cmakelists = load(self, os.path.join(self.recipe_folder, "CMakeLists.txt"))
        self.version = re.search(r"project\(\s*\w+\s+VERSION\s+(\S+)", cmakelists).group(1)

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
        # user.project:werror and user.project:clang_tidy are this project's own switches, named without the
        # package so the CI workflow needs no edit when the package is renamed.
        tc.cache_variables["packageName_WARNINGS_AS_ERRORS"] = self.conf.get(
            "user.project:werror", default=False, check_type=bool)
        tc.cache_variables["packageName_CLANG_TIDY"] = self.conf.get(
            "user.project:clang_tidy", default=False, check_type=bool)
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
        for library in self._libraries:
            component = self.cpp_info.components[library]
            component.set_property("cmake_target_name", f"packageName::{library}")
            component.libs = [f"packageName_{library}"]
            if not self.options.shared:
                component.defines = [f"PACKAGENAME_{library.upper()}_STATIC_DEFINE"]
