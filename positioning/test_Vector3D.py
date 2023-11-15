from positioning.Vector3D import Vector3D

def test_addition():
    v0 = Vector3D([0.0, 0.0, 0.0])
    v1 = Vector3D([1.0, 2.0, 3.0])
    v2 = Vector3D([2.0, 0.0, 1.0])
    v3 = Vector3D([-1.0, -1.0, -1.0])

    assert v0 + v1 == v1
    assert v0 + v2 == v2
    assert v1 + v2 == Vector3D([3.0, 2.0, 4.0])
    assert v1 + v3 == Vector3D([0.0, 1.0, 2.0])
    assert v2 + v3 == Vector3D([1.0, -1.0, 0.0])

def test_addition_identity():
    zeroes = Vector3D([0, 0, 0])
    assert zeroes + zeroes == zeroes

def test_length():
    assert Vector3D([0.0, 0.0, 0.0]).getMagnitude() == 0.0
    assert Vector3D([3.0, 4.0, 0.0]).getMagnitude() == 5.0
    assert Vector3D([-3.0, -4.0, -0.0]).getMagnitude() == 5.0

def test_scale():
    bigNumber = 9999999999999999999999.0

    v = Vector3D([0.0, 0.0, 0.0])
    v.scale(bigNumber)
    assert v.getMagnitude() == 0.0

    v = Vector3D([bigNumber, bigNumber, bigNumber])
    v.scale(0.0)
    assert v.getMagnitude() == 0.0

    v = Vector3D([3.0, 4.0, 0.0])
    v.scale(1.0)
    assert v.getMagnitude() == 5.0
    v.scale(1.0 / 5.0)
    assert v.getMagnitude() == 1.0
    v.scale(100.0)
    assert v.getMagnitude() == 100.0

def test_normalize():
    v = Vector3D([123.0, 55555555.0, 0.0002])
    v.normalize()
    assert v.getMagnitude() == 1.0
