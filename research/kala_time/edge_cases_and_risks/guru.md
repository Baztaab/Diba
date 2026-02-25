# PyJHora-only

## E17 — Missing date/time assumptions

- provenance: `src/jhora/utils.py:L135-L141`

```python
    if dob is None:
        today = datetime.datetime.today()
        dob = (today.year,today.month,today.day)
        print("Today's Date:",dob,'assumed')
    if tob is None:
        tob = tuple(str(datetime.datetime.now()).split()[1].split(':'))
        print('Current time:',tob,'assumed')
```

## E03 — Local rise_jd recomputation in sunrise

- provenance: `src/jhora/panchanga/drik.py:L360-L365`

```python
    """ ADDED THE FOLLOWING IN V2.5.2 TO RECALCULATE RISE_JD"""
    dob = (y,m,d)
    tob = tuple(utils.to_dms(rise_local_time, as_string=False))
    rise_jd = utils.julian_day_number(dob, tob)
    # Convert to local time
    return [rise_local_time, utils.to_dms(rise_local_time),rise_jd]
```
