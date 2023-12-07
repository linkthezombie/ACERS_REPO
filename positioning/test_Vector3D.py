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

def test_addition():
    v0 = Vector3D([0.0, 0.0, 0.0])
    v1 = Vector3D([1.0, 2.0, 3.0])
    v2 = Vector3D([2.0, 0.0, 1.0])
    v3 = Vector3D([-1.0, -1.0, -1.0])

    assert_vectors(v0 + v1, v1)
    assert_vectors(v0 + v2, v2)
    assert_vectors(v1 + v2, Vector3D([3.0, 2.0, 4.0]))
    assert_vectors(v1 + v3, Vector3D([0.0, 1.0, 2.0]))
    assert_vectors(v2 + v3, Vector3D([1.0, -1.0, 0.0]))

def test_addition_identity():
    zeroes = Vector3D([0.0, 0.0, 0.0])
    assert_vectors(zeroes + zeroes, zeroes)

def test_length():
    assert Vector3D([0.0, 0.0, 0.0]).getMagnitude() == 0.0
    assert Vector3D([3.0, 4.0, 0.0]).getMagnitude() == 5.0
    assert Vector3D([-3.0, -4.0, -0.0]).getMagnitude() == 5.0

def test_scale():
    bigNumber = 9999999999999999999999.0

    v = Vector3D([0.0, 0.0, 0.0])
    assert v.scale(bigNumber).getMagnitude() == 0.0

    v = Vector3D([bigNumber, bigNumber, bigNumber])
    assert v.scale(0.0).getMagnitude() == 0.0

    v = Vector3D([3.0, 4.0, 0.0])
    assert v.scale(1.0).getMagnitude() == 5.0
    v = v.scale(1.0 / 5.0)
    assert v.getMagnitude() == 1.0
    v = v.scale(100.0)
    assert v.getMagnitude() == 100.0

def test_normalize():
    v = Vector3D([123.0, 55555555.0, 0.0002])
    assert v.normalize().getMagnitude() == 1.0
