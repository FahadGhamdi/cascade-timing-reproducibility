#!/usr/bin/env python3
"""New orchestration only. Original scientific sources are never patched.
Frozen-parent stage replay is distinct from refit-to-test reproduction.
"""
import argparse,contextlib,csv,gzip,itertools,hashlib,importlib.metadata,json,math,os,shutil,stat,subprocess,sys,time,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
ENV={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','MPLBACKEND':'Agg'}
os.environ.update(ENV)
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def safe(n):
 p=PurePosixPath(n);require(not p.is_absolute() and '..' not in p.parts and 'old' not in p.parts and '\\' not in n,'Unsafe member '+n)
def unpack(p,d,expected=None):
 d.mkdir(parents=True,exist_ok=False)
 with zipfile.ZipFile(p) as z:
  names=z.namelist();require(len(names)==len(set(names)),'Duplicate members')
  m=expected if expected is not None else read_zip(z,'MANIFEST.json')
  require(set(names)==set(m) if expected is not None else set(names)==set(m)|{'MANIFEST.json'},'Archive member set mismatch')
  for inf in z.infolist():
   safe(inf.filename);require(not stat.S_ISLNK(inf.external_attr>>16),'Symlink rejected')
   dest=d/inf.filename;dest.parent.mkdir(parents=True,exist_ok=True)
   with z.open(inf) as r,dest.open('xb') as w:shutil.copyfileobj(r,w,1048576)
   if inf.filename in m:
    v=m[inf.filename];require(dest.stat().st_size==v['bytes'] and sha(dest)==v['sha256'],'Member hash mismatch '+inf.filename)
def read_zip(z,n):return json.loads(z.read(n))
def verify_tree(root):
 count=0
 for m in (root/'manifests').glob('*.json'):
  data=read(m);base=root/data['base']
  for n,v in data['files'].items():
   p=base/n;require(p.is_file() and p.stat().st_size==v['bytes'] and sha(p)==v['sha256'],'Restored file changed '+str(p));count+=1
 return count
def restore(assets,work):
 require(not work.exists(),'Restore requires a new workspace')
 work.mkdir(parents=True);(work/'manifests').mkdir();idx=read(ROOT/'DISTRIBUTION_INDEX.json')
 for a in idx['payloads']:
  p=assets/a['archive'];require(p.is_file(),'Missing payload '+str(p))
  require(p.stat().st_size==a['bytes'] and sha(p)==a['sha256'],'Payload differs from historical index')
  dest=work/a['archive'].replace('.zip','');unpack(p,dest,a['members'])
  write(work/'manifests'/(a['archive']+'.json'),{'base':dest.name,'files':a['members']})
 paths={}
 for stage in ['13A','13B','13E','13F','14']:
  hits=list(work.glob('ORIGINALS_PAYLOAD_*/originals/**/BRACE_PHASE'+stage+'_RETURN*.zip'))
  require(len(hits)==1,'Ambiguous/missing original archive '+stage)
  dest=work/stage;unpack(hits[0],dest)
  write(work/'manifests'/(stage+'.json'),{'base':stage,'files':read(dest/'MANIFEST.json')})
  paths[stage+'_archive']=str(hits[0].relative_to(work))
 hits=list(work.glob('ORIGINALS_PAYLOAD_*/originals/BRACE_Phase13B_Kit_*.zip'));require(len(hits)==1,'Missing 13B kit')
 unpack(hits[0],work/'13B-kit');write(work/'manifests/13B-kit.json',{'base':'13B-kit','files':read(work/'13B-kit/MANIFEST.json')})
 paths['weibo']=str(next(work.glob('ORIGINALS_PAYLOAD_*/originals/**/dataset_weibo_deephawkes.txt')).relative_to(work))
 write(work/'PATHS.json',paths);print('Restored original bytes. No experiments executed.')
def environment(work):
 lock=work/'13E/source/vendor/requirements.lock.txt';mismatch=[];observed={}
 for line in lock.read_text().splitlines():
  if not line.strip() or line.startswith('#'):continue
  n,want=line.split('==')
  try:got=importlib.metadata.version(n)
  except importlib.metadata.PackageNotFoundError:got=None
  observed[n]={'expected':want,'observed':got}
  if got!=want:mismatch.append(n)
 return {'python':sys.version,'python_3_12':sys.version_info[:2]==(3,12),'packages':observed,'mismatches':mismatch,'passed':not mismatch and sys.version_info[:2]==(3,12)}
def compare(a,b,path='$'):
 if isinstance(a,dict):
  require(isinstance(b,dict) and set(a)==set(b),'Keys '+path)
  for k in a:compare(a[k],b[k],path+'/'+k)
 elif isinstance(a,list):
  require(isinstance(b,list) and len(a)==len(b),'Length '+path)
  for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i))
 elif isinstance(a,(int,float)) and not isinstance(a,bool):
  require(isinstance(b,(int,float)) and math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-8),'Number '+path)
 else:require(a==b,'Value '+path)
def compare_results(new,old,names):
 for n in names:
  a=new/n;b=old/n
  if n.endswith('.json'):compare(read(b),read(a),n)
  elif n.endswith('.npz'):
   import numpy as np
   with np.load(b,allow_pickle=False) as x,np.load(a,allow_pickle=False) as y:
    require(set(x.files)==set(y.files),'NPZ keys '+n)
    for k in x.files:require(x[k].shape==y[k].shape and np.allclose(x[k],y[k],atol=1e-8,rtol=1e-10,equal_nan=True),'NPZ array '+n+'/'+k)
  elif n.endswith(('.csv','.csv.gz')):
   op=gzip.open if n.endswith('.gz') else open
   with op(b,'rt',newline='') as x,op(a,'rt',newline='') as y:
    for i,(r,t) in enumerate(itertools.zip_longest(csv.reader(x),csv.reader(y))):
     require(r is not None and t is not None and len(r)==len(t),'CSV structure '+n)
     for j,(v,w) in enumerate(zip(r,t)):
      if v==w:continue
      try:fv,fw=float(v),float(w)
      except ValueError:raise RuntimeError('CSV text '+n+'/'+str(i)+'/'+str(j))
      require(math.isclose(fv,fw,rel_tol=1e-10,abs_tol=1e-8),'CSV numeric '+n+'/'+str(i)+'/'+str(j))
  else:raise ValueError(n)
 return {'files':names,'passed':True,'atol':1e-8,'rtol':1e-10}
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('stage',choices=['restore','verify','environment','raw','primary','supplement','reporting','check-all','train','test','noise'])
 ap.add_argument('--assets',type=Path);ap.add_argument('--work',type=Path,required=True);ap.add_argument('--out',type=Path)
 a=ap.parse_args();work=a.work.resolve()
 require(not sys.flags.optimize,'Do not run with -O')
 if a.stage=='restore':require(a.assets is not None,'--assets required');restore(a.assets.resolve(),work);return
 count=verify_tree(work)
 if a.stage=='verify':print(json.dumps({'verified_files':count}));return
 if a.stage=='environment':print(json.dumps(environment(work),indent=2));return
 require(a.out is not None,'--out required');out=a.out.resolve()
 require(out!=work and work not in out.parents,'Output must be outside immutable restored workspace')
 require(out!=ROOT and ROOT not in out.parents,'Output must be outside controller directory')
 out.mkdir(parents=True,exist_ok=False)
 report={'stage':a.stage,'verified_files':count,'steps':[],'status':'started','full_refit_to_test_reproduction':False,'interpretation':'Frozen-parent stage replay; original locks preserved.'}
 def run(name,cmd,cwd=None):
  print('RUNNING',name,flush=True);t=time.monotonic()
  with (out/(name+'.log')).open('x') as h:p=subprocess.run([str(x) for x in cmd],cwd=cwd,env=ENV,stdout=h,stderr=subprocess.STDOUT)
  report['steps'].append({'name':name,'seconds':time.monotonic()-t,'returncode':p.returncode});write(out/'RUN_REPORT.json',report)
  require(p.returncode==0,'Failed '+name+'; inspect preserved log')
 paths=read(work/'PATHS.json');py=sys.executable
 try:
  if a.stage in ['raw','check-all']:
   kit=work/'13B-kit'
   run('raw',[py,kit/'prepare_phase13b.py','--weibo',work/paths['weibo'],'--seismic-index',kit/'data/seismic_index.csv','--seismic-data',kit/'data/seismic_data.csv','--out',out/'prepared'])
   expected=read(kit/'reference/PORTABLE_CONTENT_MANIFEST.json');got=read(out/'prepared/PORTABLE_CONTENT_MANIFEST.json')
   require(got==expected,'Raw preparation content differs');report['raw_preparation']={'passed':True,'portable_entries':len(expected)}
  if a.stage in ['primary','check-all']:
   dest=out/'primary';dest.mkdir();shutil.copytree(work/'13F/run/jobs',dest/'jobs')
   print('RUNNING primary (unchanged original function)',flush=True)
   started=time.monotonic();sys.path.insert(0,str(work/'13F/source'))
   from analyze_test import run as original_primary
   # Transport-only workaround: flush gzip text output periodically. The original
   # analysis function, rows, numerical operations and inputs remain unchanged.
   saved_open=gzip.open
   class FlushedWriter:
    def __init__(self,stream):self.stream=stream;self.calls=0
    def write(self,text):
     result=self.stream.write(text);self.calls+=1
     if self.calls%128==0:self.stream.flush()
     return result
    def __enter__(self):return self
    def __exit__(self,*exc):return self.stream.__exit__(*exc)
    def __getattr__(self,name):return getattr(self.stream,name)
   def output_open(filename,mode='rb',*args,**kwargs):
    stream=saved_open(filename,mode,*args,**kwargs)
    return FlushedWriter(stream) if 'w' in mode and 't' in mode else stream
   gzip.open=output_open
   try:original_primary(work/'13F/source',dest)
   finally:gzip.open=saved_open
   report['gzip_output_adapter']='flush every 128 text writes; uncompressed output compared to original'
   report['steps'].append({'name':'primary','seconds':time.monotonic()-started,'returncode':0,'execution':'unchanged original function in process'})
   names=['PRIMARY_COMPARISONS.json','PROCEDURE_METRICS.json','CALIBRATION.json','DUPLICATE_SENSITIVITY.json','BOOTSTRAP_DESIGN.json','BOOTSTRAP_DELTAS.csv.gz','ROOT_PROCEDURE_SCORES.csv.gz']
   report['primary_comparison']=compare_results(dest/'analysis',work/'13F/run/analysis',names)
  if a.stage in ['supplement','check-all']:
   run('strata',[py,work/'14/source/strata14.py','--parent',work/'13F','--out',out/'stage_a'])
   report['strata_comparison']=compare_results(out/'stage_a',work/'14/run/stage_a',['STRATA_RESULTS.json','CASE_METADATA.json','BOOTSTRAP_DESIGN.json','STRATA_BOOTSTRAP.npz','MSLE_SAVED_MEDIANS.csv','STRATUM_LEVELS.csv','EMPIRICAL_REFERENCES_BY_STRATUM.csv','PROCEDURE_LOSSES.npz'])
   run('noise_analysis',[py,work/'14/source/analyze_noise14.py','--stage-a',out/'stage_a','--jobs',work/'14/run/noise_jobs','--out',out/'stage_b'])
   report['noise_comparison']=compare_results(out/'stage_b',work/'14/run/stage_b',['NOISE_COMPARISONS.json','NOISE_BOOTSTRAP.npz','NOISE_MATRIX_BINDINGS.json','NOISE_REALIZATION_SUMMARIES.csv','NOISE_PROCEDURE_LOSSES.npz','PROCEDURE_COMPLETENESS.json'])
  if a.stage in ['reporting','check-all']:
   paper=out/'paper';shutil.copytree(ROOT/'paper',paper)
   # Bind publication evidence to the actual uploaded original archives before rendering.
   for n in ['PRIMARY_COMPARISONS.json','PROCEDURE_METRICS.json','CALIBRATION.json','DUPLICATE_SENSITIVITY.json']:
    compare(read(work/'13F/run/analysis'/n),read(paper/'support/evidence'/n),n)
   for n,stage in [('STRATA_RESULTS.json','stage_a'),('NOISE_COMPARISONS.json','stage_b')]:
    compare(read(work/'14/run'/stage/n),read(paper/'support/evidence/phase14'/n),n)
   report['paper_evidence_bound_to_originals']=True
   for n in ['verify_reporting','make_publication_figures','make_graphical_abstract']:
    run(n,[py,paper/'support'/(n+'.py')])
  if a.stage in ['train','test','noise']:
   env=environment(work);write(out/'ENVIRONMENT_CHECK.json',env);require(env['passed'],'Exact historical dependencies required; see ENVIRONMENT_CHECK.json. No training launched.')
   if a.stage=='train':cmd=[py,work/'13E/source/run_phase13e.py','--out',out/'run']
   elif a.stage=='test':cmd=[py,work/'13F/source/run_phase13f.py','--phase13e-return',work/paths['13E_archive'],'--out',out/'run']
   else:cmd=[py,work/'14/source/run_phase14.py','--phase13f-return',work/paths['13F_archive'],'--out',out/'run']
   run(a.stage,cmd)
   if a.stage=='train':
    ref=read(work/'13E/run/MODEL_LOCK.json');new=read(out/'run/MODEL_LOCK.json')
    report['model_lock_byte_equal']=sha(work/'13E/run/MODEL_LOCK.json')==sha(out/'run/MODEL_LOCK.json')
    report['training_note']='Compare all selections, failure counts and predictions separately. A completed runner is not evidence of identical refits.'
   if a.stage=='test':report['test_comparison']=compare_results(out/'run/analysis',work/'13F/run/analysis',['PRIMARY_COMPARISONS.json','PROCEDURE_METRICS.json','CALIBRATION.json'])
   if a.stage=='noise':report['noise_comparison']=compare_results(out/'run/stage_b',work/'14/run/stage_b',['NOISE_COMPARISONS.json','NOISE_BOOTSTRAP.npz'])
  report['source_files_verified_after']=verify_tree(work);report['status']='completed_training_requires_review' if a.stage=='train' else 'passed'
 except BaseException as e:
  report['status']='failed';report['error']=str(e);raise
 finally:write(out/'RUN_REPORT.json',report)
 print('Completed',out)
if __name__=='__main__':main()
