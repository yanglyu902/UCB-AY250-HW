import argparse
import numexpr as ne
import numpy as np
from urllib.request import urlopen
from urllib.parse import quote
import json


def get_input_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s", action="store", dest="simple_expression", type=str,
        help="Enter a simple mathematical expression"
    )
    parser.add_argument(
        "-w", action="store", dest="for_wolfram", type=str,
        help="Enter a complex question for WolframAlpha"
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")
    args = parser.parse_args()

    if args.simple_expression is None and args.for_wolfram is None:
        raise TypeError("Specify an input with \'-s\' (simple expression)" +
                        "or \'-w\' (for WolframAlpha)")

    return args


def calculate(s, local=True, return_float=True):
    if local:
        try:
            return calculate_locally(s)
        except:
            print('NOTE: Not a valid numerical expression!!! \n'
            'Please switch to WolframAlpha using local=False! \n')
    else:
        return calculate_remotely(s, return_float=return_float)


def calculate_locally(s):
    answer = float(ne.evaluate(s))
    return answer


def calculate_remotely(s, return_float):
    url = use_wolfram(s)
    answer_raw = get_result_from_wolfram(url)
    answer = convert_result_from_wolfram(answer_raw,
                                         return_float=return_float)
    return answer


def use_wolfram(s):
    s = quote(s)
    SERVICE = 'http://api.wolframalpha.com/v2/query?appid='
    ID = '5TG54Y-K3JUTT44Y8'
    INPUT = '&input=' + s
    url = SERVICE + ID + INPUT + '&output=json'
    return url


def get_result_from_wolfram(url):
    data = json.load(urlopen(url))
    pods = data['queryresult']['pods']

    for pod in pods:
        if pod['id'] == 'Result':
            answer = pod['subpods'][0]['plaintext']
            return answer
    print('NOTE: Invalid question for Wolfram to return a single number!!! \n')
    return None


def convert_result_from_wolfram(s, return_float):
    if return_float is False:
        return s
    # usually in form Ax10^B
    s = s.split()[0]
    if '×' in s or '^' in s:
        num = float(s.split('×')[0])
        expo = float(s.split('^')[-1])
        out = num * 10**expo
        return out
    else:
        return float(s)


# test
def test_1(): # test local
    assert abs(2 * np.sin(3 / 5) + np.log(7)
               - calculate("2*sin(3/5)+log(7)")) < 0.001

def test_2(): # test WolframAlpha
    assert abs(7.3459e+23 - calculate('mass of the moon in kg', \
               return_float=True, local=False) * 10) < 0.001

def test_3(): # simple expression, but use WolframAlpha
    assert abs(6.0 - calculate('2*3', \
               return_float=True, local=False)) < 0.001

def test_4(): # test WolframAlpha, string output
    assert calculate('mass of the moon in kg',  return_float=False, local=False)\
                     == '7.3459×10^22 kg (kilograms)'

if __name__ == "__main__":

    args = get_input_args()

    if args.simple_expression:
        print(calculate(args.simple_expression))

    if args.for_wolfram:
        print(calculate(args.for_wolfram, local=False))
