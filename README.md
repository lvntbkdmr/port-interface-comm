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

**Documentation:**
- [Port Interface Guide](docs/PORT_INTERFACE_GUIDE.md) - Step-by-step instructions for creating new port connections
- [Migration Guide](docs/MIGRATION_GUIDE.md) - Converting from the old macro-based pattern to the new simplified pattern

**Claude Code Skills (for automated migration):**
- `/migrate-scan` - Scan codebase to identify classes needing migration
- `/migrate-port <ClassName>` - Migrate a single class to the new pattern
- `/migrate-wiring` - Update PartitionCls to use direct port wiring

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

### Host Build (for development and testing)

Build natively on the development machine to run unit tests:

```bash
# Windows (cmd)
mkdir build-host
cd build-host
cmake .. -DBUILD_TESTS=ON
cmake --build .

# Windows (PowerShell)
cmake -B build-host -DBUILD_TESTS=ON
cmake --build build-host

# Linux/macOS
cmake -B build-host -DBUILD_TESTS=ON
cmake --build build-host
```

### Cross-Compilation (for target deployment)

Build for the target architecture without tests:

```bash
# Copy and customize the toolchain file
cp cmake/toolchain-target.cmake.example cmake/toolchain-target.cmake
# Edit cmake/toolchain-target.cmake with your cross-compiler paths

# Cross-compile
cmake -B build-target -DCMAKE_TOOLCHAIN_FILE=cmake/toolchain-target.cmake
cmake --build build-target
```

### Build Options

| Option | Default | Description |
|--------|---------|-------------|
| `BUILD_TESTS` | ON | Build unit and integration tests |
| `USE_VENDORED_GTEST` | ON | Use GoogleTest from third_party/ (for offline builds) |

```bash
# Example: Use system GoogleTest instead of vendored
cmake -B build -DBUILD_TESTS=ON -DUSE_VENDORED_GTEST=OFF
```

### Offline/Intranet Development

This project includes GoogleTest in `third_party/` for environments without internet access. The vendored GoogleTest is used by default, requiring no external downloads.

## Testing

Unit tests are located in each package's `tests/` directory. Integration tests are in the central `tests/` directory.

**Note:** Tests are designed to run on the host machine only. When cross-compiling, tests are automatically disabled.

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
