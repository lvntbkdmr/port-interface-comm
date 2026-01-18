cmake_minimum_required(VERSION 3.14)
project(EgiCmpExtPkg LANGUAGES CXX)

# Header-only interface library for EGI Component external interfaces
add_library(EgiCmpExtPkg INTERFACE)

target_include_directories(EgiCmpExtPkg
    INTERFACE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_compile_features(EgiCmpExtPkg INTERFACE cxx_std_17)

# Depends on EgiMgrExtPkg for EgiVorExtDataType (in EgiExtDataType.h)
if(TARGET EgiMgrExtPkg)
    target_link_libraries(EgiCmpExtPkg INTERFACE EgiMgrExtPkg)
endif()
