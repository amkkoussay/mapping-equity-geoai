# Zindi: component-specific residual probe

## Confirmed evidence
- Best public score: 0.084844078 (`01_span5_balanced`).
- Ridge submissions scored 0.085767868 and 0.085146032, worse than span5 despite optimistic local estimates.
- Prior analysis reports v2dev correlation with POI component ≈0.964 and with building gap ≈0.19.

## New hypothesis
The next improvement, if any, may come from an independent component-specific tract signal rather than more aggressive ridge. Building-gap deviations are the less redundant candidate; POI deviations are included as a comparison.

## Test design
Both candidates start from the current best `01_span5_balanced` and add only one component direction at quarter the amplitude of the existing probe. This is deliberately more conservative because the original component probes have extreme outliers.

- `04_building_component_probe.csv`: primary test; independent building-gap direction.
- `05_poi_component_probe.csv`: comparison test; POI direction, which may be partly redundant with the POI-heavy v2dev.

Each file contains 9,794 unique GEOIDs and predictions clipped to [0,1]. These are diagnostic probes, not candidates with a reliable local RMSE estimate. Submit 04 first; compare actual public score against 0.084844078. Submit 05 only if the remaining slot is still available and the comparison is useful. Keep the current best unchanged.
