# PyJHora Doc vs Code Audit — D7/D8/D9

Scope: `docs/jhora/horoscope/chart/charts.py` and `docs/jhora/panchanga/drik.py` compared against `docs/vargas_d7_d8_d9_research.md`.

## Files checked
- `docs/jhora/horoscope/chart/charts.py`
  - `saptamsa_chart`
  - `ashtamsa_chart`
  - `navamsa_chart`
  - `_navamsa_kalachakra`
- `docs/jhora/panchanga/drik.py`
  - `nakshatra_pada`
- `docs/jhora/const.py`
  - `varga_option_dict`

## Mismatches (doc vs code)

### 1) D9 navamsa_dict tuple order
**Code (navamsa_chart):**
```python
navamsa_dict = {0:(1,const.fire_signs),3:(1,const.water_signs),6:(1,const.air_signs),9:(1,const.earth_signs)}
# ...
r = [(seed+dirn*l)%12 for seed,(dirn,sign_list) in navamsa_dict.items() if sign in sign_list][0]
```
Tuple order is **(dirn, sign_list)**, and comprehension unpacks as `(dirn, sign_list)`.

**Doc (docs/vargas_d7_d8_d9_research.md):** currently shows **(sign_list, dirn)** and unpacks `(sign_list, dirn)`.

**Status:** mismatch.

### 2) D9 navamsa_dict unpacking line
**Code:** `for seed,(dirn,sign_list) in navamsa_dict.items()`

**Doc:** `seed, (sign_list, dirn) = ...`

**Status:** mismatch (needs to reflect code ordering).

## D7/D8 verification status (no mismatch)
- **D7**: methods 1–3 even-sign direction rules match code; methods 4–6 wrap parivritti helpers correctly.
- **D8**: method 1 movable/fixed/dual offsets match code; methods 2–4 wrap parivritti helpers correctly.
- **Kalachakra**: `drik.nakshatra_pada` returns `[nakshatra, pada, remainder]` and `_navamsa_kalachakra` indexes `nak-1`, `pada-1` (doc already reflects this).

## Proposed patch (doc-only)
Apply the following changes to **`docs/vargas_d7_d8_d9_research.md`**:

```diff
@@
-navamsa_dict = {
-  0: (fire_signs,  1),
-  3: (water_signs, 1),
-  6: (air_signs,   1),
-  9: (earth_signs, 1),
-}
+navamsa_dict = {
+  0: (1, fire_signs),
+  3: (1, water_signs),
+  6: (1, air_signs),
+  9: (1, earth_signs),
+}
 if method == 4:
-  navamsa_dict = {
-    0: (fire_signs,  1),
-    3: (water_signs, -1),
-    6: (air_signs,   1),
-    9: (earth_signs, -1),
-  }
+  navamsa_dict = {
+    0: (1, fire_signs),
+    3: (-1, water_signs),
+    6: (1, air_signs),
+    9: (-1, earth_signs),
+  }
@@
-seed, (sign_list, dirn) = (seed, tuple) where sign ∈ sign_list
+seed, (dirn, sign_list) = (seed, tuple) where sign ∈ sign_list
```

Notes:
- This aligns the doc with the actual tuple ordering and unpacking in `navamsa_chart`.
- No code change required.
