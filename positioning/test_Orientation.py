from math import pi
import quaternion

from positioning.Orientation import Orientation
from positioning.Vector3D import Vector3D

# Comparing floats is painful. There's no perfect way of doing it unless you
# track error accumulation with every single operation.
def assert_floats(a: float, b: float):
    small_number = 1.0 / 1_000_000.0

    if abs(min(a, b)) == 0.0:
        # When comparing against 0, the main test fails
        assert abs(max(a, b)) < small_number
    else:
        # Check to see if the error is smaller than a certain fraction of the numbers
        largest_unsigned = max(abs(a), abs(b))
        difference = abs(a - b)
        acceptable_error = largest_unsigned * small_number

        assert difference <= acceptable_error

def assert_vectors(a: Vector3D, b: Vector3D):
    assert_floats(a.x, b.x)
    assert_floats(a.y, b.y)
    assert_floats(a.z, b.z)

def assert_matrices(a: list[list[float]], b: list[list[float]]):
    for i in range(0, 3):
        for j in range(0, 3):
            assert_floats(a[i][j], b[i][j])

def test_identity_quaternion():
    array = quaternion.as_float_array(Orientation().quaternion)
    assert array[0] == 1.0
    assert array[1] == 0.0
    assert array[2] == 0.0
    assert array[3] == 0.0

def test_get_rotation_matrix():
    identity = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    matrix = Orientation().getRotationMatrix()
    assert_matrices(matrix, identity)

def test_pitch():
    orientation = Orientation()
    orientation.pitch(pi / 2.0)

    vector = orientation.rotateVector(Vector3D([1.0, 0.0, 0.0]))
    expected = Vector3D([0.0, 0.0, 1.0])
    assert_vectors(vector, expected)

    vector = orientation.rotateVector(Vector3D([0.0, 1.0, 0.0]))
    expected = Vector3D([0.0, 1.0, 0.0])
    assert_vectors(vector, expected)

    vector = orientation.rotateVector(Vector3D([0.0, 0.0, 1.0]))
    expected = Vector3D([-1.0, 0.0, 0.0])
    assert_vectors(vector, expected)

def test_yaw():
    orientation = Orientation()
    orientation.yaw(pi / 2.0)

    vector = orientation.rotateVector(Vector3D([1.0, 0.0, 0.0]))
    expected = Vector3D([0.0, 1.0, 0.0])
    assert_vectors(vector, expected)

    vector = orientation.rotateVector(Vector3D([0.0, 1.0, 0.0]))
    expected = Vector3D([-1.0, 0.0, 0.0])
    assert_vectors(vector, expected)

    vector = orientation.rotateVector(Vector3D([0.0, 0.0, 1.0]))
    expected = Vector3D([0.0, 0.0, 1.0])
    assert_vectors(vector, expected)

def test_roll():
    orientation = Orientation()
    orientation.roll(pi / 2.0)

    vector = orientation.rotateVector(Vector3D([1.0, 0.0, 0.0]))
    expected = Vector3D([1.0, 0.0, 0.0])
    assert_vectors(vector, expected)

    vector = orientation.rotateVector(Vector3D([0.0, 1.0, 0.0]))
    expected = Vector3D([0.0, 0.0, 1.0])
    assert_vectors(vector, expected)

    vector = orientation.rotateVector(Vector3D([0.0, 0.0, 1.0]))
    expected = Vector3D([0.0, -1.0, 0.0])
    assert_vectors(vector, expected)
