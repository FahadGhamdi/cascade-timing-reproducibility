"""Read-only independent audit; never unpickle models or execute uploaded scripts."""
import argparse, collections, csv, hashlib, json
from pathlib import Path

def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--return-dir',type=Path,required=True); ap.add_argument('--originals',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args()
    p=a.return_dir; w=a.originals
    read=lambda q:json.loads(q.read_text())
    m=read(p/'RETURN_MANIFEST.json'); errors=[]
    for n,r in m.items():
        q=p/n
        if not q.is_file() or q.stat().st_size!=r['bytes'] or sha(q)!=r['sha256']: errors.append(['manifest',n])
    source_to_local={r['source']:p/n for n,r in m.items()}
    rows=read(p/'audit/FILE_COMPARISONS.json'); counts=collections.Counter(); direct=[]
    large={r['path']:r for r in read(p/'return_bundle/LARGE_OUTPUT_SHA256.json')}
    timing={'end_utc','fit_seconds','prediction_scoring_seconds','seconds','started_utc','time','total_seconds','wall_seconds'}
    def strip(v):
        if isinstance(v,dict): return {k:strip(x) for k,x in v.items() if k not in timing}
        if isinstance(v,list): return [strip(x) for x in v]
        return v
    for r in rows:
        if 'historical_path' not in r:
            counts['comparison_report_only']+=1
            if not r['passed_scientific_comparison']: errors.append(['reported_comparison_failed',r['scope']])
            continue
        old=w/r['historical_path'].split('/REPRO_ORIGINALS_20260921/')[1]
        if 'historical_sha256' in r:
            counts['historical_hash_checked']+=1
            if sha(old)!=r['historical_sha256']: errors.append(['historical_hash',r['scope']])
        elif r.get('byte_equal') and r['replayed_path'] in large:
            counts['reported_large_digest_equals_original_checked']+=1
            if sha(old)!=large[r['replayed_path']]['sha256']: errors.append(['large_hash',r['scope']])
        else: counts['comparison_report_only']+=1
        new=source_to_local.get(r['replayed_path'])
        if new:
            counts['replayed_files_available']+=1
            if 'replayed_sha256' in r and sha(new)!=r['replayed_sha256']: errors.append(['replayed_hash',r['scope']])
            if new.suffix=='.json':
                same=strip(read(old))==strip(read(new)); counts['json_exact_excluding_timing' if same else 'json_difference']+=1
                if not same: errors.append(['non_time_json_difference',r['scope']])
            elif old.read_bytes()!=new.read_bytes(): errors.append(['other_included_difference',r['scope']])
        else: counts['replayed_files_represented_by_digest_only']+=1
        if not r['passed_scientific_comparison']: errors.append(['reported_comparison_failed',r['scope']])
    stages={}
    for stage,jobdir in [('train','jobs'),('test','jobs'),('noise','noise_jobs')]:
        reports=[read(q) for q in (p/'evidence'/stage/jobdir).glob('*/JOB_REPORT.json')]
        stages[stage]={'reports':len(reports),'statuses':dict(collections.Counter(x.get('status') for x in reports)),**{k:sum(x.get(k,0) for x in reports) for k in ['score_attempts','score_successes','score_failures','component_fit_calls']}}
    selected=read(p/'SELECTED_MODEL_IDENTITY.json')['models']
    for r in selected:
        q=w/'13E/run/jobs'/r['job_id']/'MODEL.joblib'
        if sha(q)!=r['sha256'] or q.stat().st_size!=r['bytes']: errors.append(['selected_historical_model',r['job_id']])
    differences=list(csv.DictReader((p/'audit/FIELD_DIFFERENCES.csv').open()))
    report={'status':'PASS' if not errors else 'FAIL','manifest_entries_verified':len(m),'comparison_records':len(rows),'comparison_verification':dict(counts),'selected_model_reported_digests_checked_against_original_bytes':len(selected),'new_large_model_bytes_received':False,'difference_categories':dict(collections.Counter(r['category'] for r in differences)),'stage_counts_from_job_reports':stages,'errors':errors,'scope':'Independent verification of attached evidence and original bytes; new large Mac outputs represented by local-run digests, not independently read here.'}
    a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
    if errors: raise SystemExit(1)

if __name__=='__main__': main()
