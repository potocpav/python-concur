
import concur as c
import integrations.window_glfw as window

def app():
    yield from c.button("Hello!")
    yield
    yield from c.text("Hello, sailor!")

window.main(app())
