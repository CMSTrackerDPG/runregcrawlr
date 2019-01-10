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
    run_numbers = tracker.get_non_regular_run_numbers(run_number_in=all_runs)
    expected = [314576, 314828, 318817, 319103, 319270]
    assert expected == run_numbers


def test_get_run_range():
    tracker = TrackerWorkspace()
    runs = tracker.get_runs(run_number_from=315543, run_number_to=315583)
    assert 29 == len(runs)


def test_get_run_txt():
    tracker = TrackerWorkspace()
    runs = tracker.get_runs_txt(run_number_from=315543, run_number_to=315583)
    print(runs)
    assert 29 == len(runs)
    assert [315543, "Express", "Collisions"] == runs[0]


def test_get_cosmics_run_numbers():
    cosmics_runs = [320481, 326945, 316706]
    commissioning_runs = [314576, 314828]
    special_runs = [319270, 318817, 319103]
    normal_runs = [318820, 326943]
    all_runs = cosmics_runs + commissioning_runs + special_runs + normal_runs

    tracker = TrackerWorkspace()
    run_numbers = tracker.get_cosmics_run_numbers(run_number_in=all_runs)
    expected = [316706, 320481, 326945]
    assert expected == run_numbers
