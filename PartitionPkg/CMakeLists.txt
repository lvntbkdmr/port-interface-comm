cmake_minimum_required(VERSION 3.14)
project(PartitionPkg LANGUAGES CXX)

# Partition library (top-level container)
add_library(PartitionPkg
    src/PartitionCls.cpp
)

target_include_directories(PartitionPkg
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/inc>
        $<INSTALL_INTERFACE:include>
)

target_compile_features(PartitionPkg PUBLIC cxx_std_17)

# Dependencies
if(TARGET EgiMgrPkg)
    target_link_libraries(PartitionPkg PUBLIC EgiMgrPkg)
endif()

if(TARGET RadaltMgrPkg)
    target_link_libraries(PartitionPkg PUBLIC RadaltMgrPkg)
endif()

if(TARGET VorIlsMgrPkg)
    target_link_libraries(PartitionPkg PUBLIC VorIlsMgrPkg)
endif()
