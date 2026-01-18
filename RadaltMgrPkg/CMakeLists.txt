cmake_minimum_required(VERSION 3.14)
project(RadaltMgrPkg LANGUAGES CXX)

# Radar Altimeter Manager library
add_library(RadaltMgrPkg
    src/RadaltLruMgrCls.cpp
    src/RadaltMgrCls.cpp
)

target_include_directories(RadaltMgrPkg
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/inc>
        $<INSTALL_INTERFACE:include>
)

target_compile_features(RadaltMgrPkg PUBLIC cxx_std_17)

# Dependencies
if(TARGET EgiMgrExtPkg)
    target_link_libraries(RadaltMgrPkg PUBLIC EgiMgrExtPkg)
endif()

if(TARGET RadaltMgrExtPkg)
    target_link_libraries(RadaltMgrPkg PUBLIC RadaltMgrExtPkg)
endif()
