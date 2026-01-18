cmake_minimum_required(VERSION 3.14)
project(PortInterfaceComm LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

option(BUILD_TESTS "Build tests" ON)

# Interface packages (header-only)
add_subdirectory(EgiMgrExtPkg)
add_subdirectory(RadaltMgrExtPkg)
add_subdirectory(EgiCmpExtPkg)

# Library packages
add_subdirectory(EgiCmpPkg)
add_subdirectory(EgiMgrPkg)
add_subdirectory(RadaltMgrPkg)
add_subdirectory(VorIlsMgrPkg)
add_subdirectory(PartitionPkg)

# Tests
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()
