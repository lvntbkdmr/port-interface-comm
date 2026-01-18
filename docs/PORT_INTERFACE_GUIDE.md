# Port Interface Guide

This guide explains how to create new port-interface connections between classes in this project.

## Overview

The port interface pattern enables type-safe, decoupled communication between components:

```
Sender ──[Interface]──► Receiver
```

- **Sender**: Has an output port (pointer to interface) and calls interface methods
- **Receiver**: Implements the interface and receives data via virtual methods
- **Interface**: Abstract class defining the communication contract

## Step-by-Step: Creating a New Port Connection

### Example Scenario

We want to send `FooDataType` from `SenderCls` to `ReceiverCls`.

---

### Step 1: Define the Data Type

Create or locate the data type in the appropriate `*ExtPkg` package.

**File: `SenderExtPkg/FooDataType.h`**
```cpp
#ifndef FOODATATYPE_H
#define FOODATATYPE_H

struct FooDataType {
    int fieldA;
    float fieldB;
};

#endif
```

> **Naming Convention**: Data types end with `Type` (e.g., `EgiExtDataType`, `RadaltExtDataType`)

---

### Step 2: Define the Interface

Create the interface in the sender's external package.

**File: `SenderExtPkg/FooDataIfc.h`**
```cpp
#ifndef FOODATAIFC_H
#define FOODATAIFC_H

#include <FooDataType.h>

class FooDataIfc {
public:
    virtual ~FooDataIfc() = default;
    virtual void SetFooData(const FooDataType& data) = 0;
};

#endif
```

> **Naming Convention**: Interfaces end with `Ifc` (e.g., `EgiExtDataIfc`, `EgiCommandIfc`)

---

### Step 3: Implement the Interface in the Receiver

**File: `ReceiverPkg/inc/ReceiverCls.h`**
```cpp
#ifndef RECEIVERCLS_H
#define RECEIVERCLS_H

#include <FooDataIfc.h>  // Add include

class ReceiverCls : public FooDataIfc {  // Add inheritance
public:
    ReceiverCls();
    void Initialize();
    void PeriodicRun();

    // Implement the interface
    void SetFooData(const FooDataType& data) override;

private:
    // Optional: store received data
    FooDataType m_lastFooData{};
};

#endif
```

**File: `ReceiverPkg/src/ReceiverCls.cpp`**
```cpp
#include <ReceiverCls.h>

// Receive data from Sender
void ReceiverCls::SetFooData(const FooDataType& data)
{
    m_lastFooData = data;
    // Process the received data as needed
}
```

---

### Step 4: Add Output Port to the Sender

**File: `SenderPkg/inc/SenderCls.h`**
```cpp
#ifndef SENDERCLS_H
#define SENDERCLS_H

#include <FooDataIfc.h>  // Add include

class SenderCls {
public:
    SenderCls();
    void Initialize();
    void PeriodicRun();

    // Output port setter
    void SetFooOut(FooDataIfc* port);

private:
    // Output port
    FooDataIfc* m_fooOut{nullptr};
};

#endif
```

**File: `SenderPkg/src/SenderCls.cpp`**
```cpp
#include <SenderCls.h>

// Set output port for Foo data
void SenderCls::SetFooOut(FooDataIfc* port)
{
    m_fooOut = port;
}

void SenderCls::PeriodicRun()
{
    // Send data through the port
    if (m_fooOut != nullptr) {
        FooDataType data;
        data.fieldA = 42;
        data.fieldB = 3.14f;
        m_fooOut->SetFooData(data);
    }
}
```

> **Naming Convention**:
> - Output port members: `m_fooOut`, `m_egiOut`, `m_commandOut`
> - Setter methods: `SetFooOut()`, `SetEgiOut()`, `SetCommandOut()`

---

### Step 5: Wire the Connection

Wire the port in the parent class's `InitRelations()` method.

**File: `ParentPkg/src/ParentCls.cpp`**
```cpp
void ParentCls::InitRelations()
{
    // Sender sends Foo data to Receiver
    Sender.SetFooOut(&Receiver);  // Implicit upcast to FooDataIfc*
}
```

> **Note**: C++ implicitly upcasts `&Receiver` to `FooDataIfc*` because `ReceiverCls` inherits from `FooDataIfc`.

---

### Step 6: Update CMakeLists.txt (if needed)

If you created new files in an ExtPkg, ensure the package's CMakeLists.txt includes them.

For interface packages (header-only), no changes needed - headers are included via the directory.

For library packages, ensure dependencies are linked:

```cmake
target_link_libraries(ReceiverPkg PUBLIC SenderExtPkg)
```

---

## Real Examples from This Project

### Example 1: EgiLruMgrCls → RadaltLruMgrCls (EgiExtDataType)

| Component | File | What to Add |
|-----------|------|-------------|
| Data Type | `EgiMgrExtPkg/EgiExtDataType.h` | `struct EgiExtDataType` |
| Interface | `EgiMgrExtPkg/EgiExtDataIfc.h` | `class EgiExtDataIfc` |
| Receiver | `RadaltMgrPkg/inc/RadaltLruMgrCls.h` | Inherit `EgiExtDataIfc`, implement `SetEgiExtData()` |
| Sender | `EgiMgrPkg/inc/EgiLruMgrCls.h` | Add `m_egiOut` port, `SetEgiOut()` method |
| Wiring | `PartitionPkg/src/PartitionCls.cpp` | `EgiMgr.GetEgiLruMgr().SetEgiOut(&RadaltMgr.GetRadaltLruMgr())` |

### Example 2: EgiLruMgrCls → EgiCmpCls (EgiCommandType)

| Component | File | What to Add |
|-----------|------|-------------|
| Data Type | `EgiMgrExtPkg/EgiCommandType.h` | `struct EgiCommandType` |
| Interface | `EgiMgrExtPkg/EgiCommandIfc.h` | `class EgiCommandIfc` |
| Receiver | `EgiCmpPkg/inc/EgiCmpCls.h` | Inherit `EgiCommandIfc`, implement `SetEgiCommand()` |
| Sender | `EgiMgrPkg/inc/EgiLruMgrCls.h` | Add `m_commandOut` port, `SetCommandOut()` method |
| Wiring | `EgiMgrPkg/src/EgiMgrCls.cpp` | `EgiLruMgr.SetCommandOut(&EgiCmp)` (internal wiring) |

### Example 3: EgiCmpCls → VorIlsLruMgrCls (EgiVorExtDataType)

| Component | File | What to Add |
|-----------|------|-------------|
| Data Type | `EgiMgrExtPkg/EgiExtDataType.h` | `struct EgiVorExtDataType` |
| Interface | `EgiCmpExtPkg/EgiVorExtDataIfc.h` | `class EgiVorExtDataIfc` |
| Receiver | `VorIlsMgrPkg/inc/VorIlsLruMgrCls.h` | Inherit `EgiVorExtDataIfc`, implement `SetEgiVorExtData()` |
| Sender | `EgiCmpPkg/inc/EgiCmpCls.h` | Add `m_vorIlsOut` port, `SetVorIlsOut()` method |
| Wiring | `PartitionPkg/src/PartitionCls.cpp` | `EgiMgr.GetEgiCmp().SetVorIlsOut(&VorIlsMgr.GetVorIlsLruMgr())` |

---

## Quick Reference

### File Locations

| Item | Location Pattern |
|------|-----------------|
| Data Types | `<Sender>ExtPkg/<Name>Type.h` |
| Interfaces | `<Sender>ExtPkg/<Name>Ifc.h` |
| Sender Implementation | `<Sender>Pkg/src/<Sender>Cls.cpp` |
| Receiver Implementation | `<Receiver>Pkg/src/<Receiver>Cls.cpp` |
| Cross-Manager Wiring | `PartitionPkg/src/PartitionCls.cpp` |
| Internal Wiring | `<Manager>Pkg/src/<Manager>Cls.cpp` |

### Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Data Type | `<Name>Type` | `EgiExtDataType` |
| Interface | `<Name>Ifc` | `EgiExtDataIfc` |
| Interface Method | `Set<Name>()` | `SetEgiExtData()` |
| Output Port Member | `m_<name>Out` | `m_egiOut` |
| Output Port Setter | `Set<Name>Out()` | `SetEgiOut()` |

### Checklist

- [ ] Data type defined in `*ExtPkg`
- [ ] Interface defined in `*ExtPkg`
- [ ] Receiver inherits interface
- [ ] Receiver implements interface method
- [ ] Sender has output port member
- [ ] Sender has output port setter
- [ ] Sender calls interface method in `PeriodicRun()`
- [ ] Port wired in appropriate `InitRelations()`
- [ ] CMakeLists.txt updated if needed
