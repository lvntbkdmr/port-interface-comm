# Migrate Port Wiring

Update PartitionCls to use direct port wiring instead of hierarchical delegation.

## Usage

```
/migrate-wiring
```

## Instructions

This skill updates `PartitionCls::InitRelations()` to wire ports directly to LRU managers instead of through manager hierarchy.

### Step 1: Read current files

Read these files:
- `PartitionPkg/inc/PartitionCls.h`
- `PartitionPkg/src/PartitionCls.cpp`

### Step 2: Identify old wiring patterns

Look for patterns like:
```cpp
// OLD - wiring through manager with getter methods
EgiMgr.SetItsDataOutPortEgiExtDataIfc(
    RadaltMgr.GetItsRadaltEgiInPortEgiExtDataIfc()
);
```

### Step 3: Ensure manager accessors exist

Verify that manager classes have accessor methods. If not, they need to be added first using `/migrate-port`.

Required accessors:
- `EgiMgrCls::GetEgiLruMgr()` - returns `EgiLruMgrCls&`
- `EgiMgrCls::GetEgiCmp()` - returns `EgiCmpCls&`
- `RadaltMgrCls::GetRadaltLruMgr()` - returns `RadaltLruMgrCls&`
- `VorIlsMgrCls::GetVorIlsLruMgr()` - returns `VorIlsLruMgrCls&`

### Step 4: Convert to direct wiring

Transform each port connection:

**Old Pattern:**
```cpp
void PartitionCls::InitRelations()
{
    // Wiring through manager proxy methods
    EgiMgr.SetItsDataOutPortEgiExtDataIfc(
        RadaltMgr.GetItsRadaltEgiInPortEgiExtDataIfc()
    );
    RadaltMgr.SetItsDataOutPortRadaltExtDataIfc(
        EgiMgr.GetItsEgiCmpRadaltInPortRadaltExtDataIfc()
    );
}
```

**New Pattern:**
```cpp
void PartitionCls::InitRelations()
{
    // EgiLruMgr sends EGI external data to RadaltLruMgr
    EgiMgr.GetEgiLruMgr().SetEgiOut(&RadaltMgr.GetRadaltLruMgr());

    // RadaltLruMgr sends radar altimeter data to EgiCmp
    RadaltMgr.GetRadaltLruMgr().SetRadaltOut(&EgiMgr.GetEgiCmp());
}
```

### Step 5: Apply wiring rules

For each data flow, use this pattern:
```cpp
<SourceManager>.Get<SourceComponent>().Set<DataName>Out(&<DestManager>.Get<DestComponent>());
```

**Key points:**
- Use `&` to get address of destination (implicit upcast to interface)
- Call setter directly on the component that owns the port
- Add comment describing the data flow

### Step 6: Common wiring patterns

| Data Flow | Wiring Code |
|-----------|-------------|
| EgiLruMgr → RadaltLruMgr | `EgiMgr.GetEgiLruMgr().SetEgiOut(&RadaltMgr.GetRadaltLruMgr())` |
| RadaltLruMgr → EgiCmp | `RadaltMgr.GetRadaltLruMgr().SetRadaltOut(&EgiMgr.GetEgiCmp())` |
| EgiLruMgr → EgiCmp (command) | `EgiMgr.GetEgiLruMgr().SetCommandOut(&EgiMgr.GetEgiCmp())` |
| EgiCmp → VorIlsLruMgr | `EgiMgr.GetEgiCmp().SetVorIlsOut(&VorIlsMgr.GetVorIlsLruMgr())` |

### Step 7: Internal wiring (within same manager)

Some wiring happens inside manager classes, not in PartitionCls:

**EgiMgrCls::InitRelations():**
```cpp
void EgiMgrCls::InitRelations()
{
    // Internal wiring: EgiLruMgr sends commands to EgiCmp
    EgiLruMgr.SetCommandOut(&EgiCmp);
}
```

### Step 8: Remove proxy methods from managers

After updating wiring, remove unused proxy methods from manager classes:
- `EgiMgrCls::SetItsDataOutPortEgiExtDataIfc()`
- `RadaltMgrCls::SetItsDataOutPortRadaltExtDataIfc()`
- Any `Get*In*Port*()` methods

### Step 9: Verify compilation

```bash
cmake --build build
```

### Step 10: Run integration tests

```bash
ctest -R IntegrationTest
```

## Example Complete InitRelations

```cpp
// PartitionCls.cpp
void PartitionCls::InitRelations()
{
    // EgiLruMgr sends EGI external data to RadaltLruMgr
    EgiMgr.GetEgiLruMgr().SetEgiOut(&RadaltMgr.GetRadaltLruMgr());

    // RadaltLruMgr sends radar altimeter data to EgiCmp
    RadaltMgr.GetRadaltLruMgr().SetRadaltOut(&EgiMgr.GetEgiCmp());

    // EgiCmp sends VOR/ILS navigation data to VorIlsLruMgr
    EgiMgr.GetEgiCmp().SetVorIlsOut(&VorIlsMgr.GetVorIlsLruMgr());
}
```

## Output

After successful migration, report:
1. Old wiring patterns removed
2. New direct wiring applied
3. Proxy methods removed from managers
4. Compilation status
5. Integration test results
