from runregcrawlr.runinfo import RunInfo


def test_get_single_run():
    runinfo = RunInfo()
    runs = runinfo.get_runs(run_number=315543)
    assert 1 == len(runs)
    assert 37941.37109375 == runs[0]["run_lumi"]
    assert 36726.3984375 == runs[0]["run_live_lumi"]
    assert 180 == runs[0]["lumisections"]
    assert 6633 == runs[0]["lhc_fill"]
    assert 315543 == runs[0]["run_number"]


def test_get_run_range():
    runinfo = RunInfo()
    runs = runinfo.get_runs(run_number_from=315543, run_number_to=315583)
    assert 13 == len(runs)
