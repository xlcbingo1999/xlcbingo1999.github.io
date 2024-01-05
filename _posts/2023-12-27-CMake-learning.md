---
layout: post
title: CMake和Makefile相关学习
date: 2023-12-27 17:39:00
description: CMake和Makefile相关学习
tags: 技术杂记
categories: 技术杂记
featured: false
---

## CMake

### CMake 通常的 build 和编译位置

- 参考文献：[https://blog.csdn.net/shaoyou223/article/details/84764633](https://blog.csdn.net/shaoyou223/article/details/84764633)

```bash
# 方案1: 创建
mkdir build
cd build
cmake ..
make
```

```bash
# 方案2: 直接在主目录下进行
cmake -S . -B build
cmake --build
```

### Ubuntu 安装 CMake

- 参考文献：[https://askubuntu.com/questions/355565/how-do-i-install-the-latest-version-of-cmake-from-the-command-line](https://askubuntu.com/questions/355565/how-do-i-install-the-latest-version-of-cmake-from-the-command-line)
- 需要安装新版的 CMake 的时候就需要用这个文章里提到的方法

### CMakelists 的编写规则

- 号称是全网最全的规则：[https://zhuanlan.zhihu.com/p/534439206](https://zhuanlan.zhihu.com/p/534439206)

### FetchContent 依赖库

- 参考文献：[https://juejin.cn/post/7102762548423819272](https://juejin.cn/post/7102762548423819272)

```cpp
# FetchContent 模块用于获取外部依赖库, 在构建生成文件的过程中被调用
include(FetchContent)
# FetchContent_Declare 描述如何下载依赖库
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG        v2.6.2
    GIT_SHALLOW    TRUE
)
# FetchContent_MakeAvaliable 下载依赖库, 并使其可用
FetchContent_MakeAvailable(pybind11)
```

### CMake 的多版本共存

- 请不要直接删除 cmake，可能会导致一些文件被删除
- 多版本共存 CMake 参考文献：[https://zhuanlan.zhihu.com/p/442561052](https://zhuanlan.zhihu.com/p/442561052)

### CMakePresets: 简化 CMake 项目初始化繁杂步骤

- 参考文献：[https://cloud.tencent.com/developer/article/2348379](https://cloud.tencent.com/developer/article/2348379)
- 针对不同平台的 CMake 指令主流配置方案

  - 缺点：命令非常长，配置可能不同开发机器上都不一样，对工程在不同设备上编译带来很大的挑战，非常容易编译出错。而且在版本迭代过程中，工程的配置是不断在更新的，很容易忘记去修改 README 或者项目文档导致一些历史的编译脚本缺少一些关键指令丢失内容，这不符合 GitOps 思想。

| 参数                                                                                                    | Win           | Linux          | macOS | iOS   | Android |  |
| ------------------------------------------------------------------------------------------------------- | ------------- | -------------- | ----- | ----- | ------- | - |
| -G [用于指定生成器（Generator），即指定生成的项目文件（例如 Makefile、Visual Studio 项目文件等）的类型] | Visual Studio | Unix Makefiles | Xcode | Xcode |         |  |
| -A [ 用于指定目标平台的体系结构（Architecture）]                                                        | Win32/x64     |                |       |       |         |  |
| -DCMAKE_OSX_ARCHITECTURES [用于定义 CMake 变量]                                                         |               |                |       |       |         |  |
| -DTOOLSETS                                                                                              |               |                |       |       |         |  |
| -DCMAKE_SYSTEM_NAME                                                                                     |               |                |       |       |         |  |
|                                                                                                         |               |                |       |       |         |  |

- CMakePreset 的动机

  - 虽然不同的 IDE 或代码编辑器工具有提供一些自己的 CMake 初始化配置能力（如 Visual Studio Code 可通过 .vscode/settings.json 来配置一些默认值）但这都不是通用方案。每个人使用的开发工具都各要求。特别是开源项目，如果没有提供一套全平台对各类工具都支持的配置文件，这会让开发者在工程配置上就被劝退。所以我们期望对项目工程化改造的目标不仅仅是解决上面的痛苦问题，更期望能让开发人员在接手项目时不需要在编译工具链、工程配置上花费太多的心思，让主流的开发工具打开工程开箱即用。
  - 为了实现这个目标，CMake 从 3.19 版本就开始支持了 CMakePresets.json 配置。如果你的版本还低于 3.19 请尽快升级来体验下 C/C++ 生态工具链的魅力。
- CMakePreset 的几个阶段

  - configure
  - build
  - test 【可选】
  - package 【可选】
- 常用的指令

  - `cmake --list-presets` ： 查看当前支持的配置
  - `cmake --preset=ios-release-arm64`：configure
  - `cmake --build --preset=ios-release-arm64`：build 阶段
- 一个完整的 Preset 的例子

```bash
{
  "version": 3,
  "cmakeMinimumRequired": {
    "major": 3,
    "minor": 19,
    "patch": 0
  },
  "configurePresets": [ # configure阶段的配置
    {
      "name": "macos",
      "hidden": true,
      "condition": {
        "type": "equals",
        "lhs": "${hostSystemName}",
        "rhs": "Darwin"
      },
      "generator": "Xcode",
      "warnings": {"dev": true, "deprecated": true},
      "cacheVariables": {
        "BUILD_TESTING": "OFF"
      }
    },
    {
      "name": "darwin-debug",
      "inherits": "macos",
      "displayName": "Darwin 10.14+ (Debug)",
      "description": "NetEase MSS C wrapper for macOS - Debug Configuration",
      "binaryDir": "${sourceDir}/build",
      "cacheVariables": {
        "BUILD_TESTING": "ON",
        "CMAKE_BUILD_TYPE": "Debug",
        "CMAKE_INSTALL_PREFIX": "${sourceDir}/darwin-debug"
      }
    },
    {
      "name": "darwin-release-arm64",
      "inherits": "macos",
      "displayName": "Darwin arm64 10.14+ (Release)",
      "description": "NetEase MSS C wrapper for macOS arm64 - Release Configuration",
      "binaryDir": "${sourceDir}/build-darwin-arm64-realese",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_OSX_ARCHITECTURES": "arm64",
        "CONAN_PROFILE_BUILD": "${sourceDir}/.profiles/darwin-x86_64",
        "CONAN_PROFILE_HOST": "${sourceDir}/.profiles/darwin-arm64",
        "CMAKE_INSTALL_PREFIX": "${sourceDir}/darwin-release-arm64"
      }
    },
    {
      "name": "darwin-release-x86_64",
      "inherits": "macos",
      "displayName": "Darwin x86_64 10.14+ (Release)",
      "description": "NetEase MSS C wrapper for macOS x86_64 - Release Configuration",
      "binaryDir": "${sourceDir}/build-darwin-x86_64-realese",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CONAN_PROFILE_BUILD": "${sourceDir}/.profiles/darwin-x86_64",
        "CONAN_PROFILE_HOST": "${sourceDir}/.profiles/darwin-x86_64",
        "CMAKE_INSTALL_PREFIX": "${sourceDir}/darwin-release-x86_64"
      }
    },
    {
      "name": "ios-release-arm64",
      "inherits": "macos",
      "displayName": "iOS arm64 9.0+ (Release)",
      "description": "NetEase MSS C wrapper for iOS arm64 - Release Configuration",
      "binaryDir": "${sourceDir}/build-ios-arm64-release",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_SYSTEM_NAME": "iOS",
        "CMAKE_OSX_DEPLOYMENT_TARGET": "9.0",
        "CMAKE_OSX_ARCHITECTURES": "arm64",
        "CMAKE_OSX_SYSROOT": "iphoneos",
        "CONAN_PROFILE_BUILD": "${sourceDir}/.profiles/darwin-x86_64",
        "CONAN_PROFILE_HOST": "${sourceDir}/.profiles/ios-arm64-iphoneos",
        "CMAKE_INSTALL_PREFIX": "${sourceDir}/ios-release-arm64"
      }
    },
    {
      "name": "ios-release-armv7",
      "inherits": "macos",
      "displayName": "iOS armv7 9.0+ (Release)",
      "description": "NetEase MSS C wrapper for iOS armv7 - Release Configuration",
      "binaryDir": "${sourceDir}/build-ios-armv7-release",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_SYSTEM_NAME": "iOS",
        "CMAKE_OSX_DEPLOYMENT_TARGET": "9.0",
        "CMAKE_OSX_ARCHITECTURES": "armv7",
        "CMAKE_OSX_SYSROOT": "iphoneos",
        "CONAN_PROFILE_BUILD": "${sourceDir}/.profiles/darwin-x86_64",
        "CONAN_PROFILE_HOST": "${sourceDir}/.profiles/ios-armv7-iphoneos",
        "CMAKE_INSTALL_PREFIX": "${sourceDir}/ios-release-armv7"
      }
    },
    {
      "name": "ios-release-x86_64",
      "inherits": "macos",
      "displayName": "iOS x86_64 9.0+ (Release)",
      "description": "NetEase MSS C wrapper for iOS x86_64 - Release Configuration",
      "binaryDir": "${sourceDir}/build-ios-x86_64-release",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_SYSTEM_NAME": "iOS",
        "CMAKE_OSX_DEPLOYMENT_TARGET": "9.0",
        "CMAKE_OSX_ARCHITECTURES": "x86_64",
        "CMAKE_OSX_SYSROOT": "iphonesimulator",
        "CONAN_PROFILE_BUILD": "${sourceDir}/.profiles/darwin-x86_64",
        "CONAN_PROFILE_HOST": "${sourceDir}/.profiles/ios-x86_64-iphonesimulator",
        "CMAKE_INSTALL_PREFIX": "${sourceDir}/ios-release-x86_64"
      }
    },
    {
      "name": "macos-android",
      "hidden": true,
      "condition": {
        "type": "equals",
        "lhs": "${hostSystemName}",
        "rhs": "Darwin"
      },
      "warnings": {"dev": true, "deprecated": true},
      "cacheVariables": {
        "BUILD_TESTING": "OFF"
      }
    },
    {
      "name": "android-release-x86_64",
      "inherits": "macos-android",
      "displayName": "Android x86_64 abi21 (Release)",
      "description": "NetEase MSS C wrapper for Android x86_64 - Release Configuration",
      "binaryDir": "${sourceDir}/build-android-x86_64-release",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_SYSTEM_NAME": "Android",
        "CMAKE_SYSTEM_VERSION": "21",
        "CMAKE_ANDROID_STL_TYPE": "c++_static",
        "CMAKE_ANDROID_ARCH_ABI": "x86_64",
        "CMAKE_ANDROID_NDK": "$env{HOME}/Library/Android/sdk/ndk/21.4.7075529",
        "CONAN_PROFILE_BUILD": "${sourceDir}/.profiles/darwin-x86_64",
        "CONAN_PROFILE_HOST": "${sourceDir}/.profiles/android-x86_64-abi21",
        "CMAKE_INSTALL_PREFIX": "${sourceDir}/android-release-x86_64"
      }
    },
    {
      "name": "android-release-x86",
      "inherits": "macos-android",
      "displayName": "Android x86 abi21 (Release)",
      "description": "NetEase MSS C wrapper for Android x86 - Release Configuration",
      "binaryDir": "${sourceDir}/build-android-x86-release",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_SYSTEM_NAME": "Android",
        "CMAKE_SYSTEM_VERSION": "21",
        "CMAKE_ANDROID_STL_TYPE": "c++_static",
        "CMAKE_ANDROID_ARCH_ABI": "x86",
        "CMAKE_ANDROID_NDK": "$env{HOME}/Library/Android/sdk/ndk/21.4.7075529",
        "CONAN_PROFILE_BUILD": "${sourceDir}/.profiles/darwin-x86_64",
        "CONAN_PROFILE_HOST": "${sourceDir}/.profiles/android-x86-abi21",
        "CMAKE_INSTALL_PREFIX": "${sourceDir}/android-release-x86"
      }
    },
    {
      "name": "android-release-armeabi-v7a",
      "inherits": "macos-android",
      "displayName": "Android armeabi-v7a abi21 (Release)",
      "description": "NetEase MSS C wrapper for Android armeabi-v7a - Release Configuration",
      "binaryDir": "${sourceDir}/build-android-armeabi-v7a-release",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_SYSTEM_NAME": "Android",
        "CMAKE_SYSTEM_VERSION": "21",
        "CMAKE_ANDROID_STL_TYPE": "c++_static",
        "CMAKE_ANDROID_ARCH_ABI": "armeabi-v7a",
        "CMAKE_ANDROID_NDK": "$env{HOME}/Library/Android/sdk/ndk/21.4.7075529",
        "CONAN_PROFILE_BUILD": "${sourceDir}/.profiles/darwin-x86_64",
        "CONAN_PROFILE_HOST": "${sourceDir}/.profiles/android-armeabi-v7a-abi21",
        "CMAKE_INSTALL_PREFIX": "${sourceDir}/android-release-armeabi-v7a"
      }
    },
    {
      "name": "android-release-arm64-v8a",
      "inherits": "macos-android",
      "displayName": "Android arm64-v8a abi21 (Release)",
      "description": "NetEase MSS C wrapper for Android arm64-v8a - Release Configuration",
      "binaryDir": "${sourceDir}/build-android-arm64-v8a-release",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_SYSTEM_NAME": "Android",
        "CMAKE_SYSTEM_VERSION": "21",
        "CMAKE_ANDROID_STL_TYPE": "c++_static",
        "CMAKE_ANDROID_ARCH_ABI": "arm64-v8a",
        "CMAKE_ANDROID_NDK": "$env{HOME}/Library/Android/sdk/ndk/21.4.7075529",
        "CONAN_PROFILE_BUILD": "${sourceDir}/.profiles/darwin-x86_64",
        "CONAN_PROFILE_HOST": "${sourceDir}/.profiles/android-arm64-v8a-abi21",
        "CMAKE_INSTALL_PREFIX": "${sourceDir}/android-release-arm64-v8a"
      }
    },
    {
      "name": "windows",
      "hidden": true,
      "condition": {
        "type": "equals",
        "lhs": "${hostSystemName}",
        "rhs": "Windows"
      },
      "generator": "Visual Studio 15 2017",
      "warnings": {"dev": true, "deprecated": true},
      "cacheVariables": {
        "CMAKE_INSTALL_PREFIX": "${sourceDir}/exports",
        "BUILD_TESTING": "OFF"
      }
    },
    {
      "name": "windows-debug",
      "inherits": "windows",
      "displayName": "Windows x64 (Debug)",
      "description": "NetEase MSS C wrapper for Windows - Debug Configuration",
      "binaryDir": "${sourceDir}/build",
      "architecture": {
        "value": "x64",
        "strategy": "set"
      },
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "CMAKE_DEBUG_POSTFIX": "d"
      }
    },
    {
      "name": "win32-release-x64",
      "inherits": "windows",
      "displayName": "Windows x64 (Release)",
      "description": "NetEase MSS C wrapper for Windows - Release Configuration",
      "binaryDir": "${sourceDir}/build-win32-x64",
      "architecture": {
        "value": "x64",
        "strategy": "set"
      },
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_INSTALL_PREFIX": "${sourceDir}/win32-release-x64"
      }
    },
    {
      "name": "win32-release-ia32",
      "inherits": "windows",
      "displayName": "Windows ia32 (Release)",
      "description": "NetEase MSS C wrapper for Windows - Release Configuration",
      "binaryDir": "${sourceDir}/build-win32-ia32",
      "architecture": {
        "value": "Win32",
        "strategy": "set"
      },
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_INSTALL_PREFIX": "${sourceDir}/win32-release-ia32"
      }
    }
  ],
  "buildPresets": [ # build阶段的配置
    {
      "name": "darwin-debug",
      "configurePreset": "darwin-debug", # 依赖的configure阶段
      "displayName": "Darwin Local Compilation (Debug)",
      "description": "NetEase MSS C wrapper for macOS - Debug Configuration",
      "configuration": "Debug"
    },
    {
      "name": "darwin-release-x86_64",
      "configurePreset": "darwin-release-x86_64",
      "displayName": "Darwin x86_64 Local Compilation (Release)",
      "description": "NetEase MSS C wrapper for macOS x86_64 - Release Configuration",
      "configuration": "Release",
      "targets": ["install"]
    },
    {
      "name": "darwin-release-arm64",
      "configurePreset": "darwin-release-arm64",
      "displayName": "Darwin x86_64 Local Compilation (Release)",
      "description": "NetEase MSS C wrapper for macOS arm64 - Release Configuration",
      "configuration": "Release",
      "targets": ["install"]
    },
    {
      "name": "ios-release-arm64",
      "configurePreset": "ios-release-arm64",
      "displayName": "iOS arm64 Local Compilation (Release)",
      "description": "NetEase MSS C wrapper for iOS arm64 - Release Configuration",
      "configuration": "Release",
      "targets": ["install"]
    },
    {
      "name": "ios-release-armv7",
      "configurePreset": "ios-release-armv7",
      "displayName": "iOS armv7 Local Compilation (Release)",
      "description": "NetEase MSS C wrapper for iOS armv7 - Release Configuration",
      "configuration": "Release",
      "targets": ["install"]
    },
    {
      "name": "ios-release-x86_64",
      "configurePreset": "ios-release-x86_64",
      "displayName": "iOS x86_64 Local Compilation (Release)",
      "description": "NetEase MSS C wrapper for iOS x86_64 - Release Configuration",
      "configuration": "Release",
      "targets": ["install"]
    },
    {
      "name": "android-release-x86_64",
      "configurePreset": "android-release-x86_64",
      "displayName": "Android x86_64 Local Compilation (Release)",
      "description": "NetEase MSS C wrapper for Android x86_64 - Release Configuration",
      "configuration": "Release",
      "targets": ["install"]
    },
    {
      "name": "android-release-x86_64-strip",
      "configurePreset": "android-release-x86_64",
      "displayName": "Android x86_64 Local Compilation (Release)",
      "description": "NetEase MSS C wrapper for Android x86_64 - Release Configuration",
      "configuration": "Release",
      "targets": ["install/strip"]
    },
    {
      "name": "android-release-x86",
      "configurePreset": "android-release-x86",
      "displayName": "Android x86 Local Compilation (Release)",
      "description": "NetEase MSS C wrapper for Android x86 - Release Configuration",
      "configuration": "Release",
      "targets": ["install"]
    },
    {
      "name": "android-release-x86-strip",
      "configurePreset": "android-release-x86",
      "displayName": "Android x86 Local Compilation (Release)",
      "description": "NetEase MSS C wrapper for Android x86 - Release Configuration",
      "configuration": "Release",
      "targets": ["install/strip"]
    },
    {
      "name": "android-release-armeabi-v7a",
      "configurePreset": "android-release-armeabi-v7a",
      "displayName": "Android armeabi-v7a Local Compilation (Release)",
      "description": "NetEase MSS C wrapper for Android armeabi-v7a - Release Configuration",
      "configuration": "Release",
      "targets": ["install"]
    },
    {
      "name": "android-release-armeabi-v7a-strip",
      "configurePreset": "android-release-armeabi-v7a",
      "displayName": "Android armeabi-v7a Local Compilation (Release)",
      "description": "NetEase MSS C wrapper for Android armeabi-v7a - Release Configuration",
      "configuration": "Release",
      "targets": ["install/strip"]
    },
    {
      "name": "android-release-arm64-v8a",
      "configurePreset": "android-release-arm64-v8a",
      "displayName": "Android arm64-v8a Local Compilation (Release)",
      "description": "NetEase MSS C wrapper for Android arm64-v8a - Release Configuration",
      "configuration": "Release",
      "targets": ["install"]
    },
    {
      "name": "windows-debug",
      "configurePreset": "windows-debug",
      "displayName": "Windows Local Compilation (Debug)",
      "description": "NetEase MSS C wrapper for Windows - Debug Configuration",
      "configuration": "Debug"
    },
    {
      "name": "win32-release-x64",
      "configurePreset": "win32-release-x64",
      "displayName": "Windows x64 Local Compilation (Release)",
      "description": "NetEase MSS C wrapper for Windows x64 - Release Configuration",
      "configuration": "Release",
      "targets": ["install"]
    },
    {
      "name": "win32-release-ia32",
      "configurePreset": "win32-release-ia32",
      "displayName": "Windows ia32 Local Compilation (Release)",
      "description": "NetEase MSS C wrapper for Windows ia32 - Release Configuration",
      "configuration": "Release",
      "targets": ["install"]
    }
  ],
  "testPresets": [ # test阶段的配置
    {
      "name": "darwin-debug",
      "configurePreset": "darwin-debug",
      "output": {"outputOnFailure": true},
      "execution": {"noTestsAction": "error", "stopOnFailure": true}
    },
    {
      "name": "darwin-release-arm64",
      "configurePreset": "darwin-release-arm64",
      "output": {"outputOnFailure": true},
      "execution": {"noTestsAction": "error", "stopOnFailure": true}
    }
  ]
}
```

### CMake 的 Generator 相关知识

- cmake 会通过 cmakelist.txt 文件，生成适用于不同项目类型的 makefile 文件，然后 makefile 文件被不同的编译器使用进行编译，考虑到 C/C++ 的开发环境之多，有非常多的种类的项目开发环境，但是 cmake 基本上都考虑到了，这里做一个小的汇总。
  - Visual Studio 6: 生成 Visual Studio 6 工程文件。
  - Visual Studio 7: 生成 Visual Studio .NET 2002 工程文件。
  - Visual Studio 10: 生成 Visual Studio 10(2010) 工程文件。
  - Visual Studio 10 Win64 会生成 x64 平台的工程;Visual Studio 10 IA64 是 Itanium 平台。
  - Visual Studio 11: 生成 Visual Studio 11(2012) 工程文件。
  - Visual Studio 11 Win64 会生成 x64 平台的工程;Visual Studio 11 ARM 是 ARM 平台。
  - Visual Studio 7 .NET 2003: 生成 Visual Studio 7 .NET 2003 工程文件。
  - Visual Studio 8 2005: 生成 Visual Studio 8 2005 工程文件。
  - Visual Studio 8 2005 Win64 会生成 x64 平台的工程。
  - Visual Studio 9 2008: 生成 Visual Studio 9 2008 工程文件。
  - Visual Studio 9 2008 Win64 会生成 x64 平台的工程;Visual Studio 9 2008 IA64 是 Itanium 平台。
  - Borland Makefiles: 生成 Borland makefile。
  - NMake Makefiles: 生成 NMake makefile。
  - NMake Makefiles JOM: 生成 JOM makefile。
  - Watcom WMake: 生成 Watcom WMake makefiles。
  - MSYS Makefiles: 生成 MSYS makefile。 生成的 makefile 用 /bin/sh 作为它的 shell。在运行 CMake 的机器上需要安装 msys
  - MinGW Makefiles: 生成供 mingw32-make 使用的 make file。 生成的 makefile 使用 cmd.exe 作为它的 shell。生成它们不需要 msys 或者 unix shell。
  - Unix Makefiles: 生成标准的 UNIX makefile。 在构建树上生成分层的 UNIX makefile。任何标准的 UNIX 风格的 make 程序都可以通过默认的 make 目标构建工程。生成的 makefile 也提供了 install 目标。
  - Ninja：生成.ninja 工程
  - Xcode：生成 Xcode 工程
  - CodeBlocks - MinGW Makefiles：生成 CodeBlocks 工程。
  - 在顶层目录以及每层子目录下为 CodeBlocks 生成工程文件，生成的 CMakeList.txt 的特点是都包含一个 PROJECT()调用。除此之外还会在构建树上生成一套层次性的 makefile。通过默认的 make 目标，正确的 make 程序可以构建这个工程。makefile 还提供了 install 目标。
  - CodeBlocks - NMake Makefiles：生成 CodeBlocks 工程。 在顶层目录以及每层子目录下为 CodeBlocks 生成工程文件，生成的 CMakeList.txt 的特点是都包含一个 PROJECT()调用。除此之外还会在构建树上生成一套层次性的 makefile。通过默认的 make 目标，正确的 make 程序可以构建这个工程。makefile 还提供了 install 目标。
  - CodeBlocks - Ninja：生成 CodeBlocks 工程。
  - CodeBlocks - Unix Makefiles：生成 CodeBlocks 工程。 在顶层目录以及每层子目录下为 CodeBlocks 生成工程文件，生成的 CMakeList.txt 的特点是都包含一个 PROJECT()调用。除此之外还会在构建树上生成一套层次性的 makefile。通过默认的 make 目标，正确的 make 程序可以构建这个工程。makefile 还提供了 install 目标。
  - Eclipse CDT4 - MinGW Makefiles: 生成 Eclipse CDT 4.0 工程文件。 在顶层目录下为 Eclipse 生成工程文件。在运行源码外构建时，一个连接到顶层源码路径的资源文件会被创建。除此之外还会在构建树上生成一套层次性的 makefile。通过默认的 make 目标，正确的 make 程序可以构建这个工程。makefile 还提供了 install 目标。
  - Eclipse CDT4 - NMake Makefiles: 生成 Eclipse CDT 4.0 工程文件。 在顶层目录下为 Eclipse 生成工程文件。在运行源码外构建时，一个连接到顶层源码路径的资源文件会被创建。除此之外还会在构建树上生成一套层次性的 makefile。通过默认的 make 目标，正确的 make 程序可以构建这个工程。makefile 还提供了 install 目标。
  - Eclipse CDT4 - NMake Makefiles：生成 Eclipse CDT 4.0 工程文件。
  - Eclipse CDT4 - Ninja：生成 Eclipse CDT 4.0 工程文件。
  - Eclipse CDT4 - Unix Makefiles: 生成 Eclipse CDT 4.0 工程文件。 在顶层目录下为 Eclipse 生成工程文件。在运行源码外构建时，一个连接到顶层源码路径的资源文件会被创建。除此之外还会在构建树上生成一套层次性的 makefile。通过默认的 make 目标，正确的 make 程序可以构建这个工程。makefile 还提供了 install 目标。
  - KDevelop3: 生成 KDevelop 3 工程文件。
  - KDevelop3 - Unix Makefiles: 生成 KDevelop 3 工程文件。
  - Sublime Text 2 - MinGW Makefiles: 生成 Sublime Text 2 工程文件。
  - Sublime Text 2 - NMake Makefiles: 生成 Sublime Text 2 工程文件。
  - Sublime Text 2 - Ninja: 生成 Sublime Text 2 工程文件。
  - Sublime Text 2 - Unix Makefiles: 生成 Sublime Text 2 工程文件。

## Makefile


