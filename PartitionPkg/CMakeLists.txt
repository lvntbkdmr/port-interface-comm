add_library(PartitionPkg STATIC
    src/PartitionCls.cpp
)

target_include_directories(PartitionPkg PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/inc
)

target_link_libraries(PartitionPkg PUBLIC
    EgiMgrPkg
    RadaltMgrPkg
)
