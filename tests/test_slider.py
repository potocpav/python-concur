
import concur as c
import imgui

# Breaking change in ImGui
# https://github.com/potocpav/python-concur/issues/24

@c.testing.test_widget
def test_sliders(tester):
    ev = yield from c.orr([
        c.orr_same_line([
            c.interactive_elem(imgui.v_slider_float,
                       name="Vslider",
                       width=20.0, height=100, value=1.0,
                       min_value=1, max_value=10,
                       format="%0.3f",
                       flags=imgui.SLIDER_LOGARITHMIC),
            ]),
        c.interactive_elem(imgui.slider_float, "Slider", 1.0, 1, 10),
        c.interactive_elem(imgui.slider_float2, "Slider2", 1.0, 2.0, 1, 10),
        c.interactive_elem(imgui.slider_float3, "Slider3", 1.0, 2.0, 3.0, 1, 10),
        c.interactive_elem(imgui.slider_float4, "Slider4", 1.0, 2.0, 3.0, 4.0, 1, 10),

        c.interactive_elem(imgui.drag_float, "Drag", 1.0, 1, 10),
        c.interactive_elem(imgui.drag_float2, "Drag2", 1.0, 2.0, 1, 10),
        c.interactive_elem(imgui.drag_float3, "Drag3", 1.0, 2.0, 3.0, 1, 10),
        c.interactive_elem(imgui.drag_float4, "Drag4", 1.0, 2.0, 3.0, 4.0, 1, 10),

        tester.pause(),
        ])
