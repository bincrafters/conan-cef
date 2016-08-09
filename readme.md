
# Libcef_dll_wrapper prebuilt project

For inexor we provide CEF and all its stuff in prebuilt form. So people don't spend compile time building another project.  
This project is there to help you prebuilt the libcef_dll_wrapper target.


Read `cef/tools/distrib/<your_OS>/README.redistrib.txt` on https://bitbucket.org/chromiumembedded/cef/


We need in the platform submodule:

* libcef_dll_wrapper.libs
  * renamed to cef_dll_wrapper_release.lib and cef_dll_wrapper_debug.lib on windows
    * we need 2 for windows for each arch
  * simply libcef_dll_wrapper.a on linux
* everything for cef see the README_redistrib.txt
  * note: the headers are not the same for different platforms! merge stuff (if thats working)

# Step by Step

cmake for your target into build folders
(if you need: adapt the CEF_VERSION entry before)
build
You find the libcef_dll_wrapper.lib somewhere nested in your build-folder
