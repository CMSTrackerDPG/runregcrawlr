from runregcrawlr.tracker import TrackerWorkspace


def test_get_single_run():
    tracker = TrackerWorkspace()
    runs = tracker.get_runs(run_number=315543)
    assert 4 == len(runs)


def test_get_run_range():
    tracker = TrackerWorkspace()
    runs = tracker.get_runs(run_number_from=315543, run_number_to=315583)
    assert 29 == len(runs)
