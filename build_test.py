"""Build the allowlisted ZIP and cold-test external actual workbooks, stdlib only."""
import argparse
import copy
from decimal import Decimal
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

FILES=['README.md','LICENSE.txt','coverage.md','extensions.py','replay.py','expectations.json','reference.json','source_comparison.json','build_test.py']

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def proof(rows):
    return dict(n=len(rows),sha256=hashlib.sha256(json.dumps(sorted(rows),ensure_ascii=False,separators=(',',':')).encode()).hexdigest())

def compare(actual,expected,path='',stats=None):
    if stats is None: stats={'leaves':0,'float_leaves':0,'max_absolute_float_error':0.0}
    if isinstance(expected,dict):
        if not isinstance(actual,dict): raise AssertionError(path+': not an object')
        for k,v in expected.items():
            if k not in actual: raise AssertionError(path+'/'+k+': missing')
            compare(actual[k],v,path+'/'+k,stats)
    elif isinstance(expected,list):
        if path.endswith('/duplicate_audit'):
            actual=sorted(actual,key=lambda r:(r['treatment'],r['gene']))
            expected=sorted(expected,key=lambda r:(r['treatment'],r['gene']))
        if not isinstance(actual,list) or len(actual)!=len(expected): raise AssertionError(path+': list length')
        for i,(a,e) in enumerate(zip(actual,expected)): compare(a,e,path+'/'+str(i),stats)
    else:
        stats['leaves']+=1
        decimal_string=path.endswith(('/effect','/padj','/nearest_below','/nearest_above')) and expected not in ('',None)
        if decimal_string:
            x,y=Decimal(str(actual)),Decimal(str(expected))
            if abs(x-y)>max(Decimal('1e-25'),abs(y)*Decimal('2e-15')): raise AssertionError(path+': Decimal cell differs')
        elif isinstance(expected,float):
            if not isinstance(actual,(int,float)) or not math.isfinite(actual): raise AssertionError(path+': nonfinite/non-numeric')
            # stdlib compensated covariance vs NumPy BLAS reductions: 1e-12.
            # Boundary distances are much smaller, hence a separate 1e-14 absolute cap.
            atol=1e-14 if 'distance_to_' in path else 1e-12
            if not math.isclose(actual,expected,rel_tol=1e-12,abs_tol=atol): raise AssertionError(path+': '+repr(actual)+' != '+repr(expected))
            stats['float_leaves']+=1; stats['max_absolute_float_error']=max(stats['max_absolute_float_error'],abs(actual-expected))
        elif actual!=expected or (isinstance(expected,bool) and type(actual)!=bool): raise AssertionError(path+': exact value differs: '+repr(actual)+' != '+repr(expected))
    return stats

def normalized(study,data):
    data=copy.deepcopy(data)
    if study=='pd':
        data['memberships']=proof([[str(r[k]) for k in ['contrast','excel_row','id','geneSymbol','population_direction','source_direction']] for r in data['memberships']])
    return data

def run(script,study,workbook,output,cwd):
    return subprocess.run([sys.executable,'-I','-S','-B',str(script),'--study',study,'--input',str(workbook),'--output',str(output)],cwd=cwd,capture_output=True,text=True,timeout=180)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for s in ['ad','pd','pdac']: p.add_argument('--'+s,required=True,type=Path)
    p.add_argument('--work',required=True,type=Path,help='Writable local test/build directory; not a source directory')
    p.add_argument('--source-root',type=Path,help='Optional private source hash comparison; never bundled')
    p.add_argument('--build',action='store_true')
    a=p.parse_args(); here=Path(__file__).resolve().parent; a.work.mkdir(parents=True,exist_ok=True)
    target=a.work/'portable_extensions.zip'
    if a.build:
        # Explicit file allowlist; no workbooks, matrices, local logs or private paths.
        with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for name in sorted(FILES):
                data=(here/name).read_bytes()
                info=zipfile.ZipInfo(name,(2026,1,1,0,0,0)); info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=0o644<<16
                z.writestr(info,data,compresslevel=9)
    if not target.exists(): raise ValueError('Use --build or place portable_extensions.zip in --work')
    report={'status':'PASS','isolation':['-I','-S','-B'],'runtime':sys.version.split()[0],'tests':[],'zip_sha256':sha(target),'inventory':[]}
    with zipfile.ZipFile(target) as z:
        if z.testzip() is not None: raise AssertionError('ZIP CRC failed')
        assert sorted(z.namelist())==sorted(FILES)
        for name in sorted(z.namelist()):
            data=z.read(name)
            if (b'C:'+bytes([92])+b'Users'+bytes([92])) in data or (b'C:'+b'/'+b'Users'+b'/') in data: raise AssertionError('Personal absolute path leaked: '+name)
            report['inventory'].append(dict(filename=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
        with tempfile.TemporaryDirectory(prefix='cold_',dir=a.work) as tmp:
            cold=Path(tmp); code=cold/'code'; code.mkdir(); z.extractall(code)
            references=json.loads((code/'reference.json').read_text(encoding='utf-8'))
            if a.source_root:
                evidence=json.loads((code/'source_comparison.json').read_text(encoding='utf-8'))['reference_source_sha256']
                for name,digest in evidence.items():
                    assert sha(a.source_root/name)==digest,'Source changed since reference capture: '+name
                report['source_files_hash_checked']=len(evidence)
            for study in ['ad','pd','pdac']:
                inp=getattr(a,study).resolve(); output=cold/(study+'_output')
                result=run(code/'extensions.py',study,inp,output,cold)
                if result.returncode: raise AssertionError(study+': '+result.stderr)
                actual=json.loads((output/'extensions.json').read_text(encoding='utf-8'))
                stats=compare(normalized(study,actual),references[study],study)
                report['tests'].append(dict(study=study,test='external_workbook_extensions_vs_reviewed_outputs',status='PASS',**stats))
                if study=='pd':
                    assert len(actual['strict_inclusive_audit'])==18
                    assert all(x['membership_difference']==0 for x in actual['strict_inclusive_audit'])
                    assert actual['boundaries'][0]['id']=='uc008uhu.2' and actual['boundaries'][0]['excel_row']==689
                    assert actual['contrasts'][0]['population_up']==688 and actual['contrasts'][0]['source_up']==687
                # Deliberately corrupted real input: software negative control, not empirical data.
                bad=cold/(study+'_bad.bin'); bad.write_bytes(inp.read_bytes()+b'ARTIFICIAL_SHA_NEGATIVE_CONTROL')
                badout=cold/(study+'_bad_output'); failed=run(code/'extensions.py',study,bad,badout,cold)
                assert failed.returncode!=0 and 'Input SHA256 mismatch' in failed.stderr and not badout.exists()
                report['tests'].append(dict(study=study,test='artificial_bad_SHA_rejected_before_output_creation',status='PASS'))
                ep=code/'expectations.json'; original=ep.read_text(encoding='utf-8'); corrupted=json.loads(original)
                corrupted[study]['membership_sha256']='0'*64
                ep.write_text(json.dumps(corrupted),encoding='utf-8')
                gateout=cold/(study+'_core_gate_output')
                gate=run(code/'extensions.py',study,inp,gateout,cold)
                ep.write_text(original,encoding='utf-8')
                assert gate.returncode!=0 and 'Core membership/row-anchor mismatch' in gate.stderr and not gateout.exists()
                report['tests'].append(dict(study=study,test='artificial_core_expectation_corruption_rejected_before_output_creation',status='PASS'))
                # Artificial count-preserving identity corruption must fail exact digest comparison.
                mutated=normalized(study,actual)
                if study=='pd': mutated['memberships']['sha256']='0'*64
                else: mutated['membership_proofs'][next(iter(mutated['membership_proofs']))]['rows' if study=='ad' else 'sha256']=({'n':mutated['membership_proofs']['primary']['rows']['n'],'sha256':'0'*64} if study=='ad' else '0'*64)
                try: compare(mutated,references[study],study)
                except AssertionError: pass
                else: raise AssertionError('Artificial count-preserving identity mutation was not detected')
                report['tests'].append(dict(study=study,test='artificial_count_preserving_identity_corruption_rejected',status='PASS'))
            # Explicit isolated numerical fixtures; these are not empirical observations.
            spec=importlib.util.spec_from_file_location('cold_extensions',code/'extensions.py'); ext=importlib.util.module_from_spec(spec); spec.loader.exec_module(ext)
            assert ext.ranks([2,1,2,4])==[2.5,1.0,2.5,4.0]
            assert ext.quantile([0,10,20,30],.25)==7.5
            assert math.isclose(ext.corr([1,2,3],[3,2,1]),-1)
            assert not Decimal('.01')<Decimal('.01')
            assert Decimal('.00999999999999999999')<Decimal('.01')
            report['tests'].append(dict(test='artificial_ties_linear_quartile_correlation_Decimal_thresholds',status='PASS'))
    (a.work/'cold_test_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
