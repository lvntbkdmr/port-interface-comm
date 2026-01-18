cmake_minimum_required(VERSION 3.14)
project(VorIlsMgrPkg LANGUAGES CXX)

# VOR/ILS Manager library
add_library(VorIlsMgrPkg
    src/VorIlsLruMgrCls.cpp
    src/VorIlsMgrCls.cpp
)

target_include_directories(VorIlsMgrPkg
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/inc>
        $<INSTALL_INTERFACE:include>
)

target_compile_features(VorIlsMgrPkg PUBLIC cxx_std_17)

# Dependencies
if(TARGET EgiCmpExtPkg)
    target_link_libraries(VorIlsMgrPkg PUBLIC EgiCmpExtPkg)
endif()
