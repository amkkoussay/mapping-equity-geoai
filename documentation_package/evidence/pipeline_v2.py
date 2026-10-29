"""Bias Bounty Mapping Equity Challenge - pipeline v2 (Koussay Mehdouani).

Component-wise coverage-gap estimate per Census tract, using ONLY the challenge package:
  * Overture extracts (buildings, roads, places)  -> feat/<region>.parquet via features.py
  * strata tract table (ALAND, pop_total, usfs_BuildingCount_sum, ...)
  * ACS housing units (used only as a sanity check / edge-case flag, never as a denominator for buildings)
No TIGER, Microsoft Building Footprints, USGS National Map facilities or CBP data are read.

Run:  python features.py && python pipeline_v2.py
Deterministic: no randomness, no training.
"""
import numpy as np, pandas as pd, json, sys

REGIONS = ["maricopa-az", "northern-ca", "eastern-ok", "south-central-tx", "eastern-wa"]
P = dict(                       # every tunable constant, in one place
    ROAD_CONST=0.05,            # transport gap assigned when a named highway is present in Overture
    WATER_FRAC=0.5,             # tract is "water-dominated" above this water share of total area
    ALPHA=0.25,
    BUILDING_REF="usfs",        # "usfs" = strata usfs_BuildingCount_sum; "none" = v1 proxy (buildings per HU vs regional median)                 # weight on the tract estimate; (1-ALPHA) on the regional mean (shrinkage)
    W=dict(transport=1.0, building=1.0, poi=1.0),   # component weights in the composite
)
STRATA = ["GEOID", "ALAND", "pop_total", "ur_class", "svi_overall", "cvi_overall",
          "tribal_any", "usfs_BuildingCount_sum"]

def clip01(x):
    return np.clip(x, 0.0, 1.0)

def load():
    f = pd.concat([pd.read_parquet(f"feat/{r}.parquet") for r in REGIONS], ignore_index=True)
    s = pd.concat([pd.read_parquet(f"data/{r}/{r}-strata-tract-table.parquet", columns=STRATA)
                   for r in REGIONS], ignore_index=True)
    sample = pd.concat([pd.read_csv(f"data/{r}/{r}-sample-submission.csv", dtype={"GEOID": str})[["GEOID"]]
                        for r in REGIONS], ignore_index=True)
    d = sample.merge(f, on="GEOID", how="left").merge(s, on="GEOID", how="left")
    assert d.region.notna().all(), "tract missing from Overture features"
    return d

def flags(d):
    total_m2 = d.area_km2 * 1e6
    d["water_frac"] = clip01(1 - d.ALAND.fillna(total_m2) / total_m2)
    d["is_water"] = d.water_frac > P["WATER_FRAC"]
    d["is_zero_pop"] = (d.pop_total.fillna(0) == 0) | (d.hu.fillna(0) == 0)
    d["no_overture"] = (d.n_bldg == 0) & (d.n_poi == 0) & (d.km_road == 0)
    return d

def building(d):
    if P["BUILDING_REF"] == "none":
        r = d.n_bldg / d.hu.clip(lower=1)
        return clip01(1 - r / r.groupby(d.region).transform("median"))
    ref = d.usfs_BuildingCount_sum              # structure count shipped in the strata table
    g = clip01(1 - d.n_bldg / ref.where(ref > 0))
    return g.where(ref > 0)                     # undefined: no reference structures

def transport(d):
    # Without the named-highway reference we can only see presence. Present -> small constant;
    # absent -> undefined (most such tracts have no named highway in the reference either).
    return pd.Series(np.where(d.km_hwy > 0, P["ROAD_CONST"], np.nan), index=d.index)

def poi(d):
    hu = d.hu.clip(lower=1)
    exp_school, exp_fire = d.hu / 1500, d.hu / 4000
    g_school = np.where(exp_school >= 0.5, clip01(1 - d.n_school / exp_school), np.nan)
    g_fire = np.where(exp_fire >= 0.5, clip01(1 - d.n_fire / exp_fire), np.nan)
    with np.errstate(all="ignore"):
        fac = np.nanmean(np.vstack([g_school, g_fire]), axis=0)
    ratio = d.n_poi / hu
    est = clip01(1 - ratio / ratio.groupby(d.region).transform("median"))
    est = est.where(~d.is_zero_pop)             # no residents -> establishments half undefined
    with np.errstate(all="ignore"):
        return pd.Series(np.nanmean(np.vstack([fac, est]), axis=0), index=d.index)

def composite(d):
    C = pd.DataFrame({k: d[f"{k}_gap"] * w for k, w in P["W"].items()})
    W = pd.DataFrame({k: d[f"{k}_gap"].notna() * w for k, w in P["W"].items()})
    raw = C.sum(axis=1, min_count=1) / W.sum(axis=1).replace(0, np.nan)
    # edge cases with every component undefined
    reg_mean = raw.groupby(d.region).transform("mean")
    raw = raw.fillna(reg_mean)
    raw = np.where(d.no_overture & ~d.is_water & ~d.is_zero_pop, 1.0, raw)   # people live there, nothing mapped
    raw = pd.Series(raw, index=d.index)
    return clip01(P["ALPHA"] * raw + (1 - P["ALPHA"]) * raw.groupby(d.region).transform("mean")), raw

def main(out="submission_v2.csv"):
    d = flags(load())
    d["building_gap"], d["transport_gap"], d["poi_gap"] = building(d), transport(d), poi(d)
    d["coverage_gap_score"], d["raw_score"] = composite(d)
    sub = d[["GEOID", "coverage_gap_score"]]
    assert len(sub) == sub.GEOID.nunique() and sub.coverage_gap_score.notna().all()
    sub.to_csv(out, index=False)
    d.to_parquet("v2_tracts.parquet")
    summary = {
        "tracts": int(len(d)),
        "edge_cases": {k: int(d[k].sum()) for k in ["is_water", "is_zero_pop", "no_overture"]},
        "undefined_share": {c: round(float(d[c].isna().mean()), 3) for c in ["transport_gap", "building_gap", "poi_gap"]},
        "params": P,
    }
    json.dump(summary, open("v2_summary.json", "w"), indent=1)
    print(json.dumps(summary, indent=1))
    print(d.groupby("region")[["building_gap", "transport_gap", "poi_gap", "raw_score", "coverage_gap_score"]].mean().round(3))

if __name__ == "__main__":
    # usage: python pipeline_v2.py [out.csv] [BUILDING_REF] [ALPHA]
    a = sys.argv[1:]
    if len(a) > 1: P["BUILDING_REF"] = a[1]
    if len(a) > 2: P["ALPHA"] = float(a[2])
    main(*a[:1])
