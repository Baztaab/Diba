# match_behavior_contract_map.engine_plus_consumers.md

## Snapshot identity (FACTS)

- pyjhora_root: `D:\lab\Pyjhora`
- extraction_timestamp_local: `2026-02-28 06:01:56`
- in-scope files: `9`
- in-scope file digests (SHA256):
- `src/jhora/horoscope/match/compatibility.py` -> `1fd2ca3de139ccac5cce7f4985ff1346bf7008a392086ed053c8d3a1138cf08d` (bytes: `43007`)
- `src/jhora/const.py` -> `2dacc910fce9babc69582491b52cde9fd23ab9dde835d41efb65fc0f79e00ba8` (bytes: `79727`)
- `src/jhora/utils.py` -> `861062b3abba1655b9d4e5608333f8aaa1d391b3d38ecdacbac565bf930f3875` (bytes: `70076`)
- `src/jhora/data/all_nak_pad_boy_girl.csv` -> `2c89e04f41606c9077895c51a8e5c5abbba07df80da93b8f011bf5b91ae2b4d6` (bytes: `685288`)
- `src/jhora/data/all_nak_pad_boy_girl_south.csv` -> `6b191884b2a691b061e82c5fba2b6fac423977d74596fe0f8a5235d0e9f710cd` (bytes: `961806`)
- `src/jhora/horoscope/match/all_nak_pad_boy_girl.csv` -> `2c89e04f41606c9077895c51a8e5c5abbba07df80da93b8f011bf5b91ae2b4d6` (bytes: `685288`)
- `src/jhora/horoscope/match/all_nak_pad_boy_girl_south.csv` -> `b0ad190606500e7bff1c357f65dae33c15e6cf27718ed064823d002bad00a031` (bytes: `913422`)
- `src/jhora/ui/match_ui.py` -> `7a14b867394dbdf05857f133c8c59fcfce7e3a401b62980b8bb450c8dfde809e` (bytes: `18011`)
- `src/jhora/ui/horo_chart_tabs.py` -> `f38615b20964505a98e25a513f58aa238a77bb7c53ad6b14b70c54cee5cb556c` (bytes: `396681`)

## Scope (FACTS)

- In-scope engine files:
  - `src/jhora/horoscope/match/compatibility.py`
  - `src/jhora/const.py`
  - `src/jhora/utils.py`
- In-scope data files:
  - `src/jhora/data/all_nak_pad_boy_girl.csv`
  - `src/jhora/data/all_nak_pad_boy_girl_south.csv`
  - `src/jhora/horoscope/match/all_nak_pad_boy_girl.csv`
  - `src/jhora/horoscope/match/all_nak_pad_boy_girl_south.csv`
- In-scope consumers:
  - `src/jhora/ui/match_ui.py`
  - `src/jhora/ui/horo_chart_tabs.py`
- Out-of-scope:
  - refactor / bug-fix / data repair
  - UI redesign
  - CSV regeneration
  - threshold or rule changes

## Pattern inventory (FACTS)
- `compatibility`
- `Ashtakoota`
- `Match`
- `porutham`
- `compatibility_score`
- `compatibility_score_south`
- `varna`
- `vasiya`
- `tara_dina`
- `yoni`
- `graha_maitri`
- `gana`
- `bhakoot`
- `nadi`
- `mahendra`
- `vedha`
- `rajju`
- `sthree_dheerga`
- `_is_there_minimum_tamil_porutham`
- `exception_dict`
- `exception_22_list`
- `all_nak_pad_boy_girl`
- `read_csv`
- `count_stars`
- `count_rasis`

## Behavior taxonomy (FACTS)

- constants and scoring thresholds: `MC01`, `MC02`
- evaluator engine and hardcoded score tables: `MC03`, `MC04`
- South exceptions and Nadi behavior: `MC05`, `MC06`, `MC07`, `MC08`
- cache/database layer and drift facts: `MC09`, `MC10`, `MC11`, `MC12`
- consumer contracts and shape adjustments: `MC13`, `MC14`, `MC15`
- negative fact: `ABSENCE-OF-NADI-PARIHARA`
- residual inventory: `MC900`

## Evidence anchors (MC01..MCNN, MC900)

### MC01

- Behavior: Compatibility thresholds and South mandatory gating constants are centralized in const.
- Source: `src/jhora/const.py:L588-L592`
- Excerpt:
```python
compatibility_minimum_score_north = 18.0
compatibility_minimum_score_south = 6.0
compatibility_maximum_score_south = 10.0
compatibility_maximum_score_north = 36.0
mandatory_compatibility_south_list = [1,2,3,5] # Gana(1), Dhinam/Thara/Star(2), Yoni(3), Rasi(5). Rajju is also added.
```
- Observed behavior: North and South use different minimum and maximum totals, and South has a mandatory compatibility list.

### MC02

- Behavior: Active compatibility databases are hardwired to `src/jhora/data` and the engine aliases helper counters from utils.
- Source: `src/jhora/horoscope/match/compatibility.py:L42-L45`
- Excerpt:
```python
_DATABASE_FILE = const.ROOT_DIR+ '/data/all_nak_pad_boy_girl.csv'
_DATABASE_SOUTH_FILE = const.ROOT_DIR+ '/data/all_nak_pad_boy_girl_south.csv' 
count_stars = utils.count_stars
count_rasis = utils.count_rasis
```
- Observed behavior: Active reads target `data/` CSVs, not the duplicate files under `horoscope/match`, and `count_stars` / `count_rasis` are helper dependencies.

### MC03

- Behavior: `Ashtakoota` is the independent evaluator engine seeded from nakshatra, paadham and method.
- Source: `src/jhora/horoscope/match/compatibility.py:L178-L195`
- Excerpt:
```python
class Ashtakoota:
    """
        To compute Marriage compatibility score Ashtakoota system based on boy and girl's birth star
        @param boy_nakshatra_number: boy's nakshatra_list number [1 to 27]
        @param boy_paadham_number: boy's nakshatra_list paadham number [1 to 4]
        @param girl_nakshatra_number: girl's nakshatra_list number [1 to 27]
        @param girl_paadham_number: girl's nakshatra_list paadham number [1 to 4]
    """
    def __init__(self,boy_nakshatra_number:int,boy_paadham_number:int,girl_nakshatra_number:int,girl_paadham_number:int, method:str="North"):
        self.boy_nakshatra_number=boy_nakshatra_number#-1
        self.girl_nakshatra_number=girl_nakshatra_number#-1
        self.boy_paadham_number = boy_paadham_number
```
- Observed behavior: The engine precomputes boy/girl rasi numbers and star counts before any koota scoring.

### MC04

- Behavior: Core koota scoring uses hardcoded module arrays rather than external rule files.
- Source: `src/jhora/horoscope/match/compatibility.py:L115-L125`
- Excerpt:
```python
VarnaArray = [[1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 1, 0], [1, 1, 1, 1]]
varna_results = {0:'Not Matching',1:'Matching'}
varna_max_score = 1
vasiya_categories = ['Chathushpadha','Manava','Jalachara','Vanachara','Keeta']
VasiyaArray  =[ # From Saravali.de
            [2.0, 0.5, 1.0, 0.0, 2.0],
            [0.5, 2.0, 0.0, 0.0, 0.0],
            [1.0, 0.0, 2.0, 2.0, 2.0],
            [0.0, 0.0, 2.0, 2.0, 0.0],
            [1.0, 0.0, 1.0, 0.0, 2.0]]
VasiyaArray_AstroYogi =[ # From astroyogi.com
```
- Observed behavior: Varna and Vasiya tables are embedded in code; other score tables like `YoniArray` and `NadiArray` follow the same pattern elsewhere in the module.

### MC05

- Behavior: South Dina logic includes explicit exception dictionaries and a Vinashika override list.
- Source: `src/jhora/horoscope/match/compatibility.py:L317-L328`
- Excerpt:
```python
        exception_dict = {"12":[2,3,4],"14":[1,2,3],"16":[1,2,4]}
        if any([self.girl_nakshatra_number == int(k) and self.girl_paadham_number in vl for k,vl in exception_dict.items()]):
            return True
        if self.girl_nakshatra_number==self.boy_nakshatra_number:
            if self.girl_nakshatra_number in [1,3,5,10,13,15,20,23] and (self.girl_raasi_number < self.boy_raasi_number or self.girl_paadham_number < self.boy_paadham_number):
                return True
            elif self.girl_raasi_number != self.boy_raasi_number and self.boy_raasi_number < self.girl_raasi_number: # Same star diff rasi
                return True
        if self.girl_raasi_number == self.boy_raasi_number and self.boy_nakshatra_number < self.girl_nakshatra_number:
            return True
        exception_22_list = [(4,25),(7,1),(8,2),(10,4),(12,6),(13,7),(14,8),(17,11),(21,15),(25,19),(26,20),(27,21)]
        if (self.boy_nakshatra_number,self.girl_nakshatra_number) in exception_22_list: return True
```
- Observed behavior: South Dina compatibility is not a pure count rule; it adds ad hoc exception and override branches.

### MC06

- Behavior: Nadi compatibility is a direct array lookup with no embedded parihara branch.
- Source: `src/jhora/horoscope/match/compatibility.py:L421-L429`
- Excerpt:
```python
    def naadi_porutham(self):
        """
            To compute naadi koota for the given boy/girl birth star combination
            Returns the score in the range [0 or 8]
        """
        bvk = [0,1,2,2,1,0,0,1,2,2,1,0,0,1,2,2,1,0,0,1,2,2,1,0,0,1,2] ; gvk = bvk
        bv = bvk[self.boy_nakshatra_number-1] ; gv = gvk[self.girl_nakshatra_number-1]
        if 'south' in self.method.lower(): return NadiArray[bv][gv]==8
        return (NadiArray[bv][gv],naadi_max_score)
```
- Observed behavior: The active path is limited to bucket lookup through `NadiArray` for North and a boolean comparison for South.

### MC07

- Behavior: `compatibility_score_south` is a boolean-heavy aggregation with fixed false slots for Varna and Nadi.
- Source: `src/jhora/horoscope/match/compatibility.py:L500-L508`
- Excerpt:
```python
    def compatibility_score_south(self):
        varna_porutham = False
        vasiya_porutham = self.vasiya_porutham_south()
        gana_porutham = self.gana_porutham_south()
        dina_porutham = self.dina_porutham_south() # nakshathra_porutham is same as tara porutham
        yoni_porutham = self.yoni_porutham_south()
        raasi_adhipathi_porutham= self.raasi_adhipathi_porutham_south()
        raasi_porutham= self.raasi_porutham_south()
        naadi_porutham = False
```
- Observed behavior: South scoring is not a scaled North score; it is a different rule family with boolean components and a 10-point aggregate.

### MC08

- Behavior: South minimum acceptance uses a nested gate that branches on girl varna or a skip flag.
- Source: `src/jhora/horoscope/match/compatibility.py:L541-L554`
- Excerpt:
```python
        def _is_there_minimum_tamil_porutham(skip_varna_checking=const.skip_using_girls_varna_for_minimum_tamil_porutham): # V4.5.5
            if skip_varna_checking: # V4.5.5
                return rajju_porutham and dina_porutham and gana_porutham and raasi_porutham and yoni_porutham
            girl_varna = vasiya_raasi_list[self.girl_raasi_number-1]
            minimum_porutham = rajju_porutham
            if girl_varna==0:
                minimum_porutham = minimum_porutham and dina_porutham
            elif girl_varna==1:
                minimum_porutham = minimum_porutham and gana_porutham
            elif girl_varna==2:
                minimum_porutham = minimum_porutham and raasi_porutham
            else:
```
- Observed behavior: `_is_there_minimum_tamil_porutham` acts as a post-score acceptance gate rather than a component score.

### MC09

- Behavior: `update_compatibility_database` materializes scorer outputs directly into the active CSV caches.
- Source: `src/jhora/horoscope/match/compatibility.py:L578-L590`
- Excerpt:
```python
def update_compatibility_database(method='North'):
    import codecs, csv
    outFile = _DATABASE_FILE#'all_nak_pad_boy_girl.csv'
    if 'south' in method.lower():
        outFile = _DATABASE_SOUTH_FILE#'all_nak_pad_boy_girl_south.csv'
    fp = codecs.open(outFile, encoding='utf-8', mode='w')
    csv_writer = csv.writer(fp)
    for bn in range(27):
        for bp in range(4):
            for gn in range(27):
                for gp in range(4):
                    a = Ashtakoota(bn+1,bp+1,gn+1,gp+1,method=method)
```
- Observed behavior: North and South cache rows are generated from `Ashtakoota.compatibility_score()` and written to `data/` files.

### MC10

- Behavior: `Match` is a CSV-backed query/cache layer built on pandas filtering.
- Source: `src/jhora/horoscope/match/compatibility.py:L599-L608`
- Excerpt:
```python
        db_file = _DATABASE_FILE
        self.minimum_score = minimum_score
        if 'south' in method.lower(): 
            db_file = _DATABASE_SOUTH_FILE
            self.minimum_score = const.compatibility_minimum_score_south
        if os.path.exists(db_file):
            self.data_file = db_file
        else:
            Exception("database file:"+db_file+" not found.")
        self.match_db=pd.read_csv(db_file,header=None,encoding='utf-8')
```
- Observed behavior: `Match` does not recompute kootas; it reads the precomputed CSV selected by method and filters it.

### MC11

- Behavior: Active CSV authority is under `data/`, and the scoped duplicate files under `horoscope/match` are legacy mirrors.
- Source: `src/jhora/horoscope/match/compatibility.py:L42-L43`
- Excerpt:
```python
_DATABASE_FILE = const.ROOT_DIR+ '/data/all_nak_pad_boy_girl.csv'
_DATABASE_SOUTH_FILE = const.ROOT_DIR+ '/data/all_nak_pad_boy_girl_south.csv' 
```
- Observed behavior: Inference from source path constants plus snapshot digests shows the North legacy file matches the active file exactly, while the South legacy file has a different hash and a 17-column row shape versus the active South 18-column file.

### MC12

- Behavior: South cache shape drifts from North because `minimum_porutham` is appended only in the South branch of `compatibility_score`.
- Source: `src/jhora/horoscope/match/compatibility.py:L555-L561`
- Excerpt:
```python
        if 'south' in self.method.lower():
            compatibility_score = sum([dina_porutham,gana_porutham,mahendra_porutham,sthree_dheerga_porutham,yoni_porutham,\
                                         raasi_porutham,raasi_adhipathi_porutham,vasiya_porutham,rajju_porutham,vedha_porutham])
            minimum_porutham = _is_there_minimum_tamil_porutham()
            return [varna_porutham, vasiya_porutham, gana_porutham, dina_porutham, yoni_porutham, \
                    raasi_adhipathi_porutham, raasi_porutham, naadi_porutham,compatibility_score, \
                    mahendra_porutham,vedha_porutham,rajju_porutham,sthree_dheerga_porutham,minimum_porutham]
```
- Observed behavior: The scorer itself creates the North/South row-length split that later appears in cached CSVs and UI handling.

### MC13

- Behavior: `match_ui.py` consumes cached partner tuples from `Match.get_matching_partners` and sorts by score.
- Source: `src/jhora/ui/match_ui.py:L194-L197`
- Excerpt:
```python
        comp = compatibility.Match(boy_nakshatra_number=bn,boy_paadham_number=bp,girl_nakshatra_number=gn,girl_paadham_number=gp,\
                                   check_for_mahendra_porutham=m_check,check_for_vedha_porutham=v_check,\
                                   check_for_rajju_porutham=r_check,check_for_shreedheerga_porutham=s_check)
        self._matching_stars_tuple = utils.sort_tuple(comp.get_matching_partners(),4,reverse=True)
```
- Observed behavior: The preferred UI path is cache-backed rather than direct rule evaluation.

### MC14

- Behavior: `match_ui.py` also carries an old direct `Ashtakoota` path whose unpacking contract no longer matches the scorer output shape.
- Source: `src/jhora/ui/match_ui.py:L216-L219`
- Excerpt:
```python
        a = compatibility.Ashtakoota(boy_nakshatra_number,boy_paadham_number,girl_nakshatra_number,girl_paadham_number)
        ettu_poruthham_list = ['varna porutham', 'vasiya porutham', 'gana porutham', 'nakshathra porutham', 'yoni porutham', 'adhipathi porutham', 'raasi porutham', 'naadi porutham']
        naalu_porutham_list = ['mahendra porutham','vedha porutham','rajju porutham','sthree dheerga porutham']
        ettu_porutham_results,compatibility_score,naalu_porutham_results = a.compatibility_score()
```
- Observed behavior: The old path expects three outputs, while the active scorer returns 13 items for North and 14 for South.

### MC15

- Behavior: `horo_chart_tabs.py` performs South-specific shape adjustment on cached compatibility tuples.
- Source: `src/jhora/ui/horo_chart_tabs.py:L5218-L5224`
- Excerpt:
```python
        ettu_porutham_results = selected_matching_star_tuple[2]
        compatibility_score = selected_matching_star_tuple[3]
        naalu_porutham_results = selected_matching_star_tuple[4]
        minimum_tamil_porutham = naalu_porutham_results[-1]
        if 'south' in self._chart_type.lower():
            ettu_porutham_results = ettu_porutham_results[1:-1]
            #minimum_tamil_porutham = all([ettu_porutham_results[t] for t in const.mandatory_compatibility_south_list]) and naalu_porutham_results[2]          
```
- Observed behavior: The consumer reads `minimum_tamil_porutham` from the tail of `naalu_porutham_results` and slices `ettu_porutham_results[1:-1]` for South.

### ABSENCE-OF-NADI-PARIHARA

- Behavior: No built-in Nadi parihara or same-lord cancellation branch was found in the active compatibility engine.
- Source: `research/match_and_compatibility/_coverage_match_callsites_engine_plus_consumers.tsv:L2`
- Excerpt:
```text
Scope-ActiveCode	0	nadi_parihara	not_found_in_active_code	ABSENCE-OF-NADI-PARIHARA	engine_core
```
- Observed behavior: The negative fact is recorded explicitly rather than inferred only from prose.

### MC900

- Behavior: Residual matched rows are retained in the callsite inventory.
- Source: `research/match_and_compatibility/_coverage_match_callsites_engine_plus_consumers.tsv:L3`
- Excerpt:
```text
Scope-Residual	0	residual_inventory	retained_matches	MC900	residual
```
- Observed behavior: Non-focused matches remain visible in the inventory instead of being dropped.

## Conflict / ambiguity register

- UNCERTAIN-MC-DATA-DRIFT: Duplicate CSVs exist under `data/` and `horoscope/match/`, and the South copies diverge.
- UNCERTAIN-MC-SOUTH-SHAPE: South cache rows are 18 columns while North rows are 17.
- UNCERTAIN-MC-MISSING-PARIHARA: Classical Nadi cancellation logic is absent from the active code path.
- UNCERTAIN-MC-HARDCODED-ARRAYS: Koota scoring relies on hardcoded arrays instead of externalized rule data.
- UNCERTAIN-MC-UI-SHAPE-DRIFT: UI consumers rely on method-specific tuple slicing and tail extraction.

## Coverage ledger

- Inventory file: `research/match_and_compatibility/_coverage_match_callsites_engine_plus_consumers.tsv`
- Inventory columns: `file`, `line`, `pattern`, `function_context`, `anchor_id`, `scope_class`
- Inventory row count: `{callsite_row_count}`
- Unique `(file,function_context)` count: `{unique_file_context}`
- Rows by scope_class: `engine_core={scope_counter.get('engine_core',0)}`, `consumer_core={scope_counter.get('consumer_core',0)}`, `residual={scope_counter.get('residual',0)}`
- Absence rows (`ABSENCE-OF-NADI-PARIHARA`): `{absence_rows}`
- Koota scoring matrix: `research/match_and_compatibility/_coverage_koota_scoring_matrix.tsv`
- Compatibility exceptions matrix: `research/match_and_compatibility/_coverage_compatibility_exceptions_matrix.tsv`
- Output-contract matrix: `research/match_and_compatibility/_coverage_match_output_contract_matrix.tsv`

## Sanity checks

- command: `rg -n "^### MC[0-9]+|^### MC900|^### ABSENCE-OF-NADI-PARIHARA" research/match_and_compatibility/match_behavior_contract_map.engine_plus_consumers.md -S`
- command: `rg -n "UNCERTAIN-MC-" research/match_and_compatibility/match_behavior_contract_map.engine_plus_consumers.md -S`
- command: `rg -n "Source:" research/match_and_compatibility/match_behavior_contract_map.engine_plus_consumers.md -S`
- command: `Get-Content research/match_and_compatibility/_coverage_match_callsites_engine_plus_consumers.tsv | Measure-Object -Line`
- command: `Get-Content research/match_and_compatibility/_coverage_koota_scoring_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/match_and_compatibility/_coverage_compatibility_exceptions_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/match_and_compatibility/_coverage_match_output_contract_matrix.tsv | Measure-Object -Line`
