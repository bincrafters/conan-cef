from conans import ConanFile, CMake, tools, ConfigureEnvironment
import os
import shutil


class CEFConan(ConanFile):
    name = "CEF"
    version = "3.2704.1424.gc3f0a5b"
    branch = 2704 # Used instead of the version in case of build_from_source==True
    url = "https://github.com/inexor-game/conan-CEF.git"
    license = "BSD-3Clause"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "use_sandbox": [True, False],
        "debug_info_flag_vs": ["-Zi", "-Z7"],
        "build_from_source": [True, False]
    }
    default_options = '''use_sandbox=False
    debug_info_flag_vs=-Z7
    build_from_source=False'''
    generators = "cmake"
    exports = "CMakeLists.txt"

    def get_cef_distribution_name(self):
        platform = ""
        if self.settings.os == "Windows":
            platform = "windows"
        if self.settings.os == "Macos":
            platform = "macosx"
        if self.settings.os == "Linux":
            platform = "linux"
        if self.settings.arch == "x86":
            platform += "32"
        else:
            platform += "64"
        return "cef_binary_%s_%s" % (self.version, platform)

    def config(self):
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio" and self.settings.compiler.version != "14":
            self.options.remove("use_sandbox") # it requires to be built with that exact version for sandbox support

    def adapt_cmake_files(self, cmake_vars_file):
        if self.settings.compiler == "Visual Studio" and not (self.settings.compiler.runtime == "MT" or self.settings.compiler.runtime == "MTd"):
            tools.replace_in_file(cmake_vars_file, "/MT           # Multithreaded release runtime", "/MD           # Multithreaded release runtime")
            tools.replace_in_file(cmake_vars_file, "/MDd          # Multithreaded debug runtime", "/MDd          # Multithreaded debug runtime")
        tools.replace_in_file(cmake_vars_file, 'set(CEF_DEBUG_INFO_FLAG "/Zi"', 'set(CEF_DEBUG_INFO_FLAG "{}"'.format(self.options.debug_info_flag_vs))
        tools.replace_in_file(cmake_vars_file, 'set(CEF_DEBUG_INFO_FLAG "/Zi"', 'set(CEF_DEBUG_INFO_FLAG "{}"'.format(self.options.debug_info_flag_vs))

    def source(self):
        if self.options.build_from_source:
            tools.download("https://bitbucket.org/chromiumembedded/cef/raw/master/tools/automate/automate-git.py", "automate-git.py")
        else:
            cef_download_filename ="{}.tar.bz2".format(self.get_cef_distribution_name())
            self.output.info("Downloading CEF prebuilts from opensource.spotify.com")
            tools.download("http://opensource.spotify.com/cefbuilds/{}".format(cef_download_filename), cef_download_filename)
            tools.unzip(cef_download_filename)
            os.unlink(cef_download_filename)
            self.adapt_cmake_files("{}/cmake/cef_variables.cmake".format(self.get_cef_distribution_name()))

    def build(self):
        if self.options.build_from_source:
            self.output.warn("Building CEF from sources, this will take some time (~2-3 hours) and resources (8GB Ram 40GB Disk space)")
            linux_get_deps_cmd = '''apt-get install aptitude && aptitude -y update && DEBIAN_FRONTEND=noninteractive aptitude -y install bison build-essential cdbs curl devscripts dpkg-dev elfutils fakeroot flex g++ git-core git-svn gperf libapache2-mod-php5 libasound2-dev libav-tools libbrlapi-dev libbz2-dev libcairo2-dev libcap-dev libcups2-dev libcurl4-gnutls-dev libdrm-dev libelf-dev libexif-dev libffi-dev libgconf2-dev libgl1-mesa-dev libglib2.0-dev libglu1-mesa-dev libgnome-keyring-dev libgtk2.0-dev libkrb5-dev libnspr4-dev libnss3-dev libpam0g-dev libpci-dev libpulse-dev libsctp-dev libspeechd-dev libsqlite3-dev libssl-dev libudev-dev libwww-perl libxslt1-dev libxss-dev libxt-dev libxtst-dev mesa-common-dev openbox patch perl php5-cgi pkg-config python python-cherrypy3 python-crypto python-dev python-psutil python-numpy python-opencv python-openssl python-yaml rpm ruby subversion ttf-dejavu-core ttf-indic-fonts ttf-kochi-gothic ttf-kochi-mincho fonts-thai-tlwg wdiff wget zip'''
            linux_build_cmd = '''export CEF_USE_GN=1 && export GN_DEFINES="is_official_build=true use_sysroot=true use_allocator=none symbol_level=1" && export GYP_DEFINES="disable_nacl=1 use_sysroot=1 buildtype=Official use_allocator=none" && export CEF_ARCHIVE_FORMAT=tar.bz2'''
            self.run(linux_get_deps_cmd) # This will only work on debian based sys, but cef does not have further docs on other systems.
            self.run("{0} && python automate-git.py --download-dir={1} --minimal-distrib-only --build-target=cef --branch={2} {3}".format(linux_build_cmd, self.get_cef_distribution_name(), self.branch, "--x64-build" if self.settings.arch != "x86" else ""))
        args = ["-DCEF_ROOT={}".format(self.get_cef_distribution_name())]
        args += ["-DUSE_SANDBOX={}".format("ON" if self.options.use_sandbox else "OFF")]

        cmake = CMake(self.settings)
        cmake_str = 'cmake {} {} {}'.format(self.conanfile_directory, cmake.command_line, " ".join(args))
        self.output.warn(cmake_str)
        self.run(cmake_str)
        self.run("cmake --build . {}".format(cmake.build_config))

    def package(self):
        # Copy headers
        self.copy('*', dst='include/include', src='{}/include'.format(self.get_cef_distribution_name()))

        # Copy all stuff from the Debug/Release folders in the downloaded cef bundle:
        dis_folder = "{}/{}".format(self.get_cef_distribution_name(), self.settings.build_type)
        res_folder = "{}/Resources".format(self.get_cef_distribution_name())
        # resource files: taken from cmake/cef_variables (on macosx we would need to convert the COPY_MACOSX_RESOURCES() function)
        cef_resources = ["cef.pak", "cef_100_percent.pak", "cef_200_percent.pak", "cef_extensions.pak", "devtools_resources.pak", "icudtl.dat", "locales*"]
        for res in cef_resources:
            self.copy(res, dst="bin", src=res_folder, keep_path=True)

        if self.settings.os == "Linux":
            # CEF binaries: (Taken from cmake/cef_variables)
            self.copy("libcef.so", dst="lib", src=dis_folder, keep_path=False)
            self.copy("natives_blob.bin", dst="bin", src=dis_folder, keep_path=False)
            self.copy("snapshot_blob.bin", dst="bin", src=dis_folder, keep_path=False)
            if self.options.use_sandbox:
                self.copy("chrome-sandbox", dst="bin", src=dis_folder, keep_path=False)
            self.copy("*cef_dll_wrapper.a", dst="lib", keep_path=False)
        if self.settings.os == "Windows":
            # CEF binaries: (Taken from cmake/cef_variables)
            self.copy("*.dll", dst="bin", src=dis_folder, keep_path=False)
            self.copy("libcef.lib", dst="lib", src=dis_folder, keep_path=False)
            self.copy("natives_blob.bin", dst="bin", src=dis_folder, keep_path=False)
            self.copy("snapshot_blob.bin", dst="bin", src=dis_folder, keep_path=False)
            if self.options.use_sandbox:
                self.copy("cef_sandbox.lib", dst="lib", src=dis_folder, keep_path=False)
            self.copy("*cef_dll_wrapper.lib", dst="lib", keep_path=False) # libcef_dll_wrapper is somewhere else

    def package_info(self):
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ["libcef_dll_wrapper", "libcef"]
        else:
            self.cpp_info.libs = ["cef_dll_wrapper", "cef"]
            self.cpp_info.defines += ["_FILE_OFFSET_BITS=64"]
        
        if self.options.use_sandbox:
            if self.settings.os == "Windows":
                self.cpp_info.libs += ["cef_sandbox", "dbghelp", "psapi", "version", "winmm"]
            self.cpp_info.defines += ["USE_SANDBOX", "CEF_USE_SANDBOX", "PSAPI_VERSION=1"]
        if self.settings.os == "Windows":
            self.cpp_info.libs += ["glu32", "opengl32", "comctl32", "rpcrt4", "shlwapi", "ws2_32"]
