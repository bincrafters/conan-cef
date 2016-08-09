cmake_minimum_required(VERSION 2.8.12.1)

### Different Configuration Types (Debug release)

# Only generate Debug and Release configuration types.
set(CMAKE_CONFIGURATION_TYPES Debug Release)

# First choice is Debug
if(NOT DEFINED CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Debug CACHE INTERN "")
endif()


message(STATUS "CMAKE_VERSION = ${CMAKE_VERSION}")
message(STATUS "CMAKE_GENERATOR = ${CMAKE_GENERATOR}")

# Project Name and start working in project scope (some things just work until now, some just work after this command)
project(LibCEFDLL_WRAPPER)

# Use folders in the resulting project files.
set_property(GLOBAL PROPERTY OS_FOLDERS ON)


include(cmake/platform_detection.cmake)    # Get compiler/os/architecture variables
include(cmake/compile_flags_and_defs.cmake)# Set compile flags and compile specific definitions

# Configure use of the sandbox.
option(USE_SANDBOX OFF)

if(USE_SANDBOX)
    # Definition required by CEF_sandbox.lib.
    add_definitions(-DPSAPI_VERSION=1)
    # Definition used by apps to test if the sandbox is enabled.
    add_definitions(-DCEF_USE_SANDBOX)
endif()
    

#### Install paths ####

# Error if paths aren't set well
get_filename_component(MAINDIR "${CMAKE_SOURCE_DIR}" REALPATH)  # Main inexor folder
get_filename_component(BINDIR "${CMAKE_BINARY_DIR}" REALPATH)   # Where it generates the projects into
if(${MAINDIR} STREQUAL ${BINDIR})
    message(FATAL_ERROR "Keep your directories clean, don't generate the project-files in the main directory! ${MAINDIR} ${BINDIR}")
endif()

if(X64)
  set(PROJECT_ARCH "64")
else()
  set(PROJECT_ARCH "32")
endif()

if(OS_LINUX)
  set(CEF_PLATFORM "linux${PROJECT_ARCH}")
elseif(OS_MACOSX)
  set(CEF_PLATFORM "macosx${PROJECT_ARCH}")
elseif(OS_WINDOWS)
  set(CEF_PLATFORM "windows${PROJECT_ARCH}")
endif()

set(CEF_DIR "cef3${EXE_DIR}")
set(CEF_WRAPPER_DIR "${CEF_DIR}/libcef_dll")

# CEF Lib for Rendering HTML ingame
set(CEF_VERSION "3.2704.1434.gec3e9ed" CACHE STRING "http://opensource.spotify.com/cefbuilds/index.html The CEF version number.")
set(CEF_DOWNLOAD_DIR "${MAINDIR}/cef3")

include(cmake/DownloadCEF.cmake)
DownloadCEF("${CEF_PLATFORM}" "${CEF_VERSION}" "${CEF_DOWNLOAD_DIR}")

# Add the CEF binary distribution's cmake/ directory to the module path.
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CEF_ROOT}/cmake")

# Load the CEF configuration (executes FindCEF.cmake).
find_package(CEF REQUIRED)

# Include the libcef_dll_wrapper target (executes libcef_dll/CMakeLists.txt).
add_subdirectory(${CEF_LIBCEF_DLL_WRAPPER_PATH} libcef_dll_wrapper)
