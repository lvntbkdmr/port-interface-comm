cmake_minimum_required(VERSION 3.14)
project(EgiMgrPkg LANGUAGES CXX)

# EGI Manager library
add_library(EgiMgrPkg
    src/EgiLruMgrCls.cpp
    src/EgiMgrCls.cpp
)

target_include_directories(EgiMgrPkg
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/inc>
        $<INSTALL_INTERFACE:include>
)

target_compile_features(EgiMgrPkg PUBLIC cxx_std_17)

# Dependencies
if(TARGET EgiMgrExtPkg)
    target_link_libraries(EgiMgrPkg PUBLIC EgiMgrExtPkg)
endif()

if(TARGET EgiCmpPkg)
    target_link_libraries(EgiMgrPkg PUBLIC EgiCmpPkg)
endif()
