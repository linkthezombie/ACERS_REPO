from math import pi
from random import random

from positioning.Orientation import Orientation
from positioning.Quaternion import *
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
    q = Orientation().quaternion
    assert_floats(q.w, 1.0)
    assert_floats(q.x, 0.0)
    assert_floats(q.y, 0.0)
    assert_floats(q.z, 0.0)

def test_get_rotation_matrix():
    identity = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    matrix = Orientation().getRotationMatrix()
    assert_matrices(matrix, identity)

def test_pitch():
    orientation = Orientation().pitch(pi / 2.0)

    vector = orientation.rotateVector(Vector3D([1.0, 0.0, 0.0]))
    expected = Vector3D([0.0, 0.0, 1.0])
    assert_vectors(vector, expected)
    assert_floats(vector.getMagnitude(), expected.getMagnitude())

    vector = orientation.rotateVector(Vector3D([0.0, 1.0, 0.0]))
    expected = Vector3D([0.0, 1.0, 0.0])
    assert_vectors(vector, expected)
    assert_floats(vector.getMagnitude(), expected.getMagnitude())

    vector = orientation.rotateVector(Vector3D([0.0, 0.0, 1.0]))
    expected = Vector3D([-1.0, 0.0, 0.0])
    assert_vectors(vector, expected)
    assert_floats(vector.getMagnitude(), expected.getMagnitude())

def test_yaw():
    orientation = Orientation().yaw(pi / 2.0)

    vector = orientation.rotateVector(Vector3D([1.0, 0.0, 0.0]))
    expected = Vector3D([0.0, 1.0, 0.0])
    assert_vectors(vector, expected)
    assert_floats(vector.getMagnitude(), expected.getMagnitude())

    vector = orientation.rotateVector(Vector3D([0.0, 1.0, 0.0]))
    expected = Vector3D([-1.0, 0.0, 0.0])
    assert_vectors(vector, expected)
    assert_floats(vector.getMagnitude(), expected.getMagnitude())

    vector = orientation.rotateVector(Vector3D([0.0, 0.0, 1.0]))
    expected = Vector3D([0.0, 0.0, 1.0])
    assert_vectors(vector, expected)
    assert_floats(vector.getMagnitude(), expected.getMagnitude())

def test_roll():
    orientation = Orientation().roll(pi / 2.0)

    vector = orientation.rotateVector(Vector3D([1.0, 0.0, 0.0]))
    expected = Vector3D([1.0, 0.0, 0.0])
    assert_vectors(vector, expected)
    assert_floats(vector.getMagnitude(), expected.getMagnitude())

    vector = orientation.rotateVector(Vector3D([0.0, 1.0, 0.0]))
    expected = Vector3D([0.0, 0.0, 1.0])
    assert_vectors(vector, expected)

    vector = orientation.rotateVector(Vector3D([0.0, 0.0, 1.0]))
    expected = Vector3D([0.0, -1.0, 0.0])
    assert_vectors(vector, expected)
    assert_floats(vector.getMagnitude(), expected.getMagnitude())

def test_axis_angle_construction():
    orientation = Orientation.fromAxisAngle(Vector3D([1.0, 0.0, 0.0]), 0.0)
    vector = orientation.rotateVector(Vector3D([0.0, 0.0, 1.0]))
    expected = Vector3D([0.0, 0.0, 1.0])
    assert_vectors(vector, expected)
    assert_floats(vector.getMagnitude(), expected.getMagnitude())

    orientation = Orientation.fromAxisAngle(Vector3D([0.0, 999213.5, 0.0]), pi / 2.0)
    vector = orientation.rotateVector(Vector3D([1.0, 0.0, 0.0]))
    expected = Vector3D([0.0, 0.0, -1.0])
    assert_vectors(vector, expected)

def test_get_axis_angle():
    num_tests = 100

    for _ in range(0, num_tests):
        test_vector = Vector3D([random(), random(), random()])
        test_scalar = random()

        test = Orientation.fromAxisAngle(test_vector, test_scalar)
        (vector, scalar) = test.getAxisAngle()

        assert_vectors(vector, test_vector.normalize())
        assert_floats(scalar, test_scalar)

def test_inversion():
    num_tests = 100

    for _ in range(0, num_tests):
        test = Orientation.fromAxisAngle(Vector3D([random(), random(), random()]), random())
        expected = Vector3D([random(), random(), random()])
        vector0 = test.rotateVector(expected)
        inverse = test.invert()
        test = test.rotate(inverse)

        vector1 = test.rotateVector(expected)
        assert_vectors(vector1, expected)

        vector2 = inverse.rotateVector(vector0)
        assert_vectors(vector2, expected)

def test_from_matrix():
    # 90 degree left yaw
    mat = [
        [0, -1, 0],
        [1,  0, 0],
        [0,  0, 1]
    ]

    test = Vector3D([1.0, 0.0, 0.0])
    expected = Vector3D([0.0, 1.0, 0.0])

    orientation = Orientation.fromRotationMatrix(mat)
    actual = orientation.rotateVector(test)

    assert_vectors(actual, expected)
