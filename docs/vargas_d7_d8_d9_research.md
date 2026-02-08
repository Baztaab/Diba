# PyJHora Research — D7/D8/D9

This document extracts rules from PyJHora code only (no JHora UI/Java logic).

## Summary Table

| Chart | Methods | Default method | Source file/functions | Notes |
| --- | --- | --- | --- | --- |
| D7 (Saptamsa) | 1..6 | 1 | `docs/jhora/horoscope/chart/charts.py`: `saptamsa_chart` | Methods 4–6 use parivritti helpers in `docs/jhora/utils.py` |
| D8 (Ashtamsa) | 1..4 | 1 | `docs/jhora/horoscope/chart/charts.py`: `ashtamsa_chart` | Methods 2–4 use parivritti helpers |
| D9 (Navamsa) | 1..6 | 1 | `docs/jhora/horoscope/chart/charts.py`: `navamsa_chart`, `_navamsa_kalachakra` | Method 3 depends on `drik.nakshatra_pada` + `const.kalachakra_navamsa` |

Default method source: `docs/jhora/const.py` → `varga_option_dict`  
- D7: `(6, 1)`  
- D8: `(4, 1)`  
- D9: `(5, 1)`

### Verification (varga_option_dict vs chart methods)
- D7 has 6 methods in `saptamsa_chart` and `varga_option_dict[7] = (6,1)` → fully represented in UI.  
- D8 has 4 methods in `ashtamsa_chart` and `varga_option_dict[8] = (4,1)` → fully represented in UI.  
- D9 has 6 methods in `navamsa_chart` but `varga_option_dict[9] = (5,1)` → UI exposes only 5 methods.  
  Based on the chart method list, **method 6 (Parivritti Alternate / Somanatha)** is not exposed by the UI profile count.  
  Reason: UI uses `varga_option_dict[dcf][0]` as method count (see `docs/jhora/ui/varga_chart_dialog.py`), so method 6 is hidden even though implemented.

---

## D7 — Saptamsa

**Source**: `docs/jhora/horoscope/chart/charts.py:saptamsa_chart`  
**Helpers**: `__parivritti_cyclic`, `__parivritti_even_reverse`, `__parivritti_alternate`  
**Constants**: `const.even_signs` (even signs are `[1,3,5,7,9,11]`).

### Methods
1. **Traditional Parasara (even start from 7th and go forward)**  
2. **Traditional Parasara (even start from 7th and go backward)**  
3. **Traditional Parasara (even reverse but end in 7th)**  
4. **Parivritti Cyclic**  
5. **Parivritti Even Reverse**  
6. **Parivritti Alternate (Somanatha)**  

### Method 1–3 (Parasara variants) — Algorithm
```
dvf = 7
f1 = 30.0 / dvf
dirn = -1 if method in [2,3] else 1
for each (sign, long):
    d_long = (long * dvf) % 30
    l = int(long // f1)
    r = (sign + l) % 12
    if sign in const.even_signs:
        r = (sign + dirn * (l + 6)) % 12
        if method == 3:
            r = (r - 6) % 12
    output (r, d_long)
```

### Method 4–6 (Parivritti wrappers)
- **4** → `__parivritti_cyclic(planet_positions_in_rasi, dvf=7)`
- **5** → `__parivritti_even_reverse(..., dvf=7)`
- **6** → `__parivritti_alternate(..., dvf=7)`

These helpers use `utils.parivritti_cyclic / parivritti_even_reverse / parivritti_alternate` and then map:
```
d_long = (long * dvf) % 30
hora = int(long // (30.0 / dvf))
varga_sign = mapping[rasi_sign][hora]  # (or tuple lookup for even_reverse)
```

### Boundary behavior
- `l = int(long // f1)` (floor); no clamp.
- `d_long = (long * dvf) % 30`.
- Near 30° (e.g., 29.999) falls into the last segment (l = dvf-1).

### Sanity asserts (method 1)
Use segment size `30/7 ≈ 4.285714`.
- Aries 0° → Aries (r=0)
- Taurus 0° → Scorpio (r=(1+6)%12=7)
- Aries 4.2857° (first boundary) → Taurus (l=1 → r=1)
- Aries 29.999° → Libra (l=6 → r=6)

### Notes
Docstring matches code. Method 1–3 only alter **even signs**; odd signs use r = sign + l.

### Implementation checklist (D7)
- Implement methods 1–3 with even-sign logic exactly.
- Wire methods 4–6 to parivritti helpers.
- Use `int(long // f1)` and `(long * dvf) % 30` (no clamp).
- Default method from `const.varga_option_dict[7]`.

---

## D8 — Ashtamsa

**Source**: `docs/jhora/horoscope/chart/charts.py:ashtamsa_chart`  
**Constants**: `const.movable_signs`, `const.fixed_signs`, `const.dual_signs`  
**Helpers**: parivritti wrappers for methods 2–4.

### Methods
1. **Traditional Parasara**  
2. **Parivritti Cyclic**  
3. **Parivritti Even Reverse**  
4. **Parivritti Alternate (Somanatha)**  

### Method 1 (Parasara) — Algorithm
```
dvf = 8
f1 = 30.0 / dvf
for each (sign, long):
    d_long = (long * dvf) % 30
    l = int(long // f1)
    r = l % 12                 # movable signs
    if sign in const.dual_signs:
        r = (l + 4) % 12
    elif sign in const.fixed_signs:
        r = (l + 8) % 12
    output (r, d_long)
```

### Method 2–4 (Parivritti wrappers)
- **2** → `__parivritti_cyclic(..., dvf=8)`
- **3** → `__parivritti_even_reverse(..., dvf=8)`
- **4** → `__parivritti_alternate(..., dvf=8)`

### Boundary behavior
- `l = int(long // (30/8))` (floor); no clamp.
- `d_long = (long * 8) % 30`.

### Sanity asserts (method 1)
Segment size `30/8 = 3.75`.
- Aries 0° (movable) → Aries (r=0)
- Taurus 0° (fixed) → Sagittarius (r=8)
- Gemini 0° (dual) → Leo (r=4)
- Aries 3.75° (boundary) → Taurus (l=1 → r=1)
- Aries 29.999° → Scorpio (l=7 → r=7)

### Notes
Docstring matches code. Method 1 uses sign type (movable/fixed/dual), not odd/even.

### Implementation checklist (D8)
- Implement method1 with movable/fixed/dual offsets (0/+8/+4).
- Wire methods 2–4 to parivritti helpers.
- Use `int(long // f1)` and `(long * dvf) % 30` (no clamp).
- Default method from `const.varga_option_dict[8]`.

---

## D9 — Navamsa

**Source**:  
`docs/jhora/horoscope/chart/charts.py:navamsa_chart`, `_navamsa_kalachakra`  
`docs/jhora/panchanga/drik.py:nakshatra_pada`  
`docs/jhora/const.py:kalachakra_navamsa`  
**Helpers**: parivritti wrappers for methods 2/5/6.

### Methods
1. **Traditional Parasara (element-seed navamsa)**  
2. **Parasara with even sign reversal (Uniform Krishna Mishra Navamsa)**  
3. **Kalachakra Navamsa**  
4. **Rangacharya Krishna Mishra / Sanjay Rath Nadi Navamsa**  
5. **Parivritti Cyclic**  
6. **Parivritti Alternate (Somanatha)**  

### Method 1 & 4 (Element-seed) — Algorithm
Note: In PyJHora, the tuple order in `navamsa_dict` is **(dirn, sign_list)**.
```
dvf = 9
f1 = 30.0 / dvf
navamsa_dict = {
  0: (1, fire_signs),
  3: (1, water_signs),
  6: (1, air_signs),
  9: (1, earth_signs),
}
if method == 4:
  navamsa_dict = {
    0: (1, fire_signs),
    3: (-1, water_signs),
    6: (1, air_signs),
    9: (-1, earth_signs),
  }
for each (sign, long):
    d_long = (long * dvf) % 30
    l = int(long // f1)
    seed, (dirn, sign_list) = (seed, tuple) where sign ∈ sign_list
    r = (seed + dirn * l) % 12
    output (r, d_long)
```

### Method 2/5/6 (Parivritti wrappers)
- **2** → `__parivritti_even_reverse(..., dvf=9)` (Uniform Krishna Mishra)  
- **5** → `__parivritti_cyclic(..., dvf=9)`  
- **6** → `__parivritti_alternate(..., dvf=9)`

**Note:** code comment says method 5 is “same as traditional UKM,” but UKM is method 2 in this file; this is a docstring/comment mismatch.

### Method 3 (Kalachakra) — Algorithm
```
dvf = 9
for each (sign, long):
    d_long = (long * dvf) % 30
    nak, pada, remainder = drik.nakshatra_pada(long + sign*30)
    r = const.kalachakra_navamsa[nak-1][pada-1]
    output (r, d_long)
```

### Boundary behavior
- `l = int(long // (30/9))` (floor); no clamp.
- `d_long = (long * 9) % 30`.

### Sanity asserts (method 1)
Segment size `30/9 = 3.333333...`.
- Aries 0° (fire) → Aries (seed=0, l=0)
- Taurus 0° (earth) → Capricorn (seed=9, l=0)
- Aries 3.3333° (boundary) → Taurus (l=1)
- Aries 29.999° → Sagittarius (l=8)

### Notes
- Method 3 depends on `drik.nakshatra_pada` and `const.kalachakra_navamsa`.
- Method 5 comment is inconsistent with method labels (see note above).

### Implementation Notes (D9)
- `drik.nakshatra_pada(longitude)` returns `[nakshatra_index (1..27), pada (1..4), remainder_deg]`.
- `kalachakra_navamsa` is indexed with `nak-1` and `pada-1` (0-based lookup).
- **Mirror rule does not apply** to D9 (scope remains D2m1/D3m5 only).

### Implementation checklist (D9)
- Implement methods 1/4 via element-seed mapping; method 4 flips direction for water/earth.
- Implement method 3 via `nakshatra_pada` + `kalachakra_navamsa`.
- Wire methods 2/5/6 to parivritti helpers.
- Use `int(long // f1)` and `(long * dvf) % 30` (no clamp).
- Default method from `const.varga_option_dict[9]`.

---

## Implementation checklist (global)
- Use PyJHora `varga_option_dict` for defaults (D7/D8/D9 default=1).
- Keep `d_long = (long * dvf) % 30` in all methods.
- Use floor (`int(long // f1)`), no clamp.
- Parivritti helpers: `docs/jhora/utils.py` (`parivritti_cyclic`, `parivritti_even_reverse`, `parivritti_alternate`).
- Mirror scope stays **only** D2(m1) and D3(m5); do not apply to D7/D8/D9.
