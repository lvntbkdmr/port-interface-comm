# Migration Guide: Converting to the New Port Interface Pattern

This guide explains how to migrate from the old verbose port-macro pattern to the new simplified port interface pattern.

## Overview of Changes

| Aspect | Old Pattern | New Pattern |
|--------|-------------|-------------|
| Port naming | `ItsDataOutPortEgiExtDataIfc` | `m_egiOut` |
| Setter naming | `SetItsDataOutPortEgiExtDataIfc()` | `SetEgiOut()` |
| Port access | `OUT_PORT(DataOutPort, EgiExtDataIfc)->` | `m_egiOut->` |
| Input port getter | `GetItsRadaltEgiInPortEgiExtDataIfc()` | Implicit upcasting |
| Wiring | Through manager hierarchy | Direct to LRU manager |
| Macro usage | `OUT_PORT(p, x)` macro | No macros |

## Migration Steps

### Step 1: Remove PortMacros.h

Delete the `PortMacros.h` file containing the `OUT_PORT` macro:

```cpp
// OLD: PortMacros.h
#define OUT_PORT(p, x) Its##p##x

// NEW: Delete this file entirely
```

Remove all includes of `PortMacros.h` from source files.

---

### Step 2: Rename Port Members

Rename verbose port members to simple naming convention:

**Header File:**
```cpp
// OLD
protected:
    EgiExtDataIfc* ItsDataOutPortEgiExtDataIfc;

// NEW
private:
    EgiExtDataIfc* m_egiOut{nullptr};
```

**Naming Convention:**
| Old Name | New Name |
|----------|----------|
| `ItsDataOutPortEgiExtDataIfc` | `m_egiOut` |
| `ItsDataOutPortRadaltExtDataIfc` | `m_radaltOut` |
| `ItsCommandOutPortEgiCommandIfc` | `m_commandOut` |

---

### Step 3: Rename Setter Methods

Simplify setter method names:

**Header File:**
```cpp
// OLD
void SetItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc);
void setItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc);  // inconsistent casing

// NEW
void SetEgiOut(EgiExtDataIfc* port);
```

**Source File:**
```cpp
// OLD
void EgiLruMgrCls::setItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc)
{
    ItsDataOutPortEgiExtDataIfc = ifc;
}

// NEW
void EgiLruMgrCls::SetEgiOut(EgiExtDataIfc* port)
{
    m_egiOut = port;
}
```

---

### Step 4: Replace Macro Usage with Direct Access

Replace `OUT_PORT()` macro calls with direct member access:

```cpp
// OLD
#include <PortMacros.h>

void EgiLruMgrCls::PeriodicRun()
{
    EgiExtDataType data;
    data.exampleField = 42;
    OUT_PORT(DataOutPort, EgiExtDataIfc)->SetEgiExtData(data);
}

// NEW
void EgiLruMgrCls::PeriodicRun()
{
    if (m_egiOut != nullptr) {
        EgiExtDataType data;
        data.exampleField = 42;
        m_egiOut->SetEgiExtData(data);
    }
}
```

> **Note:** Always add null checks before calling through port pointers.

---

### Step 5: Remove Input Port Getter Methods

Remove boilerplate getter methods that just return `this`. C++ implicit upcasting handles this:

**Old Pattern (Remove This):**
```cpp
// Header
EgiExtDataIfc* GetItsRadaltEgiInPortEgiExtDataIfc();

// Source
EgiExtDataIfc* RadaltLruMgrCls::GetItsRadaltEgiInPortEgiExtDataIfc()
{
    return this;
}
```

**New Pattern (Use Implicit Upcasting):**
```cpp
// No getter method needed!
// When wiring, C++ automatically upcasts:
EgiLruMgr.SetEgiOut(&RadaltLruMgr);  // &RadaltLruMgr implicitly becomes EgiExtDataIfc*
```

---

### Step 6: Add LRU Manager Accessors

Add getter methods to manager classes for direct access to sub-components:

**Header File:**
```cpp
class EgiMgrCls
{
public:
    // Add accessors for sub-components
    EgiLruMgrCls& GetEgiLruMgr() { return EgiLruMgr; }
    EgiCmpCls& GetEgiCmp() { return EgiCmp; }

private:
    EgiLruMgrCls EgiLruMgr;
    EgiCmpCls EgiCmp;
};
```

---

### Step 7: Flatten Port Wiring

Move port wiring from hierarchical delegation to direct wiring in `PartitionCls`:

**Old Pattern (Hierarchical Delegation):**
```cpp
// PartitionCls.cpp - wired through managers
void PartitionCls::InitRelations()
{
    EgiMgr.SetItsDataOutPortEgiExtDataIfc(
        RadaltMgr.GetItsRadaltEgiInPortEgiExtDataIfc()
    );
}

// EgiMgrCls.cpp - had to delegate down
void EgiMgrCls::SetItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc)
{
    EgiLruMgr.setItsDataOutPortEgiExtDataIfc(ifc);
}
```

**New Pattern (Direct Wiring):**
```cpp
// PartitionCls.cpp - wire directly to LRU managers
void PartitionCls::InitRelations()
{
    // EgiLruMgr sends EGI external data to RadaltLruMgr
    EgiMgr.GetEgiLruMgr().SetEgiOut(&RadaltMgr.GetRadaltLruMgr());

    // RadaltLruMgr sends radar altimeter data to EgiCmp
    RadaltMgr.GetRadaltLruMgr().SetRadaltOut(&EgiMgr.GetEgiCmp());
}
```

---

### Step 8: Remove Proxy Methods from Manager Classes

Delete proxy setter methods from manager classes that were used for hierarchical delegation:

**Old EgiMgrCls (Remove These):**
```cpp
// OLD - Delete these proxy methods
void SetItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc);
EgiExtDataIfc* GetItsEgiCmpRadaltInPortRadaltExtDataIfc();
```

**New EgiMgrCls:**
```cpp
// Only keep accessors - no proxy methods needed
EgiLruMgrCls& GetEgiLruMgr() { return EgiLruMgr; }
EgiCmpCls& GetEgiCmp() { return EgiCmp; }
```

---

## Complete Example: Before and After

### Before (Old Pattern)

**EgiLruMgrCls.h:**
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

**EgiLruMgrCls.cpp:**
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

**EgiMgrCls.cpp:**
```cpp
void EgiMgrCls::SetItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc)
{
    EgiLruMgr.setItsDataOutPortEgiExtDataIfc(ifc);
}
```

**PartitionCls.cpp:**
```cpp
void PartitionCls::InitRelations()
{
    EgiMgr.SetItsDataOutPortEgiExtDataIfc(
        RadaltMgr.GetItsRadaltEgiInPortEgiExtDataIfc()
    );
}
```

### After (New Pattern)

**EgiLruMgrCls.h:**
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

**EgiLruMgrCls.cpp:**
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

**EgiMgrCls.h:**
```cpp
class EgiMgrCls
{
public:
    EgiLruMgrCls& GetEgiLruMgr() { return EgiLruMgr; }
    // No proxy setter methods needed!

private:
    EgiLruMgrCls EgiLruMgr;
};
```

**PartitionCls.cpp:**
```cpp
void PartitionCls::InitRelations()
{
    // Direct wiring with implicit upcasting
    EgiMgr.GetEgiLruMgr().SetEgiOut(&RadaltMgr.GetRadaltLruMgr());
}
```

---

## Migration Checklist

### Per Class:
- [ ] Remove `#include <PortMacros.h>`
- [ ] Rename `Its*Port*Ifc` members to `m_*Out`
- [ ] Rename `Set*Its*Port*()` to `Set*Out()`
- [ ] Replace `OUT_PORT(...)` calls with `m_*Out->`
- [ ] Add null checks before port calls
- [ ] Remove `Get*In()` methods that return `this`
- [ ] Initialize port members to `nullptr` in declaration

### Per Manager Class:
- [ ] Add `Get*LruMgr()` accessors for sub-components
- [ ] Add `Get*Cmp()` accessors for components
- [ ] Remove proxy setter methods

### Per PartitionCls:
- [ ] Update `InitRelations()` to use direct wiring
- [ ] Use `Manager.GetLruMgr().SetOut(&OtherManager.GetLruMgr())`
- [ ] Remove calls to proxy methods

### Project-wide:
- [ ] Delete `PortMacros.h`
- [ ] Update tests to use new method names
- [ ] Verify all tests pass

---

## Benefits of the New Pattern

1. **~80% shorter names**: `m_egiOut` vs `ItsDataOutPortEgiExtDataIfc`
2. **No macros**: Direct, readable code
3. **No boilerplate**: No proxy methods or `GetXxxIn()` returns
4. **Type-safe**: C++ compiler handles implicit upcasting
5. **Flat wiring**: Clear, direct port connections in one place
6. **Null-safe**: Explicit null checks prevent crashes
