from ophyd.status import MoveStatus
import pytest

from motor_watch.status import process


@pytest.fixture(scope='function')
def move_status(motor):
    return MoveStatus(motor, 34)


@pytest.mark.xfail
def test_status_record(move_status, motor):
    move_status._finished(success=True)
    move_info = process(move_status)
    assert move_info['name'] == motor.pos
    assert move_info['target'] == move_status.target
