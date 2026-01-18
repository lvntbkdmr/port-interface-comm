cmake_minimum_required(VERSION 3.14)
project(RadaltMgrExtPkg LANGUAGES CXX)

# Header-only interface library for Radar Altimeter Manager external interfaces
add_library(RadaltMgrExtPkg INTERFACE)

target_include_directories(RadaltMgrExtPkg
    INTERFACE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_compile_features(RadaltMgrExtPkg INTERFACE cxx_std_17)
