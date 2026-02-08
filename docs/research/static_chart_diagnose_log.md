# Static Golden Diagnose Log (Before/After)

## Before Fix

```text
=== scenario_01 ===
meta.ayanamsa: id actual=lahiri expected=lahiri | dms actual=23°52'44.80" expected=23°51'37.78"
asc: actual=05°Vi21'07.29" expected=09°Cn34'45.81" delta_arcsec=+200781.480
rahu: actual=10°Ge40'38.18" expected=14°Ge39'58.75" delta_arcsec=-14360.570
ketu: actual=10°Sg40'38.18" expected=14°Sg39'58.75" delta_arcsec=-14360.570
sun: actual=13°Cn16'50.87" expected=01°Ta36'19.49" delta_arcsec=+258031.380
moon: actual=17°Sc22'42.79" expected=10°Aq50'40.81" delta_arcsec=-300478.020

=== scenario_02 ===
meta.ayanamsa: id actual=lahiri expected=lahiri | dms actual=23°59'48.40" expected=23°58'51.35"
asc: actual=14°Vi46'37.03" expected=14°Vi47'50.50" delta_arcsec=-73.470
rahu: actual=27°Sg38'29.99" expected=27°Sg39'27.04" delta_arcsec=-57.050
ketu: actual=27°Ge38'29.99" expected=27°Ge39'27.04" delta_arcsec=-57.050
sun: actual=16°Sg18'38.05" expected=16°Sg19'35.10" delta_arcsec=-57.050
moon: actual=17°Ge06'14.29" expected=17°Ge07'11.34" delta_arcsec=-57.050

=== scenario_03 ===
meta.ayanamsa: id actual=lahiri expected=lahiri | dms actual=24°01'35.19" expected=24°00'38.05"
asc: actual=09°Ge07'17.85" expected=09°Ge08'32.58" delta_arcsec=-74.730
rahu: actual=16°Sc32'27.71" expected=16°Sc33'24.85" delta_arcsec=-57.140
ketu: actual=16°Ta32'27.71" expected=16°Ta33'24.85" delta_arcsec=-57.140
sun: actual=02°Aq08'00.76" expected=02°Aq08'57.90" delta_arcsec=-57.140
moon: actual=11°Sc49'01.80" expected=11°Sc49'58.94" delta_arcsec=-57.140
```
## After Fix

```text
=== scenario_01 ===
meta.ayanamsa: id actual=lahiri expected=lahiri | dms actual=23°51'43.30" expected=23°51'37.78"
asc: actual=05°Vi21'52.69" expected=09°Cn34'45.81" delta_arcsec=+200826.880
rahu: actual=10°Ge41'39.69" expected=14°Ge39'58.75" delta_arcsec=-14299.060
ketu: actual=10°Sg41'39.69" expected=14°Sg39'58.75" delta_arcsec=-14299.060
sun: actual=13°Cn17'47.58" expected=01°Ta36'19.49" delta_arcsec=+258088.090
moon: actual=17°Sc23'39.51" expected=10°Aq50'40.81" delta_arcsec=-300421.300

=== scenario_02 ===
meta.ayanamsa: id actual=lahiri expected=lahiri | dms actual=23°58'46.43" expected=23°58'51.35"
asc: actual=14°Vi47'55.42" expected=14°Vi47'50.50" delta_arcsec=+4.920
rahu: actual=27°Sg39'31.96" expected=27°Sg39'27.04" delta_arcsec=+4.920
ketu: actual=27°Ge39'31.96" expected=27°Ge39'27.04" delta_arcsec=+4.920
sun: actual=16°Sg19'35.10" expected=16°Sg19'35.10" delta_arcsec=+0.000
moon: actual=17°Ge07'11.35" expected=17°Ge07'11.34" delta_arcsec=+0.010

=== scenario_03 ===
meta.ayanamsa: id actual=lahiri expected=lahiri | dms actual=24°00'48.89" expected=24°00'38.05"
asc: actual=09°Ge08'21.75" expected=09°Ge08'32.58" delta_arcsec=-10.830
rahu: actual=16°Sc33'14.02" expected=16°Sc33'24.85" delta_arcsec=-10.830
ketu: actual=16°Ta33'14.02" expected=16°Ta33'24.85" delta_arcsec=-10.830
sun: actual=02°Aq08'57.90" expected=02°Aq08'57.90" delta_arcsec=+0.000
moon: actual=11°Sc49'58.95" expected=11°Sc49'58.94" delta_arcsec=+0.010
```
