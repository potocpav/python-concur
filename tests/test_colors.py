
from concur.colors import color_to_rgba, color_to_rgba_tuple


def test_color_eq():
    assert color_to_rgba('cyan') == color_to_rgba((0, 1, 1))
    assert color_to_rgba(0x004080c0) == color_to_rgba((0.751, 0.501, 0.251, 0))
    assert color_to_rgba(('cyan', 0.5)) == color_to_rgba((0, 1, 1, 0.5))
    # roundtrip
    for c in [(1.0,0.0,0.0,0.0), (0.0,0.0,1.0,0.5), (0.1,0.2,0.3,0.4),]:
        assert max([abs(a - b) for a, b in zip(color_to_rgba_tuple(color_to_rgba(c)), c)]) < 1/256
