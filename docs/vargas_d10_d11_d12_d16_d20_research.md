# PyJHora Research — D10/D11/D12/D16/D20

This document extracts rules from PyJHora code only (no JHora UI/Java logic).

## Summary Table

| Chart | Methods | Default method | Source file/functions | Notes |
| --- | --- | --- | --- | --- |
| D10 (Dasamsa) | 1..6 | 1 | `docs/jhora/horoscope/chart/charts.py`: `dasamsa_chart` | Methods 4–6 use parivritti helpers |
| D11 (Rudramsa / Ekadasamsa) | 1..5 | 1 | `docs/jhora/horoscope/chart/charts.py`: `rudramsa_chart` | Method 2 is BV Raman anti‑zodiacal |
| D12 (Dwadasamsa) | 1..5 | 1 | `docs/jhora/horoscope/chart/charts.py`: `dwadasamsa_chart` | Method 2 flips even‑sign direction |
| D16 (Shodasamsa / Kalamsa) | 1..4 | 1 | `docs/jhora/horoscope/chart/charts.py`: `shodasamsa_chart` | Method 2 uses parivritti even‑reverse |
| D20 (Vimsamsa) | 1..4 | 1 | `docs/jhora/horoscope/chart/charts.py`: `vimsamsa_chart` | Method 2 uses parivritti even‑reverse |

Default method source: `docs/jhora/const.py` → `varga_option_dict`
- D10: `(6, 1)`
- D11: `(5, 1)`
- D12: `(5, 1)`
- D16: `(4, 1)`
- D20: `(4, 1)`

Boundary behavior (all):
- `seg = int(long // f1)` with `f1 = 30/dvf` (floor)
- `d_long = (long * dvf) % 30`
- No clamp in PyJHora

---

## D10 — Dasamsa

**Source**: `docs/jhora/horoscope/chart/charts.py:dasamsa_chart`  
**Helpers**: `__parivritti_cyclic`, `__parivritti_even_reverse`, `__parivritti_alternate`

### Methods
1. **Traditional Parasara (even start from 9th and go forward)**
2. **Parasara even signs (start from 9th and go backward)**
3. **Parasara even signs (start from reverse 9th and go backward)**
4. **Parivritti Cyclic (Ojha)**
5. **Parivritti Even Reverse**
6. **Parivritti Alternate (Somanatha)**

### Method 1–3 (Parasara variants) — Algorithm
```
dvf = 10
f1 = 30.0 / dvf
dirn = -1 if method in [2,3] else 1
for each (sign, long):
    d_long = (long * dvf) % 30
    l = int(long // f1)
    r = (sign + l) % 12
    if sign in const.even_signs:
        r = (sign + dirn * (l + 8)) % 12
        if method == 2:
            r = (r - 8) % 12
    output (r, d_long)
```

### Method 4–6 (Parivritti wrappers)
- **4** → `__parivritti_cyclic(..., dvf=10)`
- **5** → `__parivritti_even_reverse(..., dvf=10)`
- **6** → `__parivritti_alternate(..., dvf=10)`

### Sanity asserts (method 1)
Segment size `30/10 = 3.0`.
- Aries 0° → Aries
- Taurus 0° → Capricorn
- Aries 3.0° (boundary) → Taurus
- Aries 29.999° → Capricorn

---

## D11 — Rudramsa (Ekadasamsa)

**Source**: `docs/jhora/horoscope/chart/charts.py:rudramsa_chart`  
**Helpers**: `__parivritti_cyclic`, `__parivritti_even_reverse`, `__parivritti_alternate`

### Methods
1. **Traditional Parasara (Sanjay Rath)**
2. **BV Raman (Ekadasamsa – Anti‑zodiacal)**
3. **Parivritti Cyclic**
4. **Parivritti Even Reverse**
5. **Parivritti Alternate (Somanatha)**

### Method 1–2 — Algorithm
```
dvf = 11
f1 = 30.0 / dvf
for each (sign, long):
    d_long = (long * dvf) % 30
    l = int(long // f1)
    r = (12 - sign + l) % 12
    if method == 2:
        r = (11 - r) % 12
    output (r, d_long)
```

### Method 3–5 (Parivritti wrappers)
- **3** → `__parivritti_cyclic(..., dvf=11)`
- **4** → `__parivritti_even_reverse(..., dvf=11)`
- **5** → `__parivritti_alternate(..., dvf=11)`

### Sanity asserts (method 1)
Segment size `30/11 ≈ 2.72727`.
- Aries 0° → Aries
- Taurus 0° → Pisces
- Aries 2.72727° (boundary) → Taurus
- Aries 29.999° → Aquarius

---

## D12 — Dwadasamsa

**Source**: `docs/jhora/horoscope/chart/charts.py:dwadasamsa_chart`  
**Helpers**: `__parivritti_cyclic`, `__parivritti_even_reverse`, `__parivritti_alternate`

### Methods
1. **Traditional Parasara**
2. **Traditional Parasara with even sign reversal**
3. **Parivritti Cyclic**
4. **Parivritti Even Reverse**
5. **Parivritti Alternate (Somanatha)**

### Method 1–2 — Algorithm
```
dvf = 12
f1 = 30.0 / dvf
for each (sign, long):
    d_long = (long * dvf) % 30
    l = int(long // f1)
    dirn = -1 if (sign in const.even_signs and method == 2) else 1
    r = (sign + dirn * l) % 12
    output (r, d_long)
```

### Method 3–5 (Parivritti wrappers)
- **3** → `__parivritti_cyclic(..., dvf=12)`
- **4** → `__parivritti_even_reverse(..., dvf=12)`
- **5** → `__parivritti_alternate(..., dvf=12)`

### Sanity asserts (method 1)
Segment size `30/12 = 2.5`.
- Aries 0° → Aries
- Taurus 0° → Taurus
- Aries 2.5° (boundary) → Taurus
- Aries 29.999° → Pisces

---

## D16 — Shodasamsa (Kalamsa)

**Source**: `docs/jhora/horoscope/chart/charts.py:shodasamsa_chart`  
**Helpers**: `__parivritti_cyclic`, `__parivritti_even_reverse`, `__parivritti_alternate`

### Methods
1. **Traditional Parasara**
2. **Parivritti Even Reverse**
3. **Parivritti Cyclic**
4. **Parivritti Alternate (Somanatha)**

### Method 1 — Algorithm
```
dvf = 16
f1 = 30.0 / dvf
for each (sign, long):
    d_long = (long * dvf) % 30
    l = int(long // f1)
    r = l % 12            # movable
    if sign in const.fixed_signs:
        r = (l + 4) % 12
    elif sign in const.dual_signs:
        r = (l + 8) % 12
    output (r, d_long)
```

### Method 2–4 (Parivritti wrappers)
- **2** → `__parivritti_even_reverse(..., dvf=16)`
- **3** → `__parivritti_cyclic(..., dvf=16)`
- **4** → `__parivritti_alternate(..., dvf=16)`

### Sanity asserts (method 1)
Segment size `30/16 = 1.875`.
- Aries 0° → Aries
- Taurus 0° → Leo
- Aries 1.875° (boundary) → Taurus
- Aries 29.999° → Cancer

---

## D20 — Vimsamsa

**Source**: `docs/jhora/horoscope/chart/charts.py:vimsamsa_chart`  
**Helpers**: `__parivritti_cyclic`, `__parivritti_even_reverse`, `__parivritti_alternate`

### Methods
1. **Traditional Parasara**
2. **Parivritti Even Reverse**
3. **Parivritti Cyclic**
4. **Parivritti Alternate (Somanatha)**

### Method 1 — Algorithm
```
dvf = 20
f1 = 30.0 / dvf
for each (sign, long):
    d_long = (long * dvf) % 30
    l = int(long // f1)
    r = l % 12            # movable
    if sign in const.dual_signs:
        r = (l + 4) % 12
    elif sign in const.fixed_signs:
        r = (l + 8) % 12
    output (r, d_long)
```

### Method 2–4 (Parivritti wrappers)
- **2** → `__parivritti_even_reverse(..., dvf=20)`
- **3** → `__parivritti_cyclic(..., dvf=20)`
- **4** → `__parivritti_alternate(..., dvf=20)`

### Sanity asserts (method 1)
Segment size `30/20 = 1.5`.
- Aries 0° → Aries
- Taurus 0° → Sagittarius
- Aries 1.5° (boundary) → Taurus
- Aries 29.999° → Scorpio

---

## Implementation checklist
- Use PyJHora `varga_option_dict` defaults (fallback=1 if missing).
- Keep `d_long = (long * dvf) % 30` and `seg = int(long // f1)`.
- Mirror scope unchanged (only D2/D3/D7 in `jhora_us`).
