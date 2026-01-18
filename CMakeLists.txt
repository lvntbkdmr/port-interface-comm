cmake_minimum_required(VERSION 3.14)
project(PortInterfaceComm LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

option(BUILD_TESTS "Build tests" ON)
option(USE_VENDORED_GTEST "Use vendored GoogleTest from third_party/" ON)

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
    include(CTest)  # Creates DartConfiguration.tcl and enables testing

    # GoogleTest setup
    if(USE_VENDORED_GTEST AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/third_party/googletest/CMakeLists.txt")
        # Use vendored GoogleTest (for offline/intranet builds)
        set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)  # For Windows
        set(BUILD_GMOCK OFF CACHE BOOL "" FORCE)
        set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
        add_subdirectory(third_party/googletest)
        # Create aliases to match system GTest target names
        if(NOT TARGET GTest::gtest)
            add_library(GTest::gtest ALIAS gtest)
        endif()
        if(NOT TARGET GTest::gtest_main)
            add_library(GTest::gtest_main ALIAS gtest_main)
        endif()
        message(STATUS "Using vendored GoogleTest")
    else()
        # Fall back to system GoogleTest
        find_package(GTest REQUIRED)
        message(STATUS "Using system GoogleTest")
    endif()

    include(GoogleTest)

    # Integration tests
    add_subdirectory(tests)
    # Unit tests for each package
    add_subdirectory(EgiMgrExtPkg/tests)
    add_subdirectory(EgiCmpPkg/tests)
    add_subdirectory(EgiMgrPkg/tests)
    add_subdirectory(RadaltMgrPkg/tests)
    add_subdirectory(PartitionPkg/tests)
endif()
