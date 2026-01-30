cmake_minimum_required(VERSION 3.16)
project(PortInterfaceComm VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Create symlink for compile_commands.json at project root
execute_process(
    COMMAND ${CMAKE_COMMAND} -E create_symlink
        ${CMAKE_BINARY_DIR}/compile_commands.json
        ${CMAKE_SOURCE_DIR}/compile_commands.json
)

# Interface-only packages (headers only)
add_subdirectory(EgiCmpExtPkg)
add_subdirectory(EgiMgrExtPkg)
add_subdirectory(RadaltMgrExtPkg)

# Implementation packages - order matters for dependencies
add_subdirectory(EgiCmpPkg)
add_subdirectory(EgiMgrPkg)
add_subdirectory(RadaltMgrPkg)
add_subdirectory(PartitionPkg)
