import argparse
import numexpr as ne
import numpy as np


def get_input_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-w", action="store", dest="user_input", type=str, help="Store a simple value"
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")
    results = parser.parse_args()
    return results.user_input


def calculate(s):
    answer = float(ne.evaluate(s))
    return answer


# test
def test_1():
    assert abs(2 * np.sin(3 / 5) + np.log(7) - calculate("2*sin(3/5)+log(7)")) < 0.001


if __name__ == "__main__":
    user_input = get_input_args()
    if user_input is None:
        raise TypeError("Specify an input with '-w'")
    print(calculate(user_input))
