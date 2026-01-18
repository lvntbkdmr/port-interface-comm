cmake_minimum_required(VERSION 3.14)
project(EgiMgrExtPkg LANGUAGES CXX)

# Header-only interface library for EGI Manager external interfaces
add_library(EgiMgrExtPkg INTERFACE)

target_include_directories(EgiMgrExtPkg
    INTERFACE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_compile_features(EgiMgrExtPkg INTERFACE cxx_std_17)
