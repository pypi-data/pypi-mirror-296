def test_hello_world():
    from hello_world.main import hello_world
    assert hello_world() == "Hello, World!"
