# PyJHora Research — D24/D27/D30/D40/D45

This document extracts rules from PyJHora code only (no JHora UI/Java logic).

## Summary Table

| Chart | Methods | Default method | Source file/functions | Notes |
| --- | --- | --- | --- | --- |
| D24 (Chaturvimsamsa / Siddhamsa) | 1..3 | 1 | `docs/jhora/horoscope/chart/charts.py`: `chaturvimsamsa_chart` | Method count matches `varga_option_dict[24]=(3,1)` |
| D27 (Nakshatramsa) | 1..3 | 1 | `docs/jhora/horoscope/chart/charts.py`: `nakshatramsa_chart` | `varga_option_dict[27]=(4,1)` but charts.py implements only 3 methods |
| D30 (Trimsamsa) | 1..5 | 1 | `docs/jhora/horoscope/chart/charts.py`: `trimsamsa_chart` | Method 1 uses uneven segments per sign parity |
| D40 (Khavedamsa) | 1..4 | 1 | `docs/jhora/horoscope/chart/charts.py`: `khavedamsa_chart` | Traditional method uses even-sign offset +6 |
| D45 (Akshavedamsa) | 1..4 | 1 | `docs/jhora/horoscope/chart/charts.py`: `akshavedamsa_chart` | Traditional method uses movable/fixed/dual offsets |

Default method source: `docs/jhora/const.py` → `varga_option_dict`
- D24: `(3, 1)`
- D27: `(4, 1)`
- D30: `(5, 1)`
- D40: `(4, 1)`
- D45: `(4, 1)`

Boundary behavior (PyJHora):
- `seg = int(long // f1)` (floor)
- `d_long = (long * dvf) % 30`
- No clamp
- D30 method1 uses explicit ranges and `<=` for both bounds

---

## D24 — Chaturvimsamsa (Siddhamsa)

**Source**: `docs/jhora/horoscope/chart/charts.py:chaturvimsamsa_chart`

### Methods
1. Traditional Parasara Siddhamsa (odd: Leo start, even: Cancer start)
2. Parasara with even sign reversal (odd: Leo forward, even: Cancer backward)
3. Parasara with even sign double reversal (odd: Leo forward, even: Leo forward)

### Pseudo-code
```
dvf = 24
f1 = 30 / dvf
odd_base = 4   # Leo
even_base = 4 if method == 3 else 3  # Leo or Cancer
even_dirn = -1 if method == 2 else 1

for each (sign, long):
    d_long = (long * dvf) % 30
    seg = int(long // f1)
    r = (odd_base + seg) % 12
    if sign in even_signs:
        r = (even_base + even_dirn * seg) % 12
```

### Sanity asserts (method 1)
- Aries 0° → Leo (sign_num=4)
- Taurus 0° → Cancer (sign_num=3)
- Aries 1.25° → Virgo (sign_num=5)
- Aries 29.999° → Cancer (sign_num=3)

---

## D27 — Nakshatramsa

**Source**: `docs/jhora/horoscope/chart/charts.py:nakshatramsa_chart`

### Methods
1. Traditional Parasara (element-based)
2. Parivritti even reversal
3. Parivritti alternate (Somanatha)

**Note**: `varga_option_dict[27]=(4,1)` but charts.py only implements methods 1..3.

### Pseudo-code (method 1)
```
dvf = 27
f1 = 30 / dvf

for each (sign, long):
    d_long = (long * dvf) % 30
    seg = int(long // f1)
    r = seg % 12              # fire signs
    if sign in earth_signs:
        r = (seg + 3) % 12
    elif sign in air_signs:
        r = (seg + 6) % 12
    elif sign in water_signs:
        r = (seg + 9) % 12
```

### Sanity asserts (method 1)
- Aries 0° → Aries (sign_num=0)
- Taurus 0° → Cancer (sign_num=3)
- Aries 1.1111° → Taurus (sign_num=1)
- Aries 29.999° → Gemini (sign_num=2)

---

## D30 — Trimsamsa

**Source**: `docs/jhora/horoscope/chart/charts.py:trimsamsa_chart`

### Methods
1. Traditional Parasara (uneven segments by sign parity)
2. Parivritti cyclic
3. Shastyamsa-like (r = seg + sign)
4. Parivritti even reverse
5. Parivritti alternate (Somanatha)

### Method 1 segment tables
Odd signs:
- 0–5 → Aries
- 5–10 → Aquarius
- 10–18 → Sagittarius
- 18–25 → Gemini
- 25–30 → Libra

Even signs:
- 0–5 → Taurus
- 5–12 → Virgo
- 12–20 → Pisces
- 20–25 → Capricorn
- 25–30 → Scorpio

### Pseudo-code (method 1)
```
dvf = 30

odd = [(0,5,0),(5,10,10),(10,18,8),(18,25,2),(25,30,6)]
even = [(0,5,1),(5,12,5),(12,20,11),(20,25,9),(25,30,7)]

for each (sign, long):
    d_long = (long * dvf) % 30
    table = odd if sign in odd_signs else even
    r = first rasi where l_min <= long <= l_max
```

### Sanity asserts (method 1)
- Aries 0° → Aries (sign_num=0)
- Taurus 0° → Taurus (sign_num=1)
- Aries 5° → Aries (sign_num=0)  # inclusive boundary
- Aries 29.999° → Libra (sign_num=6)

---

## D40 — Khavedamsa

**Source**: `docs/jhora/horoscope/chart/charts.py:khavedamsa_chart`

### Methods
1. Traditional Parasara
2. Parivritti cyclic
3. Parivritti even reverse
4. Parivritti alternate (Somanatha)

### Pseudo-code (method 1)
```
dvf = 40
f1 = 30 / dvf

for each (sign, long):
    d_long = (long * dvf) % 30
    seg = int(long // f1)
    r = seg % 12
    if sign in even_signs:
        r = (seg + 6) % 12
```

### Sanity asserts (method 1)
- Aries 0° → Aries (sign_num=0)
- Taurus 0° → Libra (sign_num=6)
- Aries 0.75° → Taurus (sign_num=1)
- Aries 29.999° → Cancer (sign_num=3)

---

## D45 — Akshavedamsa

**Source**: `docs/jhora/horoscope/chart/charts.py:akshavedamsa_chart`

### Methods
1. Traditional Parasara
2. Parivritti cyclic
3. Parivritti even reverse
4. Parivritti alternate (Somanatha)

### Pseudo-code (method 1)
```
dvf = 45
f1 = 30 / dvf

for each (sign, long):
    d_long = (long * dvf) % 30
    seg = int(long // f1)
    r = seg % 12
    if sign in fixed_signs:
        r = (seg + 4) % 12
    elif sign in dual_signs:
        r = (seg + 8) % 12
```

### Sanity asserts (method 1)
- Aries 0° → Aries (sign_num=0)
- Taurus 0° → Leo (sign_num=4)
- Aries 0.6667° → Taurus (sign_num=1)
- Aries 29.999° → Sagittarius (sign_num=8)

---

## Implementation checklist
- Use defaults from `const.varga_option_dict` (fallback=1).
- Keep `d_long = (long * dvf) % 30` and `seg = int(long // f1)` (no clamp).
- Use PyJHora parivritti helpers where indicated.
- Note D27 method count mismatch in docs (const vs charts.py).
