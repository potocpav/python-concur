
from concur.colors import color_to_rgba


def test_color_eq():
    assert color_to_rgba('cyan') == color_to_rgba((0, 1, 1))
    assert color_to_rgba(0x004080c0) == color_to_rgba((0.751, 0.501, 0.251, 0))
    assert color_to_rgba(('cyan', 0.5)) == color_to_rgba((0, 1, 1, 0.5))
