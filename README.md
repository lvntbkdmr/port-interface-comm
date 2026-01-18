# Port Interface Communication

A component-based C++ project implementing port-based inter-component communication, following patterns typical of avionics/real-time systems.

## Architecture

### Component Hierarchy

```
PartitionCls (top-level container)
├── EgiMgrCls
│   ├── EgiLruMgrCls (LRU manager)
│   └── EgiCmpCls (component)
├── RadaltMgrCls
│   └── RadaltLruMgrCls (LRU manager)
└── VorIlsMgrCls
    └── VorIlsLruMgrCls (LRU manager)
```

### Port Interface Pattern

Components communicate through typed port interfaces:

- **Output ports**: Member pointers to interface types (e.g., `m_egiOut`, `m_commandOut`)
- **Setters**: Methods to wire ports (e.g., `SetEgiOut()`, `SetCommandOut()`)
- **Input ports**: Classes implement interfaces and receive data via virtual methods
- **Wiring**: Done in `InitRelations()` methods, called from constructors

## Communication Flows

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PartitionCls                                   │
│                                                                             │
│  ┌──────────────────────────────────────────┐    ┌───────────────────────┐  │
│  │              EgiMgrCls                   │    │    RadaltMgrCls       │  │
│  │                                          │    │                       │  │
│  │  ┌──────────────┐    ┌──────────────┐   │    │  ┌─────────────────┐  │  │
│  │  │ EgiLruMgrCls │    │  EgiCmpCls   │   │    │  │ RadaltLruMgrCls │  │  │
│  │  └──────┬───────┘    └───────▲──▲───┘   │    │  └────────▲────┬───┘  │  │
│  │         │                    │  │       │    │           │    │      │  │
│  │         │    EgiCommandIfc   │  │       │    │           │    │      │  │
│  │         └────────────────────┘  │       │    │           │    │      │  │
│  │                                 │       │    │           │    │      │  │
│  └─────────┬───────────────────────┼───────┘    └───────────┼────┼──────┘  │
│            │                       │                        │    │         │
│            │     EgiExtDataIfc     │    RadaltExtDataIfc    │    │         │
│            └───────────────────────┼────────────────────────┘    │         │
│                                    │                             │         │
│                                    └─────────────────────────────┘         │
│                                                                             │
│  ┌──────────────────────────────────────────┐                               │
│  │            VorIlsMgrCls                  │                               │
│  │                                          │                               │
│  │  ┌─────────────────┐                     │                               │
│  │  │ VorIlsLruMgrCls ◄─────────────────────┼───── EgiVorExtDataIfc ────────┤
│  │  └─────────────────┘                     │         (from EgiCmpCls)      │
│  │                                          │                               │
│  └──────────────────────────────────────────┘                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Flow Details

| Source | Destination | Interface | Data Type | Description |
|--------|-------------|-----------|-----------|-------------|
| EgiLruMgrCls | RadaltLruMgrCls | EgiExtDataIfc | EgiExtDataType | EGI external data |
| RadaltLruMgrCls | EgiCmpCls | RadaltExtDataIfc | RadaltExtDataType | Radar altimeter data |
| EgiLruMgrCls | EgiCmpCls | EgiCommandIfc | EgiCommandType | Command messages |
| EgiCmpCls | VorIlsLruMgrCls | EgiVorExtDataIfc | EgiVorExtDataType | VOR/ILS navigation data |

### Data Types

| Type | Location | Fields |
|------|----------|--------|
| EgiExtDataType | EgiMgrExtPkg/EgiExtDataType.h | `int exampleField` |
| EgiVorExtDataType | EgiMgrExtPkg/EgiExtDataType.h | `double latitude`, `double longitude` |
| EgiCommandType | EgiMgrPkg/inc/EgiCommandType.h | `int commandId`, `float commandValue` |
| RadaltExtDataType | RadaltMgrExtPkg/RadaltExtDataType.h | `int altitudeField` |

### Interface Locations

| Interface | Location |
|-----------|----------|
| EgiExtDataIfc | EgiMgrExtPkg/EgiExtDataIfc.h |
| EgiCommandIfc | EgiMgrExtPkg/EgiCommandIfc.h |
| RadaltExtDataIfc | RadaltMgrExtPkg/RadaltExtDataIfc.h |
| EgiVorExtDataIfc | EgiCmpExtPkg/EgiVorExtDataIfc.h |

## Building

```bash
# Configure and build
mkdir -p build && cd build
cmake .. -DBUILD_TESTS=ON
cmake --build .
```

## Testing

Unit tests are located in each package's `tests/` directory. Integration tests are in the central `tests/` directory.

```bash
# Run all tests (from build directory)
ctest

# Run all tests with output
ctest --output-on-failure

# Run a specific package's tests
./EgiCmpPkg/tests/EgiCmpPkg_tests
./EgiMgrPkg/tests/EgiMgrPkg_tests
./RadaltMgrPkg/tests/RadaltMgrPkg_tests
./PartitionPkg/tests/PartitionPkg_tests

# Run tests matching a pattern
ctest -R EgiCmpClsTest
ctest -R IntegrationTest

# List all available tests
ctest -N
```

### Test Structure

| Package | Test File | Test Suite |
|---------|-----------|------------|
| EgiCmpPkg | test_EgiCmpCls.cpp | EgiCmpClsTest |
| EgiMgrPkg | test_EgiLruMgrCls.cpp | EgiLruMgrClsTest |
| EgiMgrPkg | test_EgiMgrCls.cpp | EgiMgrClsTest |
| EgiMgrExtPkg | test_EgiExtDataType.cpp | EgiExtDataTypeTest |
| RadaltMgrPkg | test_RadaltLruMgrCls.cpp | RadaltLruMgrClsTest |
| RadaltMgrPkg | test_RadaltMgrCls.cpp | RadaltMgrClsTest |
| PartitionPkg | test_PartitionCls.cpp | PartitionClsTest |
| tests/ | test_Integration.cpp | IntegrationTest |
