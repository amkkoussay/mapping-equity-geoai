"""exp-v7 — H1: POI CALIBRATION VARYING WITH SETTLEMENT DENSITY (قصي, 2026-10-28).
yhat = a + [s0 + alpha*tanh(z/tau)] * P.  z built ONLY from package columns
(external ACS/USDA/Overture material motivated the hypothesis; per protocol it
never enters the model or the evaluation).
PRIMARY TEST (pre-registered): P = scored POI probe vector (board 0.08483727).
z in {log building density, log housing density, mix}. a = mean-preserving.
Selection on seeds (7,123) with maxcoef<=2.5; single winner -> FRESH validation
(999,31337) vs frozen s0.6 baseline (screen 0.0804; fresh halves max 0.0815).
Sensitivity (reported, not cherry-picked): P = raw poi_gap column."""
import pandas as pd, numpy as np, sys, itertools
sys.path.insert(0,'work29')
import evaluator as ev
F = ev.F; S2 = np.asarray(ev.S2)
t = pd.read_parquet('max-gamble-pack/scored/v2_tracts.parquet').set_index('GEOID').loc[F.index]
poi_probe = pd.Series(F['upload28b/staged/05_poi_component_probe.csv'].values, index=F.index)
def proj_coefs(y, Fm):
    A=Fm.values; k=A.shape[1]; M=np.zeros((k+1,k+1)); M[:k,:k]=A.T@A; M[:k,k]=1; M[k,:k]=1
    return np.linalg.lstsq(M, np.r_[A.T@y,1.0], rcond=None)[0][:k]
def screen_on(Fm,y):
    Gh=(Fm.T@Fm).values/len(Fm); Dh=np.diag(Gh).copy(); c=proj_coefs(y,Fm); c=c/c.sum()
    pc=float(np.sqrt(max(c@Gh@c-c@Dh+c@S2,0))); rr=y-Fm.values@c
    return float(np.sqrt(pc**2+(rr**2).mean())), float(np.abs(c).max())
def guarded(v, seeds):
    v=pd.Series(np.asarray(v),index=F.index).clip(0,1); y=v.values
    approx,mc=screen_on(F,y); halves=[]
    for seed in seeds:
        idx=np.random.default_rng(seed).permutation(len(F))
        for mask in (idx[:4897],idx[4897:]): halves.append(screen_on(F.iloc[mask],y[mask])[0])
    halves=np.array(halves)
    ok=bool(mc<=2.5 and halves.max()-halves.min()<=0.008 and (halves<0.0848).all())
    return dict(approx=round(approx,4),maxcoef=round(mc,2),halves=[round(h,4) for h in halves],ok=ok)
def zstd(x): return (x-x.mean())/x.std()
area = t['area_km2'].clip(lower=0.05)
Z = {'bldg': zstd(np.log1p(t['n_bldg']/area)), 'hous': zstd(np.log1p(t['hu']/area))}
Z['mix'] = (Z['bldg']+Z['hous'])/2
def build(P, z, s0, alpha, tau):
    s = s0 + alpha*np.tanh(z/tau)
    y = s*P
    a = P.mean() - y.mean()
    return y + a
attempts=[]; best_per_z={}
def run_family(P, label):
    print(f'== family {label} ==', flush=True)
    for zn, z in Z.items():
        ref = None; best = None
        for s0, alpha, tau in itertools.product([0.8,0.9,1.0,1.1],[0.0,-0.4,-0.2,-0.1,0.1,0.2,0.4],[1.0]):
            pass
        for s0, alpha, tau in itertools.product([0.8,0.9,1.0,1.1],[-0.4,-0.2,-0.1,0.1,0.2,0.4],[0.5,1.0,2.0]):
            r = guarded(build(P, z.values, s0, alpha, tau), (7,123))
            r.update(family=label, z=zn, s0=s0, alpha=alpha, tau=tau); attempts.append(r)
            if r['ok'] and (best is None or r['approx']<best['approx']): best = r
        for s0 in [0.8,0.9,1.0,1.1]:
            r = guarded(build(P, z.values, s0, 0.0, 1.0), (7,123))
            r.update(family=label, z=zn, s0=s0, alpha=0.0, tau=None); attempts.append(r)
            if r['ok'] and (ref is None or r['approx']<ref['approx']): ref = r
        print(f'z={zn}: affine ref={ref["approx"] if ref else None} (s0={ref["s0"] if ref else "-"}) | best modulated={best}', flush=True)
        if label=='probe' and best: best_per_z[zn]=best
run_family(poi_probe, 'probe')
run_family(t['poi_gap'].fillna(t['poi_gap'].groupby(t['region']).transform('mean')), 'rawgap')
pd.DataFrame(attempts).to_csv('exp-v7/attempts.csv', index=False)
# winner -> fresh validation + region stability
if best_per_z:
    w = min(best_per_z.values(), key=lambda r: r['approx'])
    print('WINNER:', w, flush=True)
    vec = build(poi_probe, Z[w['z']].values, w['s0'], w['alpha'], w['tau'])
    rf = guarded(vec, (999,31337))
    verdict = bool(rf['ok'] and max(rf['halves'])<=0.0815 and rf['approx']<0.0804)
    print('FRESH validation:', rf, '=> ACCEPTED' if verdict else '=> REJECTED', flush=True)
    prof = pd.DataFrame({'P_mean': poi_probe.groupby(t['region']).mean(), 'H1_mean': pd.Series(np.clip(vec,0,1),index=F.index).groupby(t['region']).mean()})
    print(prof.round(4).to_string(), flush=True)
    if verdict: pd.Series(np.clip(vec,0,1),index=F.index).to_frame('coverage_gap_score').rename_axis('GEOID').to_csv('exp-v7/candidates/h1_winner.csv')
print('DONE exp-v7;', len(attempts), 'attempts')
