import quaternion

from positioning.Orientation import Orientation
from positioning.Vector3D import Vector3D

def test_identity_quaternion():
    array = quaternion.as_float_array(Orientation().quaternion)
    assert array[0] == 1.0
    assert array[1] == 0.0
    assert array[2] == 0.0
    assert array[3] == 0.0