cmake_minimum_required(VERSION 2.8)

if(NOT DEFINED CEF_ROOT)
  message(FATAL_ERROR "Setting CEF_ROOT is required")
endif()

message(STATUS "CMAKE_VERSION = ${CMAKE_VERSION}")
message(STATUS "CMAKE_GENERATOR = ${CMAKE_GENERATOR}")

# Project Name and start working in project scope (some things just work until now, some just work after this command)
project(libcef_dll_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

# See https://bitbucket.org/chromiumembedded/cef/issues/1921/cmake-error-building-minimal-binary#comment-28471790
macro(SET_LIBRARY_TARGET_PROPERTIES target)
endmacro()

# Configure use of the sandbox.
option(USE_SANDBOX OFF)

if(USE_SANDBOX)
    # Definition required by CEF_sandbox.lib.
    add_definitions(-DPSAPI_VERSION=1)
    # Definition used by apps to test if the sandbox is enabled.
    add_definitions(-DCEF_USE_SANDBOX)
endif()

# Add the CEF binary distribution's cmake/ directory to the module path.
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CEF_ROOT}/cmake")
message(STATUS "MOUDLE PATH: ${CMAKE_MODULE_PATH}")

# Load the CEF configuration (executes FindCEF.cmake).
# find_package(CEF REQUIRED)

# Path to the include directory.
set(CEF_INCLUDE_PATH "${CEF_ROOT}")

# Path to the libcef_dll_wrapper target.
set(CEF_LIBCEF_DLL_WRAPPER_PATH "${CEF_ROOT}/libcef_dll")

include_directories(${CEF_INCLUDE_PATH})

# Include the libcef_dll_wrapper target (executes libcef_dll/CMakeLists.txt).
add_subdirectory(${CEF_LIBCEF_DLL_WRAPPER_PATH} libcef_dll_wrapper)
