import sys
# from api.models.base import Base
import api.models.base

print(sys.path)
print(sys.modules)


# content of test_sample.py
def inc(x):
    return x + 1


def test_answer():
    assert inc(4) == 5