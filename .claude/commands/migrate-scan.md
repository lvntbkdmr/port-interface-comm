# Scan for Migration

Scan the codebase to identify classes that need migration from the old port pattern to the new pattern.

## Usage

```
/migrate-scan
```

## Instructions

### Step 1: Search for old pattern indicators

Search for these patterns in the codebase:

**1. PortMacros.h usage:**
```bash
grep -r "PortMacros.h" --include="*.cpp" --include="*.h"
```

**2. OUT_PORT macro calls:**
```bash
grep -r "OUT_PORT(" --include="*.cpp"
```

**3. Old port member naming:**
```bash
grep -r "Its.*Port.*Ifc" --include="*.h"
```

**4. Old setter naming:**
```bash
grep -r "SetIts.*Port\|setIts.*Port" --include="*.h" --include="*.cpp"
```

**5. GetXxxIn methods:**
```bash
grep -r "Get.*In.*Port" --include="*.h"
```

### Step 2: Categorize findings

Group findings into:

1. **Classes with old port members** - Need full migration
2. **Classes using OUT_PORT macro** - Need macro removal
3. **Classes with proxy methods** - Need proxy removal
4. **Wiring code** - Needs flattening

### Step 3: Generate migration plan

Create a migration plan listing:

1. **Priority 1: Core classes with ports**
   - Classes that own output ports
   - Need: member rename, setter rename, macro removal

2. **Priority 2: Manager classes**
   - Classes that delegate port setting
   - Need: add accessors, remove proxy methods

3. **Priority 3: Wiring classes**
   - PartitionCls and any InitRelations()
   - Need: flatten to direct wiring

4. **Priority 4: Tests**
   - Test files referencing old method names
   - Need: update method calls

### Step 4: Output report format

```
## Migration Scan Report

### Files using PortMacros.h:
- [ ] path/to/file.cpp

### Classes with old port members (Its*Port*Ifc):
- [ ] ClassName (file.h:line)
  - ItsDataOutPortEgiExtDataIfc → m_egiOut
  - ItsDataOutPortRadaltExtDataIfc → m_radaltOut

### Classes using OUT_PORT macro:
- [ ] ClassName (file.cpp:line)

### Classes with old setter methods:
- [ ] ClassName::SetItsDataOutPortEgiExtDataIfc()
- [ ] ClassName::setItsDataOutPortEgiExtDataIfc()

### Classes with GetXxxIn methods to remove:
- [ ] ClassName::GetItsRadaltEgiInPortEgiExtDataIfc()

### Manager classes needing accessors:
- [ ] EgiMgrCls - needs GetEgiLruMgr(), GetEgiCmp()
- [ ] RadaltMgrCls - needs GetRadaltLruMgr()

### Wiring to update:
- [ ] PartitionCls::InitRelations()

### Tests to update:
- [ ] test_ClassName.cpp

## Suggested Migration Order:
1. /migrate-port EgiLruMgrCls
2. /migrate-port RadaltLruMgrCls
3. /migrate-port EgiMgrCls
4. /migrate-port RadaltMgrCls
5. /migrate-wiring
```

### Step 5: Check for already migrated code

Also check for new pattern indicators to avoid re-migrating:
- `m_*Out` member naming
- `Set*Out()` setter naming
- Direct accessor methods like `GetEgiLruMgr()`

Mark already-migrated classes as complete in the report.

## Output

Provide a complete migration scan report with:
1. All files/classes needing migration
2. Specific changes needed for each
3. Suggested migration order
4. Already-migrated items (if any)
