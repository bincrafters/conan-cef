[![Download](https://api.bintray.com/packages/bincrafters/public-conan/cef%3Abincrafters/images/download.svg) ](https://bintray.com/bincrafters/public-conan/cef%3Abincrafters/_latestVersion)
[![Build Status Travis](https://travis-ci.com/bincrafters/conan-cef.svg?branch=testing%2F3.3239.1709.g093cae4)](https://travis-ci.com/bincrafters/conan-cef)
[![Build Status AppVeyor](https://ci.appveyor.com/api/projects/status/github/bincrafters/conan-cef?branch=testing%2F3.3239.1709.g093cae4&svg=true)](https://ci.appveyor.com/project/bincrafters/conan-cef)

## Conan package recipe for [*cef*](https://bitbucket.org/chromiumembedded/cef)

The Chromium Embedded Framework (CEF) is an open source framework for embedding a web browser engine which is based on the Chromium core

The packages generated with this **conanfile** can be found on [Bintray](https://bintray.com/bincrafters/public-conan/cef%3Abincrafters).


## Issues

If you wish to report an issue or make a request for a Bincrafters package, please do so here:

[Bincrafters Community Issues](https://github.com/bincrafters/community/issues)


## For Users

### Basic setup

    $ conan install cef/3.3239.1709.g093cae4@bincrafters/testing

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    cef/3.3239.1709.g093cae4@bincrafters/testing

    [generators]
    cmake

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.


## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create . bincrafters/testing


### Available Options
| Option        | Default | Possible Values  |
| ------------- |:----------------- |:------------:|
| use_sandbox      | False |  [True, False] |
| debug_info_flag_vs      | -Z7 |  ['-Zi', '-Z7'] |


## Add Remote

    $ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"


## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which can be used to build and package cef.
It does *not* in any way apply or is related to the actual software being packaged.

[MIT](https://github.com/bincrafters/conan-cef/blob/testing/3.3239.1709.g093cae4/LICENSE.md)
