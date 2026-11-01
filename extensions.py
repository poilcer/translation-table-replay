"""Workbook-derived manuscript extensions; standard library only, offline."""
import argparse
import collections
import csv
import json
import math
import re
import statistics as st
from decimal import Decimal
from pathlib import Path
import importlib.util
_spec=importlib.util.spec_from_file_location('replay',Path(__file__).with_name('replay.py'))
replay=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(replay)

THRESHOLDS = ['0.001','0.005','0.01','0.02','0.03','0.04','0.05']
Counter=collections.Counter

def quantile(values, p):
    values=sorted(values)
    x=(len(values)-1)*p
    i=math.floor(x)
    # NumPy linear's stable interpolation branch, matching the candidate.
    t=x-i
    j=min(i+1,len(values)-1)
    return values[j]-(values[j]-values[i])*(1-t) if t>=.5 else values[i]+(values[j]-values[i])*t

def corr(x,y):
    mx,my=st.mean(x),st.mean(y)
    return math.fsum((a-mx)*(b-my) for a,b in zip(x,y))/math.sqrt(math.fsum((a-mx)**2 for a in x)*math.fsum((b-my)**2 for b in y))

def finite(x):
    try: return math.isfinite(float(x))
    except (TypeError,ValueError): return False

def number(x):
    return float(x) if finite(x) else x

def proof(rows):
    return dict(n=len(rows),sha256=replay.membership_digest(rows))

def direction(z):
    return 'up' if z >= 1.5 else 'down' if z <= -1.5 else 'unchanged'

def ranks(values):
    order = sorted(range(len(values)), key=values.__getitem__)
    out = [0.] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and values[order[j]] == values[order[i]]:
            j += 1
        for k in order[i:j]:
            out[k] = (i+j-1)/2 + 1
        i = j
    return out

def summary(ds):
    m, sp, ss = st.mean(ds), st.pstdev(ds), st.stdev(ds)
    return dict(n=len(ds), mean=m, population_sd=sp, sample_sd=ss,
                population_up=sum((d-m)/sp >= 1.5 for d in ds),
                population_down=sum((d-m)/sp <= -1.5 for d in ds))

def ad(book):
    rows=[]; audits=[]
    for sheet,data in book.items():
        treatment='vehicle' if 'control' in sheet else 'abeta'
        stratum='non_fmrp' if 'non_fmrp' in sheet else 'fmrp'
        local=[dict(sheet=sheet,excel_row=n,treatment=treatment,source_stratum=stratum,gene=c.get('A'),log2FoldChange=c.get('B'),padj=c.get('C')) for n,c in data if n>1]
        rows.extend(local)
        names=[r['gene'] for r in local if r['gene'] and r['gene'].strip()]
        audits.append(dict(sheet=sheet,data_rows=len(local),distinct_nonblank_ids=len(set(names)),duplicate_rows=len(names)-len(set(names)),blank_ids=len(local)-len(names),invalid_or_nonfinite_effect=sum(not finite(r['log2FoldChange']) for r in local),invalid_or_nonfinite_padj=sum(not finite(r['padj']) for r in local),padj_ge_005=sum(finite(r['padj']) and float(r['padj'])>=.05 for r in local)))
    sensitivity={}; membership_proofs={}; allsets={}
    for mode in ['primary','trim','padj_0.05','padj_0.01','finite_effect']:
        sets={'vehicle':set(),'abeta':set()}
        selected=[]
        for r in rows:
            g=r['gene']
            if not g or not g.strip(): continue
            if mode.startswith('padj') and not (finite(r['padj']) and float(r['padj'])<float(mode.split('_')[1])): continue
            if mode=='finite_effect' and not finite(r['log2FoldChange']): continue
            sets[r['treatment']].add(g.strip() if mode=='trim' else g)
            selected.append([r['sheet'],str(r['excel_row']),g.strip() if mode=='trim' else g])
        v,a=sets['vehicle'],sets['abeta']
        sensitivity[mode]=dict(vehicle=len(v),abeta=len(a),vehicle_unique=len(v-a),abeta_unique=len(a-v),shared=len(v&a),union=len(v|a))
        membership_proofs[mode]=dict(rows=proof(selected),names=proof([[g,'shared' if g in v&a else 'vehicle_unique' if g in v else 'abeta_unique'] for g in v|a]))
        allsets[mode]=sets
    strata={}; duplicates=[]; treatments={}
    for t in ['vehicle','abeta']:
        rr=[r for r in rows if r['treatment']==t]
        f={r['gene'] for r in rr if r['source_stratum']=='fmrp'}; nf={r['gene'] for r in rr if r['source_stratum']=='non_fmrp'}
        strata[t]=dict(fmrp=len(f),non_fmrp=len(nf),stratum_overlap=len(f&nf),fmrp_selected_fraction=len(f)/len(allsets['primary'][t]))
        groups=collections.defaultdict(list)
        for r in rr: groups[r['gene']].append(r)
        opposite=[]
        for g,group in sorted(groups.items()):
            if len(group)<2: continue
            duplicates.append(dict(treatment=t,gene=g,rows=[dict(sheet=r['sheet'],row=str(r['excel_row']),effect=r['log2FoldChange'],padj=r['padj']) for r in group]))
            effects=[float(r['log2FoldChange']) for r in group if finite(r['log2FoldChange'])]
            if min(effects)<0<max(effects): opposite.append(g)
        treatments[t]=dict(rows=len(rr),distinct_names=len(groups),excess=len(rr)-len(groups),duplicated_names=sorted(g for g,group in groups.items() if len(group)>1),opposite_sign_names=opposite,row_total_minus_shared=len(rr)-sensitivity['primary']['shared'])
    return dict(primary=sensitivity['primary'],sheet_audit=audits,sensitivity=sensitivity,strata=strata,duplicate_audit=duplicates,treatment_audit=treatments,membership_proofs=membership_proofs)

def pd(book):
    raw={key:[tuple(number(c.get(col)) if i in (4,5,6,7,8,9,10,11,12) else c.get(col) for i,col in enumerate('ABCDEFGHIJKLM')) for n,c in rows if n>1] for key,rows in zip(['GS','GSDA','KO'],book.values())}
    common=set.intersection(*(set(r[1] for r in rows) for rows in raw.values()))
    variants=[]; stats=[]; boundaries=[]; dup=[]; structure=[]; memberships=[]; threshold_checks=[]
    for key,rows in raw.items():
        assert all(isinstance(r[i],(int,float)) and math.isfinite(r[i]) and r[i]>0 for r in rows for i in (4,5,6,7)), 'Abundance inputs must be finite and positive'
        ds=[math.log2(r[5]/r[7])-math.log2(r[4]/r[6]) for r in rows]
        sym=collections.Counter(r[2] for r in rows)
        groups=collections.defaultdict(list)
        for r,d in zip(rows,ds): groups[r[2]].append(d)
        universes={'all_rows':ds,
                   'finite_FE':[d for r,d in zip(rows,ds) if isinstance(r[8],(int,float)) and math.isfinite(r[8])],
                   'nonduplicated_symbols_only':[d for r,d in zip(rows,ds) if sym[r[2]]==1],
                   'symbol_mean_delta':[st.mean(v) for v in groups.values()],
                   'common_literal_ids':[d for r,d in zip(rows,ds) if r[1] in common]}
        for label,values in universes.items(): variants.append(dict(contrast=key,universe=label,**summary(values)))
        s=summary(ds); m=s['mean']; sp=s['population_sd']; ss=s['sample_sd']
        caption={'GS':.226,'GSDA':.179,'KO':.273}[key]
        ferr=max(abs(d-r[11]) for r,d in zip(rows,ds))
        zerr=max(abs((d-m)/ss-r[12]) for r,d in zip(rows,ds))
        teerr=max(abs((r[10]-r[9])-d) for r,d in zip(rows,ds))
        linear=[r[5]/r[7]-r[4]/r[6] for r in rows]
        ln=[d*math.log(2) for d in ds]
        lnm, lns = st.mean(ln), st.stdev(ln)
        lnerr=max(abs((d-lnm)/lns-r[12]) for r,d in zip(rows,ln))
        stats.append(dict(contrast=key,**s,caption_sd=caption,caption_relative_excess_percent=100*(caption/ss-1),
                          duplicate_symbol_excess=len(rows)-len(sym),duplicated_symbol_groups=sum(n>1 for n in sym.values()),
                          duplicated_symbol_rows=sum(n for n in sym.values() if n>1),missing_FE=len(rows)-len(universes['finite_FE']),
                          max_delta_error=ferr,max_TE_subtraction_error=teerr,max_sample_z_error=zerr,
                          natural_log_z_max_error=lnerr,linear_TE_difference_sd=st.stdev(linear),
                          spearman_FE_delta=float(corr(ranks([r[8] for r in rows]),ranks(ds))),
                          source_up=sum(r[12]>=1.5 for r in rows),source_down=sum(r[12]<=-1.5 for r in rows)))
        for version,zscores in [('source',[r[12] for r in rows]),('sample',[(d-m)/ss for d in ds]),('population',[(d-m)/sp for d in ds])]:
            for sign in ('up','down'):
                inclusive={n for n,z in enumerate(zscores,2) if (z>=1.5 if sign=='up' else z<=-1.5)}
                strict={n for n,z in enumerate(zscores,2) if (z>1.5 if sign=='up' else z< -1.5)}
                threshold_checks.append(dict(contrast=key,score=version,direction=sign,inclusive=len(inclusive),strict=len(strict),membership_difference=len(inclusive^strict)))
        for n,(r,d) in enumerate(zip(rows,ds),2):
            zp=(d-m)/sp; zs=(d-m)/ss
            memberships.append(dict(contrast=key,excel_row=n,id=r[1],geneSymbol=r[2],population_direction=direction(zp),source_direction=direction(r[12])))
            if direction(zp)!=direction(r[12]): boundaries.append(dict(contrast=key,excel_row=n,id=r[1],geneSymbol=r[2],population_z=zp,sample_z=zs,source_z=r[12],delta=d,delta_distance_to_population_upper=d-(m+1.5*sp),delta_distance_to_sample_upper=d-(m+1.5*ss)))
            if sym[r[2]]>1: dup.append(dict(contrast=key,excel_row=n,id=r[1],geneSymbol=r[2],symbol_multiplicity=sym[r[2]]))
        for label,predicate in [('complex_FE_lt_minus250',lambda f:f < -250),('simple_FE_gt_minus20',lambda f:f > -20)]:
            vals=[d for r,d in zip(rows,ds) if predicate(r[8])]
            structure.append(dict(contrast=key,stratum=label,n=len(vals),delta_mean=st.mean(vals),delta_median=st.median(vals),q25=float(quantile(vals,.25)),q75=float(quantile(vals,.75))))
    structure_audit={}
    for key,rows in raw.items():
        counter=collections.Counter(r[2] for r in rows)
        structure_audit[key]={label:dict(rows=sum(pred(r[8]) for r in rows),unique_symbols=len({r[2] for r in rows if pred(r[8])}),singleton_symbols=sum(pred(r[8]) and counter[r[2]]==1 for r in rows),common_id_rows=sum(pred(r[8]) and r[1] in common for r in rows)) for label,pred in [('complex',lambda f:f < -250),('simple',lambda f:f > -20)]}
    maps={k:{r[1]:r[11] for r in rows} for k,rows in raw.items()}
    relations=[]
    for a,c in [('GS','GSDA'),('GS','KO')]:
        ids=sorted(maps[a].keys() & maps[c].keys())
        x=[maps[a][i] for i in ids]; y=[maps[c][i] for i in ids]
        relations.append(dict(pair=a+'_'+c,n=len(ids),pearson=float(corr(x,y)),spearman=float(corr(ranks(x),ranks(y))),median_paired_delta_difference=st.median([u-v for u,v in zip(x,y)])))
    membership_proofs={}
    for key,rows in raw.items():
        ds=[math.log2(r[5]/r[7])-math.log2(r[4]/r[6]) for r in rows]
        syms=Counter(r[2] for r in rows)
        tests={'all_rows':lambda r:True,'finite_FE':lambda r:finite(r[8]),'nonduplicated_symbols_only':lambda r:syms[r[2]]==1,'common_literal_ids':lambda r:r[1] in common,'complex':lambda r:r[8]<-250,'simple':lambda r:r[8]>-20}
        membership_proofs[key]={k:proof([[str(i),r[1],str(r[2])] for i,r in enumerate(rows,2) if pred(r)]) for k,pred in tests.items()}
        membership_proofs[key]['symbol_mean_delta']=proof([[str(r[2]),str(i),r[1]] for i,r in enumerate(rows,2)])
        for universe in ['all_rows','finite_FE','nonduplicated_symbols_only','common_literal_ids','symbol_mean_delta']:
            if universe=='symbol_mean_delta':
                grouped=collections.defaultdict(list)
                for r,d in zip(rows,ds): grouped[str(r[2])].append(d)
                entries=[([symbol],st.mean(values)) for symbol,values in grouped.items()]
            else:
                entries=[([str(i),r[1],str(r[2])],d) for i,(r,d) in enumerate(zip(rows,ds),2) if tests[universe](r)]
            values=[d for ident,d in entries]; um,us=st.mean(values),st.pstdev(values)
            for sign in ['up','down']:
                membership_proofs[key]['universe_'+universe+'_'+sign]=proof([ident for ident,d in entries if ((d-um)/us>=1.5 if sign=='up' else (d-um)/us<=-1.5)])
        for stratum in ['complex','simple']:
            for universe in ['nonduplicated_symbols_only','common_literal_ids']:
                membership_proofs[key][stratum+'_'+universe]=proof([[str(i),r[1],str(r[2])] for i,r in enumerate(rows,2) if tests[stratum](r) and tests[universe](r)])
            membership_proofs[key][stratum+'_unique_symbols']=proof([[str(r[2])] for r in {str(r[2]):r for r in rows if tests[stratum](r)}.values()])
        m,sp,ss=st.mean(ds),st.pstdev(ds),st.stdev(ds)
        for version,zs in [('source',[r[12] for r in rows]),('sample',[(d-m)/ss for d in ds]),('population',[(d-m)/sp for d in ds])]:
            for sign in ['up','down']:
                for label,strict in [('strict',True),('inclusive',False)]:
                    selected=[[str(i),r[1],str(r[2])] for i,(r,z) in enumerate(zip(rows,zs),2) if ((z>1.5 if strict else z>=1.5) if sign=='up' else (z< -1.5 if strict else z<= -1.5))]
                    membership_proofs[key][version+'_'+sign+'_'+label]=proof(selected)
    return dict(status='ANALYSIS_COMPLETE_SCIENCE_DISCREPANCY_OPEN',contrasts=stats,variants=variants,structure=structure,matched_contrasts=relations,strict_inclusive_audit=threshold_checks,structure_universe_audit=structure_audit,boundaries=boundaries,duplicate_symbols=dup,memberships=memberships,membership_proofs=membership_proofs,source_transcribed={'caption_sd':{'GS':.226,'GSDA':.179,'KO':.273},'structure_reported_n':{'complex':1145,'simple':1036},'status':'source constants, not workbook discoveries; GS/GSDA correspondence unresolved'})

def compute(data):
    curves, bands, boundaries = [], [], []
    for direction in ['down', 'up', 'all']:
        rr = [r for r in data if direction == 'all' or r['direction'] == direction]
        previous = None
        for t in THRESHOLDS:
            threshold = Decimal(t)
            chosen = {r['gene_id'] for r in rr if r['q'] < threshold}
            curves.append(dict(direction=direction, threshold=t, count=len(chosen), selected_denominator=len(rr), retention=len(chosen)/len(rr), adjacent_jaccard=None if previous is None else len(previous & chosen)/len(previous | chosen)))
            below = [r['q'] for r in rr if r['q'] < threshold]
            above = [r['q'] for r in rr if r['q'] > threshold]
            boundaries.append(dict(direction=direction, threshold=t, equal=sum(r['q']==threshold for r in rr), nearest_below=str(max(below)) if below else '', nearest_above=str(min(above)) if above else '', within_10percent=sum(threshold*Decimal('.9') <= r['q'] <= threshold*Decimal('1.1') for r in rr), upper_window_censored=threshold*Decimal('1.1')>Decimal('.05')))
            previous = chosen
        for label, lo, hi in [('q<0.01', Decimal('0'), Decimal('.01')), ('0.01<=q<0.05', Decimal('.01'), Decimal('.05'))]:
            effects = [abs(r['effect']) for r in rr if lo <= r['q'] < hi]
            q1, med, q3 = [quantile(effects,p) for p in [.25,.5,.75]]
            bands.append(dict(direction=direction, band=label, n=len(effects), abs_log2_q1=float(q1), abs_log2_median=float(med), abs_log2_q3=float(q3), abs_log2_ge1=sum(x>=1 for x in effects), abs_log2_ge2=sum(x>=2 for x in effects), fraction_abs_log2_ge1=sum(x>=1 for x in effects)/len(effects), fraction_abs_log2_ge2=sum(x>=2 for x in effects)/len(effects)))
    ids=Counter(r['gene_id'] for r in data); symbols=Counter(r['gene_name'] for r in data)
    down={r['gene_id'] for r in data if r['direction']=='down'}; up={r['gene_id'] for r in data if r['direction']=='up'}
    ds={r['gene_name'] for r in data if r['direction']=='down'}; us={r['gene_name'] for r in data if r['direction']=='up'}
    audit=dict(rows=len(data), unique_ids=len(ids), duplicate_id_rows=sum(v-1 for v in ids.values()), malformed_literal_ids=sum(not bool(re.fullmatch(r'ENSG[0-9]{11}',r['gene_id'])) for r in data), missing_symbols=sum(not r['gene_name'] for r in data), duplicated_symbols={str(k):v for k,v in symbols.items() if v>1}, cross_direction_ids=sorted(down&up), cross_direction_symbols=sorted(ds&us), sign_conflicts=sum((r['effect']>=0 if r['direction']=='down' else r['effect']<=0) for r in data), nonfinite=sum(not math.isfinite(float(r[k])) for r in data for k in ['p','q','effect']), out_of_range=sum(not (0<=r['p']<=1 and 0<=r['q']<=1) for r in data), q_below_p=sum(r['q']<r['p'] for r in data), full_tested_universe=None, correction_algorithm=None, original_figure_membership=None)
    return curves,bands,boundaries,audit

def pdac(book):
    data=[]; direction=None
    for row,c in book['Table S1']:
        a=c.get('A') or ''
        if a.startswith('Supplementary Table S1A.'): direction='down'
        if a.startswith('Supplementary Table S1B.'): direction='up'
        if not a.startswith('ENSG'): continue
        data.append(dict(row=row,gene_id=a,gene_name=c.get('B'),direction=direction,p=Decimal(c['C']),q=Decimal(c['D']),effect=float(c['E'])))
    curves,bands,boundaries,audit=compute(data)
    collisions={sym:[dict(row=r['row'],gene_id=r['gene_id'],direction=r['direction']) for r in data if r['gene_name']==sym] for sym in audit['duplicated_symbols']}
    proofs={}
    for direction in ['down','up','all']:
        rr=[r for r in data if direction=='all' or r['direction']==direction]
        for t in THRESHOLDS:
            proofs[direction+'_'+t]=proof([[str(r['row']),r['gene_id']] for r in rr if r['q']<Decimal(t)])
        for label,lo,hi in [('q<0.01',Decimal(0),Decimal('.01')),('0.01<=q<0.05',Decimal('.01'),Decimal('.05'))]:
            chosen=[r for r in rr if lo<=r['q']<hi]
            proofs[direction+'_'+label]=proof([[str(r['row']),r['gene_id']] for r in chosen])
            for magnitude in [1,2]:
                proofs[direction+'_'+label+'_abs_ge'+str(magnitude)]=proof([[str(r['row']),r['gene_id']] for r in chosen if abs(r['effect'])>=magnitude])
    return dict(audit=audit,thresholds=curves,bands=bands,boundaries=boundaries,collision_anchors=collisions,membership_proofs=proofs)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study',required=True,choices=['ad','pd','pdac'])
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    expected=json.loads(Path(__file__).with_name('expectations.json').read_text(encoding='utf-8'))[a.study]
    replay.require(replay.sha(a.input)==expected['input_sha256'],'Input SHA256 mismatch')
    book=replay.read_book(a.input)
    fields,records,core=replay.analyze(a.study,book,expected)
    replay.require(replay.membership_digest(records)==expected['membership_sha256'],'Core membership/row-anchor mismatch')
    if a.study=='pd':
        for actual,target in zip(core['contrasts'],expected['counts']['contrasts']):
            for k,v in target.items():
                replay.require(math.isclose(actual[k],v,rel_tol=1e-12,abs_tol=1e-12) if isinstance(v,float) else actual[k]==v,'Core statistic mismatch: '+k)
    else: replay.require(core==expected['counts'],'Core count mismatch')
    result=globals()[a.study](book)
    # Output is created only after all input/core and numerical checks finish.
    replay.require(a.output.resolve()!=Path(__file__).resolve().parent,'Use a separate output directory')
    a.output.mkdir(parents=True,exist_ok=False)
    (a.output/'extensions.json').write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False),encoding='utf-8')
    with (a.output/'core_membership.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f); w.writerow(fields); w.writerows(records)
    print(json.dumps(dict(status='PASS',study=a.study,input_sha256=expected['input_sha256'],core_membership_sha256=expected['membership_sha256'])))

if __name__=='__main__': main()
