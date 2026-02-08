# Vedic Config Surface (PyJHora-Aligned)

## Ayanamsa

| id | swe mode | alias | status |
| --- | --- | --- | --- |
| `fagan` | `SIDM_FAGAN_BRADLEY` | - | implemented |
| `kp` | `SIDM_KRISHNAMURTI` | - | implemented |
| `lahiri` | `SIDM_LAHIRI` | - | implemented |
| `raman` | `SIDM_RAMAN` | - | implemented |
| `ushashashi` | `SIDM_USHASHASHI` | - | implemented |
| `yukteshwar` | `SIDM_YUKTESHWAR` | - | implemented |
| `suryasiddhanta` | `SIDM_SURYASIDDHANTA` | - | implemented |
| `suryasiddhanta_msun` | `SIDM_SURYASIDDHANTA_MSUN` | - | implemented |
| `aryabhata` | `SIDM_ARYABHATA` | - | implemented |
| `aryabhata_msun` | `SIDM_ARYABHATA_MSUN` | - | implemented |
| `ss_citra` | `SIDM_SS_CITRA` | - | implemented |
| `true_citra` | `SIDM_TRUE_CITRA` | - | implemented |
| `true_lahiri` | `SIDM_TRUE_CITRA` | `alias_of=true_citra` | implemented |
| `true_revati` | `SIDM_TRUE_REVATI` | - | implemented |
| `ss_revati` | `SIDM_SS_REVATI` | - | implemented |
| `true_pushya` | `SIDM_TRUE_PUSHYA` | - | implemented |
| `true_mula` | `SIDM_TRUE_MULA` | - | implemented |
| `kp_senthil` | `SIDM_KRISHNAMURTI_VP291` | - | implemented |
| `sidm_user` | `SIDM_USER` | - | implemented (requires user value) |
| `senthil` | - | - | recognized-not-implemented |
| `sundar_ss` | - | - | recognized-not-implemented |

## House Systems

| id | pyjhora method | status |
| --- | --- | --- |
| `1` | `1` | implemented (`equal_lagna_mid`) |
| `2` | `2` | implemented (`equal_lagna_start`) |
| `3` | `3` | implemented (`sripati`) |
| `4` | `4` | implemented (`placidus` / `kp` aliases) |
| `5` | `5` | implemented (`whole_sign` / `whole-sign` aliases) |

## Nodes

| policy | swiss ephemeris point |
| --- | --- |
| `mean` | `MEAN_NODE` |
| `true` | `TRUE_NODE` |
