# PyJHora Research — D60 (Shashtyamsa)

This document extracts rules from PyJHora code only (no JHora UI/Java logic).

## Summary

- **Chart:** D60 (Shashtyamsa)
- **Source:** `docs/jhora/horoscope/chart/charts.py:shashtyamsa_chart`
- **Default method:** `docs/jhora/const.py:varga_option_dict[60] = (4, 1)` → default = **1**
- **Dependencies:** `docs/jhora/utils.py` → `__parivritti_alternate` for method 3

## Methods (PyJHora)

From `shashtyamsa_chart(planet_positions_in_rasi, chart_method=1)`:

1. **Traditional Parasara (from sign)**
2. **Parasara Shashtyamsa (from Aries)** — docstring says same as parivritti cyclic from Aries
3. **Parasara even reversal (from Aries)** — **implemented as** `__parivritti_alternate`
4. **Parasara even reversal (from sign)**

### Pseudo-code (common)

```
dvf = 60
f1 = 30.0 / dvf  # 0.5°

for each (planet, [sign, long]):
    d_long = (long * dvf) % 30
    seg = int(long // f1)  # floor
```

### Method 1 — Traditional Parasara (from sign)
```
seed = sign
varga_sign = (seed + seg) % 12
```

### Method 2 — From Aries
```
seed = 0
varga_sign = (seed + seg) % 12
```

### Method 3 — Even reversal (from Aries)
```
return __parivritti_alternate(planet_positions_in_rasi, dvf)
```
**Note:** PyJHora implementation uses `__parivritti_alternate` for method 3.

### Method 4 — Even reversal (from sign)
```
dirn = -1 if (sign in even_signs) else 1
seed = sign
varga_sign = (seed + dirn * seg) % 12
```

## Boundary behavior

- `seg = int(long // f1)` (floor)
- `d_long = (long * dvf) % 30`
- No clamp in PyJHora; `long` is assumed normalized in `[0,30)`
- Near 30° (e.g., 29.999) falls into the last segment (`seg = 59`)

## Sanity asserts (method 1)

Segment size = `0.5°`

- Aries 0° → Aries (sign_num 0)
- Taurus 0° → Taurus (sign_num 1)
- Aries 0.5° → Taurus (seg = 1)
- Aries 29.999° → Pisces (seg = 59 → 11)

## Notes

- Method 3 name suggests even reversal from Aries, but code uses `__parivritti_alternate`. This is a docstring/label mismatch.
- Default method comes from `varga_option_dict`, not function signature.
