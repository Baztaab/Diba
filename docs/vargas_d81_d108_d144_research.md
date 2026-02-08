# PyJHora Research — D81/D108/D144

This document extracts rules from PyJHora code only (no JHora UI/Java logic).

## Summary Table

| Chart | Methods | Default method | Source file/functions | Notes |
| --- | --- | --- | --- | --- |
| D81 (Nava Navamsa) | 1..3 (4 in code) | 1 | `docs/jhora/horoscope/chart/charts.py`: `nava_navamsa_chart` | Method 4 exists in code but UI exposes only 1..3 via `varga_option_dict[81] = (3,1)` |
| D108 (Ashtotharamsa) | 1..4 | 1 | `docs/jhora/horoscope/chart/charts.py`: `ashtotharamsa_chart` | Method 1 is mixed D9(m1) → D12(m1) |
| D144 (Dwadas Dwadasamsa) | 1..4 | 1 | `docs/jhora/horoscope/chart/charts.py`: `dwadas_dwadasamsa_chart` | Method 1 is mixed D12(m1) → D12(m1) |

Default method source: `docs/jhora/const.py` → `varga_option_dict`
- D81: `(3, 1)`
- D108: `(4, 1)`
- D144: `(4, 1)`

---

## D81 — Nava Navamsa

**Source**: `docs/jhora/horoscope/chart/charts.py:nava_navamsa_chart`

### Methods
1. **Traditional Parasara** (Parivritti Cyclic)
2. **Parivritti Even Reverse**
3. **Parivritti Alternate (Somanatha)**
4. **Kalachakra nava navamsa** (implemented in code, *not* exposed in UI; `varga_option_dict[81] = (3,1)`)

### Pseudo-code
```
dvf = 81
f1 = 30.0 / dvf

if method == 1:
  return parivritti_cyclic(dvf)
elif method == 2:
  return parivritti_even_reverse(dvf)
elif method == 3:
  return parivritti_alternate(dvf)
else:  # method 4
  pp1 = navamsa_kalachakra(dvf=9)
  pp2 = navamsa_kalachakra(pp1, dvf=9)
  return pp2
```

### Boundary behavior
- `seg = int(long // f1)` (floor)
- `d_long = (long * dvf) % 30`
- No clamp in PyJHora

### Sanity asserts (method 1)
Segment size `30/81 ≈ 0.37037°`
- Aries 0° → Aries
- Taurus 0° → Taurus
- Aries 0.37037° → Taurus (seg = 1)
- Aries 29.999° → Pisces (seg = 80 → 11)

---

## D108 — Ashtotharamsa

**Source**: `docs/jhora/horoscope/chart/charts.py:ashtotharamsa_chart`

### Methods
1. **Traditional Parasara** (mixed chart: D9(m1) → D12(m1))
2. **Parivritti Cyclic**
3. **Parivritti Even Reverse**
4. **Parivritti Alternate (Somanatha)**

### Pseudo-code
```
dvf = 108
f1 = 30.0 / dvf

if method == 2:
  return parivritti_cyclic(dvf)
elif method == 3:
  return parivritti_even_reverse(dvf)
elif method == 4:
  return parivritti_alternate(dvf)
else:  # method 1
  # mixed chart: D9(m1) then D12(m1)
  return mixed_chart(dvf_1=9, method_1=1, dvf_2=12, method_2=1)
```

### Boundary behavior
- `seg = int(long // f1)` (floor)
- `d_long = (long * dvf) % 30`
- No clamp in PyJHora

### Sanity asserts (method 1)
- Aries 0° → Aries
- Taurus 0° → Capricorn (D9 seed earth = Capricorn, then D12 from sign)
- Aries 30/108° (first boundary) → Taurus
- Aries 29.999° → Pisces (last segment)

---

## D144 — Dwadas Dwadasamsa

**Source**: `docs/jhora/horoscope/chart/charts.py:dwadas_dwadasamsa_chart`

### Methods
1. **Traditional Parasara** (mixed chart: D12(m1) → D12(m1))
2. **Parivritti Cyclic**
3. **Parivritti Even Reverse**
4. **Parivritti Alternate (Somanatha)**

### Pseudo-code
```
dvf = 144
f1 = 30.0 / dvf

if method == 2:
  return parivritti_cyclic(dvf)
elif method == 3:
  return parivritti_even_reverse(dvf)
elif method == 4:
  return parivritti_alternate(dvf)
else:  # method 1
  # mixed chart: D12(m1) then D12(m1)
  return mixed_chart(dvf_1=12, method_1=1, dvf_2=12, method_2=1)
```

### Boundary behavior
- `seg = int(long // f1)` (floor)
- `d_long = (long * dvf) % 30`
- No clamp in PyJHora

### Sanity asserts (method 1)
- Aries 0° → Aries
- Taurus 0° → Taurus (D12 from sign twice)
- Aries 30/144° (first boundary) → Taurus
- Aries 29.999° → Pisces (last segment)

---

## Notes

- D81 exposes only methods 1..3 via `varga_option_dict[81] = (3,1)`; method 4 exists but is hidden in UI.
- All methods use floor segmentation with normalized longitudes; PyJHora does not clamp `seg == dvf`.
