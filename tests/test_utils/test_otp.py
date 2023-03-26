from app.utils.otp import get_random_pass


def test_get_random_pass_without_args():
    password = get_random_pass()

    assert len(password) == 6


def test_get_random_pass_with_args():
    password = get_random_pass(10)

    assert len(password) == 10
