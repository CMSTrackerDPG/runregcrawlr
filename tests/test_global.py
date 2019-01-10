from runregcrawlr.globalworkspace import GlobalWorkspace


def test_get_single_run():
    global_workspace = GlobalWorkspace()
    runs = global_workspace.get_runs(run_number=315543)
    assert 3 == len(runs)


def test_get_run_range():
    global_workspace = GlobalWorkspace()
    runs = global_workspace.get_runs(run_number_from=315543, run_number_to=315583)
    assert 24 == len(runs)
