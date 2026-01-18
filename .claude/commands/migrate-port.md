# Migrate Port Pattern

Migrate a class from the old verbose port-macro pattern to the new simplified port interface pattern.

## Usage

```
/migrate-port <ClassName>
```

Example: `/migrate-port EgiLruMgrCls`

## Arguments

- `$ARGUMENTS` - The class name to migrate (e.g., `EgiLruMgrCls`)

## Instructions

Follow these steps to migrate the specified class to the new port interface pattern:

### Step 1: Find the class files

Search for the header and source files:
- `*Pkg/inc/<ClassName>.h`
- `*Pkg/src/<ClassName>.cpp`

Read both files to understand the current implementation.

### Step 2: Identify old pattern elements

Look for these old pattern indicators:
- `#include <PortMacros.h>` - Remove this include
- `Its*Port*Ifc` members (e.g., `ItsDataOutPortEgiExtDataIfc`)
- `OUT_PORT(...)` macro calls
- `Set*Its*Port*()` or `set*Its*Port*()` methods
- `Get*In*Port*()` methods that return `this`

### Step 3: Rename port members

Transform port member names:

| Old Pattern | New Pattern |
|-------------|-------------|
| `ItsDataOutPortEgiExtDataIfc` | `m_egiOut` |
| `ItsDataOutPortRadaltExtDataIfc` | `m_radaltOut` |
| `ItsCommandOutPortEgiCommandIfc` | `m_commandOut` |
| `Its<Name>OutPort<Interface>Ifc` | `m_<name>Out` |

Rules:
- Change `protected:` to `private:` for port members
- Initialize to `nullptr`: `EgiExtDataIfc* m_egiOut{nullptr};`

### Step 4: Rename setter methods

Transform setter method names:

| Old Pattern | New Pattern |
|-------------|-------------|
| `SetItsDataOutPortEgiExtDataIfc()` | `SetEgiOut()` |
| `setItsDataOutPortEgiExtDataIfc()` | `SetEgiOut()` |
| `Set*Its*Port*Ifc()` | `Set*Out()` |

Update both header declaration and source implementation.

### Step 5: Replace OUT_PORT macro usage

In the source file, replace:

```cpp
// OLD
OUT_PORT(DataOutPort, EgiExtDataIfc)->SetEgiExtData(data);

// NEW
if (m_egiOut != nullptr) {
    m_egiOut->SetEgiExtData(data);
}
```

Always add null check before calling through port pointer.

### Step 6: Remove PortMacros.h include

Remove this line from the source file:
```cpp
#include <PortMacros.h>
```

### Step 7: Remove GetXxxIn() methods (if present)

If the class has methods like:
```cpp
EgiExtDataIfc* GetItsRadaltEgiInPortEgiExtDataIfc() { return this; }
```

Remove them entirely. C++ implicit upcasting handles this automatically.

### Step 8: Add sub-component accessors (for Manager classes only)

If this is a Manager class (e.g., `EgiMgrCls`, `RadaltMgrCls`), add getter methods for sub-components:

```cpp
// In header, public section:
EgiLruMgrCls& GetEgiLruMgr() { return EgiLruMgr; }
EgiCmpCls& GetEgiCmp() { return EgiCmp; }
```

### Step 9: Remove proxy setter methods (for Manager classes only)

If this is a Manager class that has proxy methods like:
```cpp
void SetItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc)
{
    EgiLruMgr.setItsDataOutPortEgiExtDataIfc(ifc);
}
```

Remove these entirely. Port wiring is now done directly to sub-components.

### Step 10: Update tests

Find test files for this class:
- `*Pkg/tests/test_<ClassName>.cpp`
- `tests/test_<ClassName>.cpp`

Update any references to old method names.

### Step 11: Verify compilation

After making changes, verify the code compiles:
```bash
cmake --build build
```

### Step 12: Run tests

Run tests to verify functionality:
```bash
ctest -R <ClassName>Test
```

## Example Migration

### Before (EgiLruMgrCls.h):
```cpp
#ifndef EGILRUMGR_H
#define EGILRUMGR_H

#include <EgiExtDataIfc.h>

class EgiLruMgrCls
{
public:
    void setItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc);
    void PeriodicRun();

protected:
    EgiExtDataIfc* ItsDataOutPortEgiExtDataIfc;
};
#endif
```

### After (EgiLruMgrCls.h):
```cpp
#ifndef EGILRUMGRCLS_H
#define EGILRUMGRCLS_H

#include <EgiExtDataIfc.h>

class EgiLruMgrCls
{
public:
    void SetEgiOut(EgiExtDataIfc* port);
    void PeriodicRun();

private:
    EgiExtDataIfc* m_egiOut{nullptr};
};
#endif
```

### Before (EgiLruMgrCls.cpp):
```cpp
#include <EgiLruMgrCls.h>
#include <PortMacros.h>

void EgiLruMgrCls::setItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc)
{
    ItsDataOutPortEgiExtDataIfc = ifc;
}

void EgiLruMgrCls::PeriodicRun()
{
    EgiExtDataType data;
    data.exampleField = 42;
    OUT_PORT(DataOutPort, EgiExtDataIfc)->SetEgiExtData(data);
}
```

### After (EgiLruMgrCls.cpp):
```cpp
#include <EgiLruMgrCls.h>

void EgiLruMgrCls::SetEgiOut(EgiExtDataIfc* port)
{
    m_egiOut = port;
}

void EgiLruMgrCls::PeriodicRun()
{
    if (m_egiOut != nullptr) {
        EgiExtDataType data;
        data.exampleField = 42;
        m_egiOut->SetEgiExtData(data);
    }
}
```

## Output

After successful migration, report:
1. Files modified
2. Old patterns removed
3. New patterns applied
4. Compilation status
5. Test results
