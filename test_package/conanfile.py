from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "stable")
username = os.getenv("CONAN_USERNAME", "inexorgame")
reference = os.getenv("CONAN_REFERENCE", "CEF/3.2704.1424.gc3f0a5b")

class ProtobufTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "{}@{}/{}".format(reference, username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        self.run('cmake %s  -DNO_BROWSER_WORKING_TEST=1 %s' % (self.source_folder, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)
    #    if self.settings.os == "Macos":
    #        self.run("cd bin; for LINK_DESTINATION in $(otool -L client | grep libproto | cut -f 1 -d' '); do install_name_tool -change \"$LINK_DESTINATION\" \"@executable_path/$(basename $LINK_DESTINATION)\" client; done")

    def imports(self):
        self.copy("*", "bin", "bin")

    def test(self):
        self.run(os.path.join(".", "bin", "cefsimple"))
