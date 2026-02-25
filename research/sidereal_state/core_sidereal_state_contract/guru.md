# PyJHora-only

## E08 — set_sid_mode and default mode mutation

- provenance: `src/jhora/panchanga/drik.py:L133-L149`

```python
    if key in [am.upper() for am in const.available_ayanamsa_modes.keys()]:
        if key == "SIDM_USER":
            _ayanamsa_value = ayanamsa_value
            swe.set_sid_mode(swe.SIDM_USER,ayanamsa_value)
        elif key == "SENTHIL":
            _ayanamsa_value = _calculate_ayanamsa_senthil_from_jd(jd)
        elif key == "SUNDAR_SS":
            _ayanamsa_value = _ayanamsa_surya_siddhantha_model(jd)
```

- provenance: `src/jhora/panchanga/drik.py:L142-L149`

```python
            swe.set_sid_mode(const.available_ayanamsa_modes[key])
    else:
        warnings.warn("Unsupported Ayanamsa mode:", ayanamsa_mode,const._DEFAULT_AYANAMSA_MODE+" Assumed")
        ayanamsa_mode = const._DEFAULT_AYANAMSA_MODE
        swe.set_sid_mode(const.available_ayanamsa_modes[const._DEFAULT_AYANAMSA_MODE] )#swe.SIDM_LAHIRI)
    _ayanamsa_mode = ayanamsa_mode
    const._DEFAULT_AYANAMSA_MODE = _ayanamsa_mode
```

## E09 — README test baseline

- provenance: `src/jhora/README.md:L17-L17`

```python
There is a test module (`jhora.tests.pvr_tests`) containing about 6300 tests that can be run to verify the same. Please note the tests assume `const._DEFAULT_AYANAMSA_MODE='LAHIRI'`.
```

## E26 — set_ayanamsa_mode callsite inventory samples

- provenance: `src/jhora/panchanga/drik.py:L227-L227`; `src/jhora/panchanga/drik.py:L245-L245`; `src/jhora/ui/panchangam.py:L450-L450`; `src/jhora/tests/pvr_tests.py:L5524-L5524`; `src/jhora/panchanga/vratha.py:L791-L791`

```python
set_ayanamsa_mode(_ayanamsa_default,_ayanamsa_value,jd_utc); _ayanamsa_mode = const._DEFAULT_AYANAMSA_MODE
set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd)
drik.set_ayanamsa_mode(self._ayanamsa_mode,jd=self.julian_day) if self._ayanamsa_mode.upper()=='SUNDAR_SS' else drik.set_ayanamsa_mode(self._ayanamsa_mode)
drik.set_ayanamsa_mode(ayan, ayanamsa_value, jd)
panchanga.set_ayanamsa_mode(ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE)
```

## E27 — jd_utc-basis set_ayanamsa_mode call with in-function reset

- provenance: `src/jhora/panchanga/drik.py:L227-L232`

```python
        set_ayanamsa_mode(_ayanamsa_default,_ayanamsa_value,jd_utc); _ayanamsa_mode = const._DEFAULT_AYANAMSA_MODE
        #print('drik sidereal long ayanamsa',_ayanamsa_mode, const._DEFAULT_AYANAMSA_MODE)
        #import inspect; print('called by',inspect.stack()[1].function)
    longi,_ = swe.calc_ut(jd_utc, planet, flags = flags)
    reset_ayanamsa_mode()
    return utils.norm360(longi[0]) # degrees
```

## E32 — UI conditional mode set call

- provenance: `src/jhora/ui/panchangam.py:L448-L451`

```python
def _ayanamsa_selection_changed(self):
    self._ayanamsa_mode = self._ayanamsa_combo.currentText().upper()
    drik.set_ayanamsa_mode(self._ayanamsa_mode,jd=self.julian_day) if self._ayanamsa_mode.upper()=='SUNDAR_SS' else drik.set_ayanamsa_mode(self._ayanamsa_mode)
    const._DEFAULT_AYANAMSA_MODE = self._ayanamsa_mode
```

## E33 — One-argument mode set calls

- provenance: `src/jhora/horoscope/main.py:L96-L99`

```python
if self.calculation_type == 'ss':
    print('Horoscope:main: Forcing ayanamsa to SURYASIDDHANTA for the SURYA SIDDHANTA calculation type')
    drik.set_ayanamsa_mode('SURYASIDDHANTA')
self.ayanamsa_mode = const._DEFAULT_AYANAMSA_MODE
```

- provenance: `src/jhora/tests/pvr_tests.py:L7200-L7211`

```python
drik.set_ayanamsa_mode("LAHIRI")
lang = 'en'; const._DEFAULT_LANGUAGE = lang
const.use_24hour_format_in_to_dms = False
""" So far we have 6739 tests ~ 300 seconds """
```

- provenance: `src/jhora/tests/pvr_tests.py:L7210-L7211`

```python
""" RESET AYANAMSA BACK TO DEFAULT """
drik.set_ayanamsa_mode(current_ayanamsa_mode)
```

## E34 — Three-argument mode set calls

- provenance: `src/jhora/tests/pvr_tests.py:L5524-L5528`

```python
drik.set_ayanamsa_mode(ayan, ayanamsa_value, jd)
long = drik.get_ayanamsa_value(jd)
test_example("Ayanamsa Tests - "+ayan,utils.to_dms(ayan_values[ayan],is_lat_long='plong',round_seconds_to_digits=2),
             utils.to_dms(long,is_lat_long='plong',round_seconds_to_digits=2))
drik.set_ayanamsa_mode(previous_ayanamsa_mode) # RESET AYANAMSA
```

- provenance: `src/jhora/panchanga/surya_sidhantha.py:L176-L179`

```python
else:
    flags = swe.FLG_SIDEREAL
    drik.set_ayanamsa_mode(drik._ayanamsa_mode,drik._ayanamsa_value,jd) # needed for swe.houses_ex()
nak_no,paadha_no,_ = drik.nakshatra_pada(asc_long)
```

## E35 — panchanga module mode set call

- provenance: `src/jhora/panchanga/vratha.py:L789-L792`

```python
utils.get_resource_lists()
msgs = utils.get_resource_messages()
panchanga.set_ayanamsa_mode(ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE)
lat =  42.1181#13.0389 # 13.0389 # 41.881832 # 65.8252 N # Latitude - N+/S-
```

## E36 — drik1 mode set forms

- provenance: `src/jhora/panchanga/drik1.py:L82-L84`

```python
self._ayanamsa_mode = const._DEFAULT_AYANAMSA_MODE
set_ayanamsa_mode(self._ayanamsa_mode)
_,self._ayanamsa_value = self.get_ayanamsa()
```

- provenance: `src/jhora/panchanga/drik1.py:L163-L168`

```python
if ayanamsa_mode is None: ayanamsa_mode = const._DEFAULT_AYANAMSA_MODE
key = ayanamsa_mode.upper()
#print('panchanga setting',key,ayanamsa_value,jd)
if key in [am.upper() for am in const.available_ayanamsa_modes.keys()]:
    set_ayanamsa_mode(ayanamsa_mode, ayanamsa_value, jd)
    self._ayanamsa_mode = ayanamsa_mode
```
