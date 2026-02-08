# PyJHora D4/D5/D6 Research (for Kerykeion varga parity)

This document extracts D4/D5/D6 divisional chart rules strictly from the PyJHora codebase included in this repo under `docs/jhora/`.

## Summary

| Chart | Methods (PyJHora) | Default method | Source (file/function) |
| --- | --- | --- | --- |
| D4 Chaturthamsa | 1 Traditional Parasara; 2 Parivritti Cyclic; 3 Parivritti Even Reverse; 4 Parivritti Alternate (Somanatha) | 1 (from `const.varga_option_dict[4] = (4, 1)`) | `docs/jhora/horoscope/chart/charts.py: chaturthamsa_chart, _chaturthamsa_parasara` + `docs/jhora/utils.py: parivritti_*` |
| D5 Panchamsa | 1 Traditional Parasara; 2 Parivritti Cyclic; 3 Parivritti Even Reverse; 4 Parivritti Alternate (Somanatha) | 1 (from `const.varga_option_dict[5] = (4, 1)`) | `docs/jhora/horoscope/chart/charts.py: panchamsa_chart` + `docs/jhora/utils.py: parivritti_*` |
| D6 Shashthamsa | 1 Traditional Parasara; 2 Parivritti Cyclic; 3 Parivritti Even Reverse; 4 Parivritti Alternate (Somanatha) | 1 (from `const.varga_option_dict[6] = (4, 1)`) | `docs/jhora/horoscope/chart/charts.py: shashthamsa_chart` + `docs/jhora/utils.py: parivritti_*` |

Notes on defaults:
- Each chart function has `chart_method=1` in the signature, but the actual app-wide default is read from `const.varga_option_dict`.

## D4 (Chaturthamsa)

Source
- `docs/jhora/horoscope/chart/charts.py`: `_chaturthamsa_parasara`, `chaturthamsa_chart`
- `docs/jhora/utils.py`: `parivritti_cyclic`, `parivritti_even_reverse`, `parivritti_alternate`

Methods (chart_method)
1. Traditional Parasara
2. Parivritti Cyclic
3. Parivritti Even Reverse
4. Parivritti Alternate (aka Somanatha)

Algorithm (Traditional Parasara)
- dvf = 4
- f1 = 30 / dvf = 7.5
- seg = int(long // f1)
- d_long = (long * dvf) % 30
- varga_sign = (rasi_sign + seg * 3) % 12

Algorithm (Parivritti methods)
- dvf = 4
- f1 = 30 / dvf
- seg = int(long // f1)
- d_long = (long * dvf) % 30
- varga_sign = mapping[rasi_sign][seg]
  - mapping comes from `utils.parivritti_cyclic(4)`, `utils.parivritti_even_reverse(4)`, or `utils.parivritti_alternate(4)`

Boundary behavior
- PyJHora uses `int(long // f1)` (floor for non-negative values) and does not clamp.
- Assumes `0 <= long < 30`. Exact `long == 30` would produce `seg == dvf` and would be out of range for the mapping.

Sanity asserts (Traditional Parasara)
- Aries 0.0 deg: seg=0 -> varga_sign = Aries (0), d_long=0
- Aries 7.5 deg: seg=1 -> varga_sign = Cancer (3), d_long = 7.5*4 % 30 = 0
- Aries 15.0 deg: seg=2 -> varga_sign = Libra (6)
- Aries 22.5 deg: seg=3 -> varga_sign = Capricorn (9)
- Taurus 0.0 deg: seg=0 -> varga_sign = Taurus (1)
- Boundary: Aries 29.999 deg -> seg=3 (not 4)

Aries segments table (Traditional Parasara)
| Segment (deg) | Resulting varga sign |
| --- | --- |
| 0.0–7.5 | Aries |
| 7.5–15.0 | Cancer |
| 15.0–22.5 | Libra |
| 22.5–30.0 | Capricorn |

## D5 (Panchamsa)

Source
- `docs/jhora/horoscope/chart/charts.py`: `panchamsa_chart`
- `docs/jhora/utils.py`: `parivritti_*`

Methods (chart_method)
1. Traditional Parasara
2. Parivritti Cyclic
3. Parivritti Even Reverse
4. Parivritti Alternate (aka Somanatha)

Algorithm (Traditional Parasara)
- dvf = 5
- f1 = 30 / dvf = 6
- seg = int(long // f1)
- d_long = (long * dvf) % 30
- if rasi_sign is odd (const.odd_signs): varga_sign = odd[seg]
- else: varga_sign = even[seg]
- odd = [0, 10, 8, 2, 6]
- even = [1, 5, 11, 9, 7]

Odd/Even mapping table (0-based signs)
- seg 0: odd->0 (Aries), even->1 (Taurus)
- seg 1: odd->10 (Aquarius), even->5 (Virgo)
- seg 2: odd->8 (Sagittarius), even->11 (Pisces)
- seg 3: odd->2 (Gemini), even->9 (Capricorn)
- seg 4: odd->6 (Libra), even->7 (Scorpio)

Algorithm (Parivritti methods)
- dvf = 5
- f1 = 30 / dvf
- seg = int(long // f1)
- d_long = (long * dvf) % 30
- varga_sign = mapping[rasi_sign][seg] (from utils.parivritti_* with dvf=5)

Boundary behavior
- Uses `int(long // f1)`; assumes `0 <= long < 30`.

Sanity asserts (Traditional Parasara)
- Aries 0.0 deg -> seg=0 -> varga_sign Aries (0)
- Aries 6.0 deg -> seg=1 -> varga_sign Aquarius (10)
- Aries 7.5 deg -> seg=1 (still Aquarius)
- Taurus 0.0 deg -> seg=0 -> varga_sign Taurus (1)
- Boundary: Aries 29.999 deg -> seg=4

## D6 (Shashthamsa)

Source
- `docs/jhora/horoscope/chart/charts.py`: `shashthamsa_chart`
- `docs/jhora/utils.py`: `parivritti_*`

Methods (chart_method)
1. Traditional Parasara
2. Parivritti Cyclic
3. Parivritti Even Reverse
4. Parivritti Alternate (aka Somanatha)

Algorithm (Traditional Parasara)
- dvf = 6
- f1 = 30 / dvf = 5
- seg = int(long // f1)
- d_long = (long * dvf) % 30
- varga_sign = seg % 12
- if rasi_sign in const.even_signs: varga_sign = (seg + 6) % 12

Algorithm (Parivritti methods)
- dvf = 6
- f1 = 30 / dvf
- seg = int(long // f1)
- d_long = (long * dvf) % 30
- varga_sign = mapping[rasi_sign][seg] (from utils.parivritti_* with dvf=6)

Boundary behavior
- Uses `int(long // f1)`; assumes `0 <= long < 30`.

Sanity asserts (Traditional Parasara)
- Aries 0.0 deg -> seg=0 -> varga_sign Aries (0)
- Aries 5.0 deg -> seg=1 -> varga_sign Taurus (1)
- Aries 7.5 deg -> seg=1 (still Taurus)
- Taurus 0.0 deg -> seg=0 -> varga_sign Libra (6) because even sign shift +6
- Boundary: Aries 29.999 deg -> seg=5

## Notes (ambiguity or docstring vs code)
- No mismatch found between docstrings and implementations for D4/D5/D6.
- Parivritti method details are defined in `docs/jhora/utils.py` rather than in chart functions.
- All methods assume `planet_longitude` is in [0, 30). No explicit clamping is done.

## Implementation checklist (for Kerykeion)

- Add D4/D5/D6 to varga registry with method labels matching PyJHora docstrings.
- Use `const.varga_option_dict` to set defaults (all three default to method 1).
- Implement Traditional Parasara rules exactly as above.
- Implement parivritti methods using the same mapping semantics as PyJHora:
  - cyclic = `utils.parivritti_cyclic`
  - even_reverse = `utils.parivritti_even_reverse`
  - alternate = `utils.parivritti_alternate`
- Tests: include Aries 0.0, Taurus 0.0, Aries 7.5, and near-boundary (29.999) for each chart.
- Cross-check with PyJHora tests in `docs/jhora/tests/pvr_tests.py`:
  - D4 method tests around chapter "D4 different methods test"
  - D5 method tests around chapter "D5 panchamsa different methods test"
  - D6 method tests around chapter "D6 shashthamsa different methods test"
