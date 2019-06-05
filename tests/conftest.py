from ophyd.sim import SynAxis
import pytest


@pytest.fixture(scope='function')
def motor():
    return SynAxis(name='motor')
