from runregcrawlr.tracker import TrackerWorkspace


def test_get_single_run():
    tracker = TrackerWorkspace()
    runs = tracker.get_runs(run_number=315543)
    assert 4 == len(runs)


def test_get_non_regular_run_numbers():
    commissioning_runs = [314576, 314828]
    special_runs = [319270, 318817, 319103]
    normal_runs = [318820, 316706]
    all_runs = commissioning_runs + special_runs + normal_runs

    tracker = TrackerWorkspace()
    runs = tracker.get_non_regular_run_numbers(run_number_in=all_runs)
    run_numbers = set([run["run_number"] for run in runs])
    expected = {314576, 314828, 319270, 318817, 319103}
    assert expected == run_numbers


def test_get_run_range():
    tracker = TrackerWorkspace()
    runs = tracker.get_runs(run_number_from=315543, run_number_to=315583)
    assert 29 == len(runs)
