# tests/samples/

Intentionally empty of data. The measured samples (sample_107_direct_urls.json,
sample_30_keyword.json, sample_50_explore.json, distribution_107.csv) contain raw
Facebook event data — organiser names, descriptions — and per DEC-102 / DEC-104 they
are not committed to this repository. They live in the release package on Drive:
QN Hub → 20 Packages → Events 1.4.5.

To run the distribution analysis, download a sample locally and pass its path:

    cd gazetteer
    python ../tests/zone_distribution.py /path/to/sample_107_direct_urls.json

`test_guards.py` needs no sample — its 38 checks are self-contained.
