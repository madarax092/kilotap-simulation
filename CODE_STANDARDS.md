# KiloTap Simulation — Code Standards

## Core Rules

### 1. DRY — Don't Repeat Yourself
- DOM elements queried more than once: cache to variable
- Repeated color values: extract to CSS variables or constants
- Same logic in multiple places: extract to function

### 2. KISS — Keep It Simple
- Functions < 30 lines (break long ones)
- One function = one responsibility
- No nested ternaries
- No `try/catch` swallowing errors silently

### 3. Readable First
- Descriptive variable names (not `cm`, `hPos`, `e`)
- Comments explain WHY, not WHAT
- Consistent indentation
- Group related code with section headers

### 4. No Dead Code
- No commented-out code
- No unused variables
- No unreachable paths

### 5. Performance
- Cache DOM queries
- Avoid repeated calculations in loops
- Dispose tensors after use (memory leaks)

## Architecture Patterns

### DOM Cache (ALWAYS at top)
```javascript
const $ = (id) => document.getElementById(id);
const els = {
  yoloBadge: $('yolo-badge'),
  dashOmega: $('dash-omega'),
  // ... all used elements
};
```

### Constants (ALWAYS grouped at top)
```javascript
const CONFIG = {
  DAVAO_CENTER: [7.071, 125.613],
  EARTH_RADIUS_KM: 6371,
  CANVAS_WIDTH: 700,
  CANVAS_HEIGHT: 933,
  CONFIDENCE_THRESHOLD: 0.5,
  DEFAULT_TAU: 0.4,
};
```

### Systems Stay Decoupled (NON-NEGOTIABLE)
- YOLO panel: sets `currentVehicle`
- Map panel: reads `currentVehicle` via setInterval
- Dashboard: updated by YOLO only
- NO cross-calls between systems

## Pre-Commit Checklist
```bash
# Before ANY commit:
cd /root/kilotap-simulation
bash test/validate.sh          # 14 automated checks
grep -c 'var ' index.html      # should be 0
grep -c '// TODO' index.html   # should be 0  
grep -c 'console.log' index.html # should be 0
```
