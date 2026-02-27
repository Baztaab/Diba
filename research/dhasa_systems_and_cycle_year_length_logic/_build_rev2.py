import ast,csv,hashlib,re,shutil
from pathlib import Path
from datetime import datetime
repo=Path(r'd:\Diba');py=Path(r'd:\lab\Pyjhora')
out=repo/'research'/'dhasa_systems_and_cycle_year_length_logic';out.mkdir(parents=True,exist_ok=True)
cp=out/'_codepack';(cp/'src').mkdir(parents=True,exist_ok=True)
eng=sorted((py/'src/jhora/horoscope/dhasa').rglob('*.py'))
cons=[py/p for p in ['src/jhora/horoscope/main.py','src/jhora/const.py','src/jhora/utils.py','src/jhora/horoscope/chart/charts.py','src/jhora/horoscope/chart/house.py','src/jhora/panchanga/drik.py']]
files=sorted(set(eng+cons),key=lambda p:p.as_posix())
rel=lambda p:p.relative_to(py).as_posix()

def txt(p):
  for e in ('utf-8','utf-8-sig','latin-1'):
    try:return p.read_text(encoding=e)
    except:pass
  return p.read_text(errors='ignore')

def sha(p):
  b=p.read_bytes();return hashlib.sha256(b).hexdigest(),len(b)

def spans(s):
  try:t=ast.parse(s)
  except:return []
  r=[]
  def v(n,p=''):
    for c in ast.iter_child_nodes(n):
      if isinstance(c,ast.ClassDef):v(c,f'{p}.{c.name}' if p else c.name)
      elif isinstance(c,(ast.FunctionDef,ast.AsyncFunctionDef)):
        n2=f'{p}.{c.name}' if p else c.name;st=getattr(c,'lineno',None);en=getattr(c,'end_lineno',st)
        if st and en:r.append((st,en,n2));v(c,n2)
      else:v(c,p)
  v(t);return sorted(r,key=lambda x:(x[0],x[1]-x[0]))

def ctx(ss,l):
  c=[x for x in ss if x[0]<=l<=x[1]]
  return '<module>' if not c else sorted(c,key=lambda x:(x[1]-x[0],-x[0]))[0][2]

pat=[('dhasa',r'\bdhasa\b'),('dasha',r'\bdasha\b'),('bhukthi',r'\bbhukthi\b'),('bhukti',r'\bbhukti\b'),('antara',r'\bantara\b'),('antardhasa',r'\bantardhasa\b'),('pratyantara',r'\bpratyantara\b'),('year_duration',r'year_duration'),('sidereal_year',r'sidereal_year'),('tropical_year',r'tropical_year'),('lunar_year',r'lunar_year'),('savana_year',r'savana_year'),('human_life_span_for_',r'human_life_span_for_'),('dhasa_start_date',r'dhasa_start_date'),('dasha_start_date',r'dasha_start_date'),('start_jd +=',r'start_jd\s*\+='),('vimsottari_dict',r'vimsottari_dict'),('varsha_vimsottari_days',r'varsha_vimsottari_days'),('kalachakra_dhasa_duration',r'kalachakra_dhasa_duration'),('narayana',r'narayana'),('varsha_narayana',r'varsha_narayana'),('tribhagi',r'tribhagi'),('antardhasa_option',r'antardhasa_option'),('chara_method',r'chara_method'),('dhasa_starting_planet',r'dhasa_starting_planet'),('seed_star',r'seed_star'),('month_duration',r'month_duration'),('\\b30\\b',r'\b30\b'),('ayanamsa',r'ayanamsa'),('360',r'\b360\b'),('365.25',r'365\.25'),('365.256',r'365\.256')]
comp=[(a,re.compile(b)) for a,b in pat]

ar={
'src/jhora/const.py':[('DS01',174,181),('DS02',203,213)],
'src/jhora/horoscope/dhasa/graha/vimsottari.py':[('DS03',28,31),('DS04',47,56),('DS05',73,80),('DS06',116,119),('DS07',198,203),('DS28',230,237)],
'src/jhora/horoscope/dhasa/graha/ashtottari.py':[('DS08',103,109)],
'src/jhora/horoscope/dhasa/graha/tithi_ashtottari.py':[('DS09',46,51),('DS29',75,80)],
'src/jhora/horoscope/dhasa/graha/tithi_yogini.py':[('DS10',71,76)],
'src/jhora/horoscope/dhasa/graha/yoga_vimsottari.py':[('DS11',45,50)],
'src/jhora/horoscope/dhasa/graha/yogini.py':[('DS12',96,102)],
'src/jhora/horoscope/dhasa/annual/mudda.py':[('DS13',32,33),('DS14',65,72)],
'src/jhora/horoscope/dhasa/raasi/narayana.py':[('DS15',53,56),('DS16',135,138)],
'src/jhora/horoscope/dhasa/raasi/sudasa.py':[('DS17',53,56),('DS18',74,77),('DS34',53,53)],
'src/jhora/horoscope/dhasa/raasi/chara.py':[('DS19',228,238),('DS20',241,243)],
'src/jhora/horoscope/dhasa/raasi/kalachakra.py':[('DS21',41,50),('DS22',102,112),('DS30',138,143)],
'src/jhora/horoscope/main.py':[('DS23',95,100),('DS24',1049,1057),('DS25',1073,1077),('DS26',1083,1085),('DS27',1163,1167)],
'src/jhora/horoscope/dhasa/raasi/kendradhi_rasi.py':[('DS31',53,61)]}

def aid(r,l):
  for x in ar.get(r,[]):
    if x[1]<=l<=x[2]:return x[0]
  return 'DS900'

rows=[];hits={k:0 for k,_ in pat};eng_aya=0
for p in files:
  r=rel(p);s=txt(p).splitlines();sp=spans('\n'.join(s));sc='engine_helper' if r.endswith('__init__.py') else ('engine_core' if r.startswith('src/jhora/horoscope/dhasa/') else 'consumer_core')
  for i,l in enumerate(s,1):
    for k,c in comp:
      if c.search(l):
        hits[k]+=1
        if k=='ayanamsa' and r.startswith('src/jhora/horoscope/dhasa/'):eng_aya+=1
        rows.append({'file':r,'line':i,'pattern':k,'function_context':ctx(sp,i),'anchor_id':aid(r,i),'scope_class':sc})
if hits['month_duration']==0:rows.append({'file':'InScope-55','line':0,'pattern':'month_duration','function_context':'not_found','anchor_id':'DS33','scope_class':'residual'})
if eng_aya==0:rows.append({'file':'Engine-49','line':0,'pattern':'ayanamsa','function_context':'not_found_in_dhasa_engine','anchor_id':'DS32','scope_class':'residual'})
for r in rows:
  if r['anchor_id']=='DS900':r['scope_class']='residual'
rows=sorted(rows,key=lambda x:(x['file'],x['line'],x['pattern'],x['function_context']))
cs=out/'_coverage_dhasa_callsites_engine_plus_consumers.tsv'
with cs.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['file','line','pattern','function_context','anchor_id','scope_class'],delimiter='\t');w.writeheader();w.writerows(rows)
ln=cs.read_text(encoding='utf-8').splitlines();ds32=ds33=None
for i,l in enumerate(ln,1):
  if '\tDS32\t' in l:ds32=i
  if '\tDS33\t' in l:ds33=i

cy=[]
for p in files:
  r=rel(p);s=txt(p);ls=s.splitlines();sp=spans(s)
  for st,en,nm in sp:
    seg='\n'.join(ls[st-1:en]);nl=nm.lower()
    if not ('dhasa' in nl or 'bhuk' in nl or 'antara' in nl or any(t in seg for t in ['year_duration','sidereal_year','tropical_year','savana_year','lunar_year','period_elapsed','start_jd +='])):continue
    y=[]
    for t in ['sidereal_year','tropical_year','savana_year','lunar_year']:
      if t in seg:y.append(t)
    if re.search(r'\b360(\.0)?\b',seg):y.append('360')
    family=('graha.'+Path(r).stem if '/dhasa/graha/' in r else ('annual.'+Path(r).stem if '/dhasa/annual/' in r else ('raasi.'+Path(r).stem if '/dhasa/raasi/' in r else ('dhasa.'+Path(r).stem if '/dhasa/' in r else 'consumer.'+Path(r).stem))))
    basis=','.join(dict.fromkeys(y)) if y else 'Unknown'
    dln=st;dexpr='N/A'
    for i,t in enumerate(ls[st-1:en],st):
      if any(k in t for k in ['period_elapsed','duration =','start_date +=','start_jd +=','dhasa_duration','/360','/12']):dln=i;dexpr=t.strip();break
    bm='unknown'
    if 'period_elapsed' in seg and 'nak' in seg:bm='nakshatra_fraction'
    elif 'period_elapsed' in seg and ('one_star' in seg or 'planet_long' in seg):bm='longitude_fraction'
    elif 'get_fraction' in seg or 'sl_frac_left' in seg:bm='elapsed_period_backsolve'
    elif '12 -' in seg:bm='fixed_rule'
    ff='N/A'
    for t in ls[st-1:en]:
      if any(k in t for k in ['period_elapsed','get_fraction','sl_frac_left','12 -']):ff=t.strip();break
    sb='Unknown';sl=seg.lower();flags=[]
    if any(x in sl for x in ['lagna','asc','planet_positions[0]']) or 'dhasa_starting_planet' in seg:flags.append('Lagna')
    if any(x in sl for x in ['moon','nakshatra','star_position_from_moon']):flags.append('Moon')
    if 'sun' in sl and 'sunrise' not in sl:flags.append('Sun')
    stn=Path(r).stem.lower()
    if 'yoga' in stn:flags.append('YogaPoint')
    if 'karana' in stn:flags.append('KaranaPoint')
    if len(set(flags))==1:sb=list(set(flags))[0]
    elif len(set(flags))>1:sb='Mixed'
    nf=[]
    if '/360' in seg.replace(' ',''):nf.append('/360')
    if '/12' in seg.replace(' ',''):nf.append('/12')
    if '* year_duration' in seg or '*year_duration' in seg:nf.append('*year_duration')
    if '* const.sidereal_year' in seg or '*const.sidereal_year' in seg:nf.append('*const.sidereal_year')
    cy.append({'file':r,'function':nm,'dhasa_family':family,'year_basis_symbol':basis,'constant_source':'N/A','duration_formula':dexpr,'normalization_factor':(','.join(nf) if nf else 'none'),'balance_calc_method':bm,'initial_fraction_formula':ff,'seed_node_basis':sb,'evidence_lines':f'{r}:L{dln}-L{min(en,dln+2)}','anchor_id':aid(r,dln)})
if hits['month_duration']==0:cy.append({'file':'InScope-55','function':'not_found','dhasa_family':'engine.all','year_basis_symbol':'not_found','constant_source':'N/A','duration_formula':'month_duration not found in in-scope files','normalization_factor':'none','balance_calc_method':'unknown','initial_fraction_formula':'N/A','seed_node_basis':'Unknown','evidence_lines':f'{cs.relative_to(repo).as_posix()}:L{ds33}','anchor_id':'DS33'})
seen=set();cy2=[]
for r in sorted(cy,key=lambda x:(x['file'],x['function'],x['evidence_lines'])):
  k=(r['file'],r['function'],r['evidence_lines'])
  if k in seen:continue
  seen.add(k);cy2.append(r)
cy=cy2
cyf=out/'_coverage_dhasa_cycle_year_matrix.tsv'
with cyf.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['file','function','dhasa_family','year_basis_symbol','constant_source','duration_formula','normalization_factor','balance_calc_method','initial_fraction_formula','seed_node_basis','evidence_lines','anchor_id'],delimiter='\t');w.writeheader();w.writerows(cy)

outrows=[
{'producer_function':'src/jhora/horoscope/dhasa/graha/vimsottari.py::get_vimsottari_dhasa_bhukthi','producer_shape':'(vim_bal, [dhasa_lord,bhukthi_lord,bhukthi_start])','consumer_function':'src/jhora/horoscope/main.py::Horoscope._get_vimsottari_dhasa_bhukthi','consumer_index_use':'[dhasa_lord,bukthi_lord,bhukthi_start]=db[i]','match_status':'match','evidence_lines':'src/jhora/horoscope/dhasa/graha/vimsottari.py:L230-L237; src/jhora/horoscope/main.py:L1163-L1167','anchor_id':'DS27'},
{'producer_function':'src/jhora/horoscope/dhasa/annual/mudda.py::varsha_vimsottari_dhasa_bhukthi','producer_shape':'(dhasa_lord,bhukthi_lord,bhukthi_start,bhukthi_duration_days)','consumer_function':'src/jhora/horoscope/main.py::Horoscope._get_varsha_vimsottari_dhasa','consumer_index_use':'for pd,pb,bs,_ in md','match_status':'match','evidence_lines':'src/jhora/horoscope/dhasa/annual/mudda.py:L138-L143; src/jhora/horoscope/main.py:L1089-L1092','anchor_id':'DS26'},
{'producer_function':'src/jhora/horoscope/dhasa/raasi/narayana.py::varsha_narayana_dhasa_bhukthi','producer_shape':'(dhasa_lord,bhukthi_lord,dhasa_start,duration)','consumer_function':'src/jhora/horoscope/main.py::Horoscope._get_varsha_narayana_dhasa','consumer_index_use':'[dhasa_lord,bukthi_lord,bukthi_start,_]=db[i]','match_status':'match','evidence_lines':'src/jhora/horoscope/dhasa/raasi/narayana.py:L173-L174; src/jhora/horoscope/main.py:L1083-L1085','anchor_id':'DS26'},
{'producer_function':'src/jhora/horoscope/dhasa/annual/patyayini.py::patyayini_dhasa','producer_shape':'[dhasa_lord,[bhukthi_lord,bhukthi_start],dhasa_duration_days]','consumer_function':'src/jhora/horoscope/main.py::Horoscope._get_patyatini_dhasa_bhukthi','consumer_index_use':'for p,bhukthis,_ in p_d_b; for bk,bs in bhukthis','match_status':'transformed','evidence_lines':'src/jhora/horoscope/dhasa/annual/patyayini.py:L54-L68; src/jhora/horoscope/main.py:L1102-L1114','anchor_id':'DS26'},
{'producer_function':'src/jhora/horoscope/dhasa/raasi/chara.py::get_dhasa_antardhasa','producer_shape':'(dhasa_lord,bhukthi_lord,dhasa_start,duration)','consumer_function':'src/jhora/horoscope/main.py::Horoscope._get_chara_dhasa','consumer_index_use':'for _dhasa,_bhukthi,dhasa_start,_ in db','match_status':'match','evidence_lines':'src/jhora/horoscope/dhasa/raasi/chara.py:L247-L251; src/jhora/horoscope/main.py:L1436-L1440','anchor_id':'DS26'},
{'producer_function':'src/jhora/horoscope/dhasa/graha/vimsottari.py::get_vimsottari_dhasa_bhukthi(include_antardhasa=False)','producer_shape':'[dhasa_lord,dhasa_start]','consumer_function':'src/jhora/horoscope/main.py::Horoscope._get_vimsottari_dhasa_bhukthi','consumer_index_use':'consumer path expects three-item rows','match_status':'alt_shape_not_used_in_scope','evidence_lines':'src/jhora/horoscope/dhasa/graha/vimsottari.py:L232-L237','anchor_id':'DS28'}]
of=out/'_coverage_dhasa_output_contract_matrix.tsv'
with of.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['producer_function','producer_shape','consumer_function','consumer_index_use','match_status','evidence_lines','anchor_id'],delimiter='\t');w.writeheader();w.writerows(outrows)

opts=['use_tribhagi_variation','antardhasa_option','chara_method','dhasa_starting_planet','seed_star','include_antardhasa','include_antardasa','use_rasi_bhukthi_variation','star_position_from_moon','divisional_chart_factor']
op=[]
for p in files:
  r=rel(p);s=txt(p);ls=s.splitlines();sp=spans(s)
  for st,en,nm in sp:
    seg='\n'.join(ls[st-1:en])
    for o in opts:
      if o not in seg:continue
      e=[];vals=set()
      for i,t in enumerate(ls[st-1:en],st):
        if o in t and ('if ' in t or 'elif ' in t or o+'=' in t):e.append(i)
        if o in t:
          m=re.search(rf'{re.escape(o)}\s*==\s*([^:\n, )]+)',t)
          if m:vals.add(m.group(1).strip())
          m=re.search(rf'{re.escape(o)}\s+in\s+\[([^\]]+)\]',t)
          if m:
            for x in m.group(1).split(','):vals.add(x.strip())
          if re.search(rf'if\s+{re.escape(o)}\s*:',t):vals.add('truthy/falsy')
      if not e:e=[st]
      if not vals:vals.add('parameter_only')
      sm='none'
      if o=='use_tribhagi_variation' and ('global ' in seg or '*= _tribhagi_factor' in seg or 'vimsottari_dict[' in seg or 'ashtottari_adhipathi_dict[' in seg):sm='global_mutation'
      elif ' = ' in seg and o in seg:sm='local_recompute'
      at='none'
      if 'ayanamsa' in seg:at='direct_call' if ('set_ayanamsa_mode' in seg or 'get_ayanamsa' in seg) else 'import_coupled'
      op.append({'file':r,'function':nm,'option_name':o,'values_seen':','.join(sorted(vals)),'branch_evidence_lines':','.join('L'+str(x) for x in sorted(set(e))),'state_mutation':sm,'ayanamsa_touchpoint':at,'anchor_id':aid(r,e[0])})
if eng_aya==0:op.append({'file':'Engine-49','function':'not_found','option_name':'ayanamsa','values_seen':'not_found_in_dhasa_engine','branch_evidence_lines':'L'+str(ds32),'state_mutation':'none','ayanamsa_touchpoint':'none','anchor_id':'DS32'})
seen=set();op2=[]
for r in sorted(op,key=lambda x:(x['file'],x['function'],x['option_name'],x['branch_evidence_lines'])):
  k=(r['file'],r['function'],r['option_name'],r['branch_evidence_lines'])
  if k in seen:continue
  seen.add(k);op2.append(r)
op=op2
opf=out/'_coverage_dhasa_option_switch_matrix.tsv'
with opf.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['file','function','option_name','values_seen','branch_evidence_lines','state_mutation','ayanamsa_touchpoint','anchor_id'],delimiter='\t');w.writeheader();w.writerows(op)

man=[]
for p in files:
  r=rel(p);d=cp/r;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);h,b=sha(p)
  man.append({'original_path':r,'codepack_path':f'research/dhasa_systems_and_cycle_year_length_logic/_codepack/{r}','sha256':h,'bytes':b})
man=sorted(man,key=lambda x:x['original_path'])
with (cp/'MANIFEST.tsv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['original_path','codepack_path','sha256','bytes'],delimiter='\t');w.writeheader();w.writerows(man)

cache={rel(p):txt(p).splitlines() for p in files}
def sn(r,s,e):
  a=cache[r];s=max(1,s);e=min(len(a),e);q=a[s-1:e];q=q[:12] if len(q)>12 else q;return '\n'.join(q)

anc=[('DS01','Year basis constants and generic dhasa lifespan are module-level constants.','src/jhora/const.py',174,181),('DS02','Family-specific cycle dictionaries and life-span constants are defined in const.','src/jhora/const.py',203,213),('DS03','Vimsottari uses sidereal year as default year_duration symbol.','src/jhora/horoscope/dhasa/graha/vimsottari.py',28,31),('DS04','Vimsottari start seed supports Moon/Lagna and special points via dhasa_starting_planet.','src/jhora/horoscope/dhasa/graha/vimsottari.py',47,56),('DS05','Vimsottari balance back-solves start date from nakshatra remainder fraction.','src/jhora/horoscope/dhasa/graha/vimsottari.py',73,80),('DS06','Vimsottari bhukti duration uses maha-lord and bhukti-lord normalization.','src/jhora/horoscope/dhasa/graha/vimsottari.py',116,119),('DS07','Vimsottari tribhagi branch mutates global life-span and duration dictionary.','src/jhora/horoscope/dhasa/graha/vimsottari.py',198,203),('DS08','Ashtottari start date uses longitude range fraction.','src/jhora/horoscope/dhasa/graha/ashtottari.py',103,109),('DS09','Tithi Ashtottari balance uses tithi fraction.','src/jhora/horoscope/dhasa/graha/tithi_ashtottari.py',46,51),('DS10','Tithi Yogini balance uses tithi fraction and back-solved start_jd.','src/jhora/horoscope/dhasa/graha/tithi_yogini.py',71,76),('DS11','Yoga Vimsottari balance uses yogam fraction.','src/jhora/horoscope/dhasa/graha/yoga_vimsottari.py',45,50),('DS12','Yogini balance uses nakshatra arc remainder with one_star.','src/jhora/horoscope/dhasa/graha/yogini.py',96,102),('DS13','Mudda annual path binds year_duration to tropical_year.','src/jhora/horoscope/dhasa/annual/mudda.py',32,33),('DS14','Mudda durations normalize with /360.0 over annual day dictionary.','src/jhora/horoscope/dhasa/annual/mudda.py',65,72),('DS15','Varsha Narayana branch scales dhasa_factor by dividing year basis with 360.','src/jhora/horoscope/dhasa/raasi/narayana.py',53,56),('DS16','Rasi Narayana seed is derived from Lagna and 7th-house strength comparison.','src/jhora/horoscope/dhasa/raasi/narayana.py',135,138),('DS17','Sudasa computes initial remaining fraction from 30-degree sign arc.','src/jhora/horoscope/dhasa/raasi/sudasa.py',53,56),('DS18','Sudasa applies initial fraction to first dhasa duration before bhukti expansion.','src/jhora/horoscope/dhasa/raasi/sudasa.py',74,77),('DS19','Chara dispatch toggles cycle count by chara_method.','src/jhora/horoscope/dhasa/raasi/chara.py',228,238),('DS20','Chara per-sign duration formula switches between method branches and second-cycle inversion.','src/jhora/horoscope/dhasa/raasi/chara.py',241,243),('DS21','Kalachakra computes birth index and remaining duration from paadha travel fraction.','src/jhora/horoscope/dhasa/raasi/kalachakra.py',41,50),('DS22','Kalachakra converts bhukti and dhasa durations into days using sidereal_year.','src/jhora/horoscope/dhasa/raasi/kalachakra.py',102,112),('DS23','Main initialization mutates ayanamsa mode for SS calculation type.','src/jhora/horoscope/main.py',95,100),('DS24','Main groups graha and rasi dhasa dispatch paths via dedicated wrappers.','src/jhora/horoscope/main.py',1049,1057),('DS25','Main annual wrapper composes patyayini, mudda, and varsha narayana outputs.','src/jhora/horoscope/main.py',1073,1077),('DS26','Main consumer wrappers unpack four-field producer tuples.','src/jhora/horoscope/main.py',1083,1085),('DS27','Main vimsottari wrapper unpacks three-field rows after balance tuple.','src/jhora/horoscope/main.py',1163,1167),('DS28','Vimsottari producer emits alternate row shape when include_antardhasa is False.','src/jhora/horoscope/dhasa/graha/vimsottari.py',230,237),('DS29','Ashtottari antardhasa_option changes start lord and direction.','src/jhora/horoscope/dhasa/graha/tithi_ashtottari.py',75,80),('DS30','Kalachakra seed selector supports dhasa_starting_planet options.','src/jhora/horoscope/dhasa/raasi/kalachakra.py',138,143),('DS31','Kendradhi-Rasi divides dhasa by 12 for bhukti and scales by sidereal_year.','src/jhora/horoscope/dhasa/raasi/kendradhi_rasi.py',53,61)]

u=len({(r['file'],r['function_context']) for r in rows});res=sum(1 for r in rows if r['anchor_id']=='DS900');sc={}
for r in rows:sc[r['scope_class']]=sc.get(r['scope_class'],0)+1
shots=[]
for p in files:
  h,b=sha(p);shots.append((rel(p),h,b))
shots=sorted(shots,key=lambda x:x[0])

m=out/'dhasa_behavior_contract_map.engine_plus_consumers.md'
with m.open('w',encoding='utf-8',newline='\n') as f:
  f.write('# dhasa_behavior_contract_map.engine_plus_consumers.md\n\n## Snapshot identity (FACTS)\n\n')
  f.write(f'- pyjhora_root: `{py}`\n- extraction_timestamp_local: `{datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")}`\n- in-scope files: `{len(files)}`\n- in-scope file digests (SHA256):\n')
  for r,h,b in shots:f.write(f'  - `{r}` -> `{h}` (bytes: `{b}`)\n')
  f.write('\n## Scope (FACTS)\n\n- In-scope engine files:\n  - `src/jhora/horoscope/dhasa/**/*.py` (49 files)\n- In-scope consumers/config:\n')
  [f.write(f'  - `{x}`\n') for x in ['src/jhora/horoscope/main.py','src/jhora/const.py','src/jhora/utils.py','src/jhora/horoscope/chart/charts.py','src/jhora/horoscope/chart/house.py','src/jhora/panchanga/drik.py']]
  f.write('- Out-of-scope:\n  - UI modules\n  - tests\n  - `src/jhora/panchanga/drik1.py`\n  - deep consumers outside one-hop list\n\n## Pattern inventory (FACTS)\n\n')
  [f.write(f'- `{k}`\n') for k,_ in pat]
  f.write('\n## Schema patch set (FACTS)\n\n- `_coverage_dhasa_cycle_year_matrix.tsv` includes `balance_calc_method`, `initial_fraction_formula`, `seed_node_basis`.\n- `_coverage_dhasa_option_switch_matrix.tsv` includes `ayanamsa_touchpoint`.\n\n## Behavior taxonomy (FACTS)\n\n- year bases and constants: `DS01`, `DS02`, `DS03`, `DS13`, `DS14`, `DS15`, `DS31`\n- balance and start backsolve: `DS05`, `DS08`, `DS09`, `DS10`, `DS11`, `DS12`, `DS17`, `DS18`, `DS21`\n- seed basis and option routing: `DS04`, `DS16`, `DS19`, `DS20`, `DS29`, `DS30`\n- producer and consumer shape contracts: `DS24`, `DS25`, `DS26`, `DS27`, `DS28`\n- ayanamsa audit and month token audit: `DS23`, `DS32`, `DS33`, `DS34`\n\n## Evidence anchors (DS01..DS34, DS900)\n\n')
  for a,b,r,s,e in anc:
    f.write(f'### {a}\n\n- Behavior: {b}\n- Source: `{r}:L{s}-L{e}`\n- Excerpt:\n```python\n{sn(r,s,e)}\n```\n- Observed behavior: evidence line block shows the active rule in this path.\n\n')
  if ds32:f.write(f'### DS32\n\n- Behavior: No direct ayanamsa callsite was found inside dhasa engine files (49-file scope).\n- Source: `{cs.relative_to(repo).as_posix()}:L{ds32}`\n- Excerpt:\n```text\nEngine-49\t0\tayanamsa\tnot_found_in_dhasa_engine\tDS32\n```\n- Observed behavior: engine absence is recorded as evidence row in callsite ledger.\n\n')
  if ds33:f.write(f'### DS33\n\n- Behavior: month_duration token has no match in the in-scope file set.\n- Source: `{cs.relative_to(repo).as_posix()}:L{ds33}`\n- Excerpt:\n```text\nInScope-55\t0\tmonth_duration\tnot_found\tDS33\n```\n- Observed behavior: absence is recorded as evidence row in callsite ledger.\n\n')
  f.write('### DS34\n\n- Behavior: The numeric token 30 appears in Sudasa balance formula.\n- Source: `src/jhora/horoscope/dhasa/raasi/sudasa.py:L53-L53`\n- Excerpt:\n```text\n(30-sree_lagna_longitude)/30\n```\n- Observed behavior: 30-day or 30-degree token appears in active duration seed formula.\n\n### DS900\n\n- Behavior: Rows outside focused DS anchors remain in residual inventory.\n- Source: `research/dhasa_systems_and_cycle_year_length_logic/_coverage_dhasa_callsites_engine_plus_consumers.tsv`\n- Excerpt:\n```text\nRows with anchor_id=DS900 are retained as residual evidence.\n```\n- Observed behavior: residual entries keep non-focused matches visible in-scope.\n\n')
  f.write('## Conflict / ambiguity register\n\n- UNCERTAIN-DS-YEAR-01: year basis varies across dhasa families.\n  - Evidence: `DS03`, `DS13`, `DS14`, `DS15`, `DS31`\n- UNCERTAIN-DS-NORM-01: normalization rules vary (`/360`, `/12`, life-span factors).\n  - Evidence: `DS06`, `DS14`, `DS22`, `DS31`\n- UNCERTAIN-DS-BALANCE-01: initial balance formulas vary by family and input basis.\n  - Evidence: `DS05`, `DS08`, `DS09`, `DS10`, `DS11`, `DS12`, `DS17`\n- UNCERTAIN-DS-SEED-01: seed node basis changes between Moon, Lagna, Sun, and special points.\n  - Evidence: `DS04`, `DS16`, `DS30`\n- UNCERTAIN-DS-OUTIDX-01: producer row-shape differs by include flags and family wrappers.\n  - Evidence: `DS26`, `DS27`, `DS28`\n- UNCERTAIN-DS-STATE-01: option branches mutate global duration state in tribhagi paths.\n  - Evidence: `DS07`, `DS29`\n- UNCERTAIN-DS-AYA-01: ayanamsa state appears in consumer init but not direct in dhasa engine files.\n  - Evidence: `DS23`, `DS32`\n\n## Coverage ledger\n\n')
  f.write(f'- Inventory file: `{cs.relative_to(repo).as_posix()}`\n- Inventory columns: `file`, `line`, `pattern`, `function_context`, `anchor_id`, `scope_class`\n- Inventory row count: `{len(rows)}`\n- Unique `(file,function_context)` count: `{u}`\n- Rows by scope_class: '+', '.join(f'`{k}={v}`' for k,v in sorted(sc.items()))+f'\n- Residual rows (`DS900`): `{res}`\n- Cycle-year matrix: `{cyf.relative_to(repo).as_posix()}`\n- Output-contract matrix: `{of.relative_to(repo).as_posix()}`\n- Option-switch matrix: `{opf.relative_to(repo).as_posix()}`\n\n## Sanity checks\n\n')
  f.write(f'- command: `rg -n "^### DS[0-9]+|^### DS900" {m.relative_to(repo).as_posix()} -S`\n- command: `rg -n "UNCERTAIN-DS-" {m.relative_to(repo).as_posix()} -S`\n- command: `rg -n "Source:" {m.relative_to(repo).as_posix()} -S`\n- command: `Get-Content {cs.relative_to(repo).as_posix()} | Measure-Object -Line`\n- command: `Get-Content {cyf.relative_to(repo).as_posix()} | Measure-Object -Line`\n- command: `Get-Content {of.relative_to(repo).as_posix()} | Measure-Object -Line`\n- command: `Get-Content {opf.relative_to(repo).as_posix()} | Measure-Object -Line`\n')

rep=out/'report.md'
with rep.open('w',encoding='utf-8',newline='\n') as f:
  f.write('# dhasa_systems_and_cycle_year_length_logic\n\n- status: active\n- artifacts:\n  - [dhasa_behavior_contract_map.engine_plus_consumers.md](./dhasa_behavior_contract_map.engine_plus_consumers.md)\n  - [_coverage_dhasa_callsites_engine_plus_consumers.tsv](./_coverage_dhasa_callsites_engine_plus_consumers.tsv)\n  - [_coverage_dhasa_cycle_year_matrix.tsv](./_coverage_dhasa_cycle_year_matrix.tsv)\n  - [_coverage_dhasa_output_contract_matrix.tsv](./_coverage_dhasa_output_contract_matrix.tsv)\n  - [_coverage_dhasa_option_switch_matrix.tsv](./_coverage_dhasa_option_switch_matrix.tsv)\n  - [_codepack/MANIFEST.tsv](./_codepack/MANIFEST.tsv)\n- observed PyJHora behaviors:\n  - cycle-year bases vary across sidereal, tropical, and 360-normalized paths.\n  - initial dhasa balance formulas use nakshatra, tithi, yoga, and longitude fractions by family.\n  - option branches route seed basis, direction, and tribhagi scaling logic.\n  - consumer wrappers in main convert producer tuples into display labels.\n  - dhasa engine files contain no direct ayanamsa callsite; ayanamsa mutation appears in main init.\n- inventory summary:\n')
  f.write(f'  - callsite rows: `{len(rows)}`\n  - unique `(file,function_context)`: `{u}`\n  - residual callsites (`DS900`): `{res}`\n  - cycle-year matrix rows (data rows): `{len(cy)}`\n  - output-contract matrix rows (data rows): `{len(outrows)}`\n  - option-switch matrix rows (data rows): `{len(op)}`\n  - codepack files: `{len(man)}`\n- cross-cutting map:\n  - [sweep_2_architecture_coupling_contract_map.md](../../sweep_2_architecture_coupling_contract_map.md)\n')

idx=repo/'research'/'INDEX.md';t=idx.read_text(encoding='utf-8')
entry='- `dhasa_systems_and_cycle_year_length_logic` — ACTIVE\n  - `report`: `D:\\Diba\\research\\dhasa_systems_and_cycle_year_length_logic\\report.md`\n'
if 'dhasa_systems_and_cycle_year_length_logic' not in t:
  if not t.endswith('\n'):t+='\n'
  t+='\n'+entry;idx.write_text(t,encoding='utf-8',newline='\n')
print('DONE',len(files),len(rows),len(cy),len(outrows),len(op),ds32,ds33)
