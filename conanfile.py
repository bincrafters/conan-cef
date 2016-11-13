from conans import ConanFile, CMake, tools, ConfigureEnvironment
import os
import shutil


class CEFConan(ConanFile):
    name = "CEF"
    version = "3.2704.1434.gec3e9ed"
   # url = "https://github.com/memsharded/conan-protobuf.git"
    license = "BSD-3Clause"
    settings = "os", "compiler", "build_type", "arch"
    options = {"use_sandbox": [True, False]}
    default_options = "use_sandbox=False"
    generators = "cmake"
    exports = "CMakeLists.txt", "cmake/compile_flags_and_defs.cmake", "cmake/DownloadCEF.cmake", "cmake/platform_detection.cmake"

    def source(self):
        pass

    def build(self):
   #     args = ["-DCEF_ROOT={}".format(self.get_cef_distribution_name())]
    #    if self.options.shared:
   #         args += ["-DBUILD_SHARED_LIBS"]
        args = ["-DUSE_SANDBOX={}".format("ON" if self.options.use_sandbox else "OFF")]

        cmake = CMake(self.settings)
        self.run('cmake {} {} {}'.format(self.conanfile_directory, cmake.command_line, " ".join(args)))
        self.run("cmake --build . {}".format(cmake.build_config))

    def package(self):
        self.copy('*', dst='include', src='include')
        self.copy("*.lib", dst="lib", src="", keep_path=False)
        self.copy("*.a", dst="lib", src="", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["libcef_dll_wrapper"] # USING_CEF_SHARED
