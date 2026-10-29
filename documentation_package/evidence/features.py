"""Per-tract Overture features for the Zindi Bias Bounty Mapping Equity Challenge.
Uses ONLY the challenge package (Overture extracts, ACS housing, strata). No reference layers.
"""
import duckdb, sys, os
REGIONS = ["maricopa-az", "northern-ca", "eastern-ok", "south-central-tx", "eastern-wa"]
FIRE = "('fire_department')"
EMS = "('ambulance_and_ems_services')"
SCHOOL = "('elementary_school','middle_school','high_school','school','private_school','public_school')"

con = duckdb.connect()
con.sql("LOAD spatial;")
con.sql("SET threads=2; SET memory_limit='5GB'; SET preserve_insertion_order=false;")

def run(r):
    d = f"data/{r}/{r}"
    out = f"feat/{r}.parquet"
    if os.path.exists(out):
        return
    con.sql(f"""CREATE OR REPLACE TABLE tr AS
        SELECT GEOID, geometry AS g, ST_Area(ST_Transform(geometry,'EPSG:4326','EPSG:5070',always_xy:=true))/1e6 AS area_km2
        FROM '{d}-census-tracts.parquet'""")
    # buildings: centroid of bbox -> tract (cheap, avoids reading polygons)
    con.sql(f"""CREATE OR REPLACE TABLE b AS
        SELECT t.GEOID, count(*) n_bldg,
               sum(CASE WHEN s.dataset='OpenStreetMap' THEN 1 ELSE 0 END) n_bldg_osm
        FROM (SELECT ST_Point((bbox.xmin+bbox.xmax)/2,(bbox.ymin+bbox.ymax)/2) p, sources[1] s
              FROM '{d}-overture-buildings.parquet') x
        JOIN tr t ON ST_Intersects(t.g, x.p) GROUP BY 1""")
    # roads: length by class, clipped to tract
    con.sql(f"""CREATE OR REPLACE TABLE rd AS
        SELECT t.GEOID,
          sum(CASE WHEN class IN ('motorway','trunk','primary','secondary') THEN km END) km_hwy,
          sum(km) km_road
        FROM (SELECT class, geometry g FROM '{d}-overture-roads.parquet') x
        JOIN tr t ON ST_Intersects(t.g, x.g),
        LATERAL (SELECT ST_Length(ST_Transform(ST_Intersection(t.g,x.g),'EPSG:4326','EPSG:5070',always_xy:=true))/1000 AS km)
        GROUP BY 1""")
    con.sql(f"""CREATE OR REPLACE TABLE po AS
        SELECT t.GEOID, count(*) n_poi,
          sum((categories.primary IN {FIRE})::INT) n_fire,
          sum((categories.primary IN {EMS})::INT) n_ems,
          sum((categories.primary IN {SCHOOL})::INT) n_school
        FROM '{d}-overture-pois.parquet' x JOIN tr t ON ST_Intersects(t.g, x.geometry) GROUP BY 1""")
    con.sql(f"""CREATE OR REPLACE TABLE inf AS
        SELECT t.GEOID, count(*) n_infra FROM '{d}-overture-infrastructure.parquet' x
        JOIN tr t ON ST_Intersects(t.g, x.geometry) GROUP BY 1""")
    acs_cols = [c[0] for c in con.sql(f"DESCRIBE SELECT * FROM '{d}-census-acs-housing.parquet'").fetchall()]
    hu = "housing_units"
    con.sql(f"""COPY (
        SELECT tr.GEOID, '{r}' region, tr.area_km2, a.hu,
          coalesce(n_bldg,0) n_bldg, coalesce(n_bldg_osm,0) n_bldg_osm,
          coalesce(km_hwy,0) km_hwy, coalesce(km_road,0) km_road,
          coalesce(n_poi,0) n_poi, coalesce(n_fire,0) n_fire, coalesce(n_ems,0) n_ems,
          coalesce(n_school,0) n_school, coalesce(n_infra,0) n_infra
        FROM tr
        LEFT JOIN (SELECT GEOID, "{hu}"::DOUBLE hu FROM '{d}-census-acs-housing.parquet') a USING (GEOID)
        LEFT JOIN b USING (GEOID) LEFT JOIN rd USING (GEOID) LEFT JOIN po USING (GEOID) LEFT JOIN inf USING (GEOID)
    ) TO '{out}' (FORMAT parquet)""")
    print(r, "done", flush=True)

os.makedirs("feat", exist_ok=True)
for r in (sys.argv[1:] or REGIONS):
    run(r)
