# CMake Conversion Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Convert the port-interface-comm project to a compilable CMake build system and fix existing code errors.

**Architecture:** Hierarchical CMake structure with a root CMakeLists.txt that includes subdirectories. Each package becomes a static library. Header-only "ExtPkg" packages become INTERFACE libraries. Dependencies are expressed via target_link_libraries.

**Tech Stack:** CMake 3.16+, C++17, GTest for future tests

---

## Task 1: Fix Syntax Errors in EgiCmpCls.cpp

**Files:**
- Modify: `EgiCmpPkg/src/EgiCmpCls.cpp:14,39`

**Step 1: Fix missing semicolon on line 14**

Change line 14 from:
```cpp
    m_EgiFormatterCls.Initialize()
```
to:
```cpp
    m_EgiFormatterCls.Initialize();
```

**Step 2: Fix missing semicolon on line 39**

Change line 39 from:
```cpp
    return ItsItsAns611ControlInPortAns611ControlIfc
```
to:
```cpp
    return ItsItsAns611ControlInPortAns611ControlIfc;
```

---

## Task 2: Fix Interface Class Name Mismatch in Ans611ControlIfc.h

**Files:**
- Modify: `EgiCmpExtPkg/inc/Ans611ControlIfc.h`

**Step 1: Fix class name and add missing method**

The file defines `EgiVorExtDataIfc` but is included as `Ans611ControlIfc`. Code calls `SetAns611ControlData()` but only `SetEgiMode()` exists.

Replace entire file with:
```cpp
#ifndef ANS611CONTROLIFC_H
#define ANS611CONTROLIFC_H

#include <Ans611ControlDataType.h>

class Ans611ControlIfc
{
public:
    virtual void SetEgiMode(const Ans611ControlEgiModeType& data) = 0;
    virtual void SetAns611ControlData(const Ans611ControlEgiModeType& data) = 0;
};

#endif
```

---

## Task 3: Update EgiFormatterCls to Implement New Interface Method

**Files:**
- Modify: `EgiCmpPkg/inc/EgiFormatterCls.h`
- Modify: `EgiCmpPkg/src/EgiFormatterCls.cpp`

**Step 1: Add method declaration to header**

Add after line 16 in `EgiFormatterCls.h`:
```cpp
    void SetAns611ControlData(const Ans611ControlEgiModeType& data) override;
```

**Step 2: Add method implementation to cpp**

Add to `EgiFormatterCls.cpp`:
```cpp
void EgiFormatterCls::SetAns611ControlData(const Ans611ControlEgiModeType& data)
{
    // Forward to SetEgiMode for compatibility
    SetEgiMode(data);
}
```

---

## Task 4: Fix RadaltLruMgrCls.cpp Missing Include

**Files:**
- Modify: `RadaltMgrPkg/src/RadaltLruMgrCls.cpp`

**Step 1: Add missing PortMacros.h include**

Add after line 1:
```cpp
#include <PortMacros.h>
```

---

## Task 5: Create Root CMakeLists.txt

**Files:**
- Create: `CMakeLists.txt`

**Step 1: Write root CMakeLists.txt**

```cmake
cmake_minimum_required(VERSION 3.16)
project(PortInterfaceComm VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Interface-only packages (headers only)
add_subdirectory(EgiCmpExtPkg)
add_subdirectory(EgiMgrExtPkg)
add_subdirectory(RadaltMgrExtPkg)

# Implementation packages
add_subdirectory(EgiCmpPkg)
add_subdirectory(EgiMgrPkg)
add_subdirectory(RadaltMgrPkg)
add_subdirectory(PartitionPkg)
```

---

## Task 6: Create EgiCmpExtPkg CMakeLists.txt (Interface Library)

**Files:**
- Create: `EgiCmpExtPkg/CMakeLists.txt`

**Step 1: Write CMakeLists.txt**

```cmake
add_library(EgiCmpExtPkg INTERFACE)

target_include_directories(EgiCmpExtPkg INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}/inc
)
```

---

## Task 7: Create EgiMgrExtPkg CMakeLists.txt (Interface Library)

**Files:**
- Create: `EgiMgrExtPkg/CMakeLists.txt`

**Step 1: Write CMakeLists.txt**

```cmake
add_library(EgiMgrExtPkg INTERFACE)

target_include_directories(EgiMgrExtPkg INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}
)
```

---

## Task 8: Create RadaltMgrExtPkg CMakeLists.txt (Interface Library)

**Files:**
- Create: `RadaltMgrExtPkg/CMakeLists.txt`

**Step 1: Write CMakeLists.txt**

```cmake
add_library(RadaltMgrExtPkg INTERFACE)

target_include_directories(RadaltMgrExtPkg INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}/inc
)
```

---

## Task 9: Create EgiCmpPkg CMakeLists.txt

**Files:**
- Create: `EgiCmpPkg/CMakeLists.txt`

**Step 1: Write CMakeLists.txt**

```cmake
add_library(EgiCmpPkg STATIC
    src/EgiCmpCls.cpp
    src/EgiFormatterCls.cpp
)

target_include_directories(EgiCmpPkg PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/inc
)

target_link_libraries(EgiCmpPkg PUBLIC
    EgiCmpExtPkg
    RadaltMgrExtPkg
)
```

---

## Task 10: Create EgiMgrPkg CMakeLists.txt

**Files:**
- Create: `EgiMgrPkg/CMakeLists.txt`

**Step 1: Write CMakeLists.txt**

```cmake
add_library(EgiMgrPkg STATIC
    src/EgiMgrCls.cpp
    src/EgiLruMgrCls.cpp
    src/EgiModControllerCls.cpp
)

target_include_directories(EgiMgrPkg PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/inc
)

target_link_libraries(EgiMgrPkg PUBLIC
    EgiCmpPkg
    EgiMgrExtPkg
    EgiCmpExtPkg
    RadaltMgrExtPkg
    PartitionPkg
)
```

---

## Task 11: Create RadaltMgrPkg CMakeLists.txt

**Files:**
- Create: `RadaltMgrPkg/CMakeLists.txt`

**Step 1: Write CMakeLists.txt**

```cmake
add_library(RadaltMgrPkg STATIC
    src/RadaltMgrCls.cpp
    src/RadaltLruMgrCls.cpp
)

target_include_directories(RadaltMgrPkg PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/inc
)

target_link_libraries(RadaltMgrPkg PUBLIC
    EgiMgrExtPkg
    RadaltMgrExtPkg
    PartitionPkg
)
```

---

## Task 12: Create PartitionPkg CMakeLists.txt

**Files:**
- Create: `PartitionPkg/CMakeLists.txt`

**Step 1: Write CMakeLists.txt**

```cmake
add_library(PartitionPkg STATIC
    src/PartitionCls.cpp
)

target_include_directories(PartitionPkg PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/inc
)

target_link_libraries(PartitionPkg PUBLIC
    EgiMgrExtPkg
    RadaltMgrExtPkg
)
```

---

## Task 13: Build and Verify

**Step 1: Clean old build artifacts**

```bash
rm -rf build out
```

**Step 2: Configure CMake**

```bash
cmake -B build -S .
```

Expected: Configuration succeeds

**Step 3: Build the project**

```bash
cmake --build build
```

Expected: Build succeeds with all libraries created

**Step 4: Verify libraries exist**

```bash
ls build/*.a build/*/*.a
```

Expected: Static libraries for each package

---

## Dependency Resolution Notes

The circular dependency between EgiMgrPkg/RadaltMgrPkg/PartitionPkg requires careful ordering:
- PartitionPkg only depends on ExtPkg interfaces (no circular dep)
- EgiMgrPkg and RadaltMgrPkg depend on PartitionPkg for PortMacros.h
- This is resolved by having PartitionPkg only depend on ExtPkg interfaces
