from streamlit.testing.v1 import AppTest


def test_streamlit_app_renders_without_errors():
    app = AppTest.from_file("src/app.py")
    app.run(timeout=10)

    assert not app.exception
    assert app.title[0].value == "ValorAI"
