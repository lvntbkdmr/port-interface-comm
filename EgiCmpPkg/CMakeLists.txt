cmake_minimum_required(VERSION 3.14)
project(EgiCmpPkg LANGUAGES CXX)

# EGI Component library
add_library(EgiCmpPkg
    src/EgiCmpCls.cpp
)

target_include_directories(EgiCmpPkg
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/inc>
        $<INSTALL_INTERFACE:include>
)

target_compile_features(EgiCmpPkg PUBLIC cxx_std_17)

# Dependencies
if(TARGET EgiMgrExtPkg)
    target_link_libraries(EgiCmpPkg PUBLIC EgiMgrExtPkg)
endif()

if(TARGET RadaltMgrExtPkg)
    target_link_libraries(EgiCmpPkg PUBLIC RadaltMgrExtPkg)
endif()

if(TARGET EgiCmpExtPkg)
    target_link_libraries(EgiCmpPkg PUBLIC EgiCmpExtPkg)
endif()
