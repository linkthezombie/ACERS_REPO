from math import pi

from positioning.Orientation import Orientation
from positioning.Pose import Pose
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
    for i in range(0, 4):
        for j in range(0, 4):
            assert_floats(a[i][j], b[i][j])

def test_transformation_matrix():
    pose = Pose(Vector3D([1.0, 2.0, 3.0]), Orientation())
    mat = pose.getTransformationMatrix()

    assert_matrices(mat, [[1.0, 0.0, 0.0, 1.0],
                          [0.0, 1.0, 0.0, 2.0],
                          [0.0, 0.0, 1.0, 3.0],
                          [0.0, 0.0, 0.0, 1.0]])
