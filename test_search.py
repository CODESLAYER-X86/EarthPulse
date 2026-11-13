import asf_search as asf

print("Testing granule search...")
results = asf.search(granule_as_list=['NISAR_L2_PR_GCOV_033_139_D_050_0005_NASV_A_20261021T201350_20261021T201413_P05023_N_P_J_001'])
print("Exact granule search found:", len(results))

# Let's try wildcard search using granule parameter
results_wildcard = asf.search(granule_as_list=['NISAR_L2_PR_GCOV_03*_139_D_050*'])
print("Wildcard granule search found:", len(results_wildcard))

# Let's try searching by platform and processingLevel without frame constraint, just relativeOrbit=139
results_orbit = asf.search(platform='NISAR', processingLevel='GCOV', relativeOrbit=139)
print("Orbit 139 search found:", len(results_orbit))
for r in results_orbit:
    print(r.properties.get('fileName'), r.properties.get('frameNumber'))
