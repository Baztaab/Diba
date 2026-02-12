# Diba

Diba is a Vedic astrology computation core focused on deterministic sidereal calculations.

## Scope

- Swiss Ephemeris based core calculations
- Vedic D1 and varga payload assembly
- Canonical calculation context with SwissEph state control
- Strict runtime contracts for `ayanamsa_id`, `house_system_id`, and `node_mode`

Legacy charting/reporting layers have been removed from this repository.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from diba.vedic.factory import VedicSubjectFactory

model = VedicSubjectFactory.from_birth_data(
    year=2004,
    month=1,
    day=27,
    hour=14,
    minute=45,
    seconds=35.0,
    tz_str="Asia/Tehran",
    lat=35.7,
    lon=51.1,
    ayanamsa_id="lahiri",
    node_mode="mean",
    house_system_id="whole_sign",
)

print(model.core.objects["ascendant"].abs_pos_sidereal)
```

## CLI

```bash
python -m diba.cli vedic-d1 --help
```

## Test

```bash
pytest -q
```

## License

AGPL-3.0
