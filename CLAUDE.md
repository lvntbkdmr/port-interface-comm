# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Compile all source files to object files
clang++ -std=c++17 -c \
  -I EgiMgrPkg/inc \
  -I EgiMgrExtPkg \
  -I PartitionPkg/inc \
  -I RadaltMgrPkg/inc \
  -I EgiCmpPkg/inc \
  EgiMgrPkg/src/*.cpp \
  EgiCmpPkg/src/*.cpp \
  PartitionPkg/src/*.cpp \
  RadaltMgrPkg/src/*.cpp

# Move object files to out directory
mv *.o out/

# Compile and run all tests
clang++ -std=c++17 \
  -I /opt/homebrew/include \
  -I EgiMgrPkg/inc \
  -I EgiMgrExtPkg \
  -I PartitionPkg/inc \
  -I RadaltMgrPkg/inc \
  -I EgiCmpPkg/inc \
  -L /opt/homebrew/lib \
  -lgtest -lgtest_main -pthread \
  tests/test_*.cpp \
  EgiMgrPkg/src/*.cpp \
  EgiCmpPkg/src/*.cpp \
  PartitionPkg/src/*.cpp \
  RadaltMgrPkg/src/*.cpp \
  -o out/run_tests && ./out/run_tests

# Run a single test suite
./out/run_tests --gtest_filter=IntegrationTest.*

# Run a single test
./out/run_tests --gtest_filter=IntegrationTest.EgiLruMgrSendsDataToRadaltLruMgr
```

## Architecture

This is a component-based C++ project implementing port-based inter-component communication, following patterns typical of avionics/real-time systems.

### Component Hierarchy

```
PartitionCls (top-level container)
├── EgiMgrCls (EGI manager)
│   └── EgiLruMgrCls (LRU manager)
│       └── EgiCmpCls (component)
└── RadaltMgrCls (Radar Altimeter manager)
    └── RadaltLruMgrCls (LRU manager, implements EgiExtDataIfc)
```

### Port Interface Pattern

Components communicate through typed port interfaces using a simple naming convention:
- Output ports: `m_egiOut`, `m_radaltOut` (member variables)
- Setters: `SetEgiOut()`, `SetRadaltOut()`
- Input port getters: `GetEgiIn()`, `GetRadaltIn()` (return `this`)

Data flows from `EgiLruMgrCls` → `RadaltLruMgrCls` via the `EgiExtDataIfc` interface.

### Lifecycle Methods

All manager classes follow a consistent lifecycle:
1. Constructor calls `InitRelations()` to wire up port connections
2. `Initialize()` initializes sub-components
3. `PeriodicRun()` executes the periodic processing cycle

### Key Interfaces

- `EgiExtDataIfc` - Abstract interface for receiving EGI external data
- `EgiExtDataType` - Data structure passed through the interface

### Package Structure

Each package follows `inc/` (headers) and `src/` (implementation) convention, except `EgiMgrExtPkg` which has headers at the package root.
