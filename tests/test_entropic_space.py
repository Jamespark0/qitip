from qitip.objects import EntropicSpace


def test_from_no_random_variable() -> None:
    entropic_space = EntropicSpace(n=0)

    assert entropic_space._all_pairs == ()


def test_from_single_element() -> None:
    entropic_space = EntropicSpace(n=1)

    assert entropic_space._all_pairs == ({1},)


def test_from_two_element() -> None:
    entropic_space = EntropicSpace(n=2)

    assert entropic_space._all_pairs == (
        {1},
        {2},
        {1, 2},
    )


def test_from_three_element() -> None:
    entropic_space = EntropicSpace(n=3)

    assert entropic_space._all_pairs == (
        {1},
        {2},
        {3},
        {1, 2},
        {1, 3},
        {2, 3},
        {1, 2, 3},
    )


def test_from_four_element() -> None:
    entropic_space = EntropicSpace(n=4)

    assert len(entropic_space._all_pairs) == 2**4 - 1


def test_from_ten_element() -> None:
    entropic_space = EntropicSpace(n=10)

    assert len(entropic_space._all_pairs) == 2**10 - 1
