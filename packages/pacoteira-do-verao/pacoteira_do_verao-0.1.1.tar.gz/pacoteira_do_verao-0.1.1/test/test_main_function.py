from pacoteira_do_verao.main import hello_world

def test_hello_world():

    greeting = hello_world("Luba")
    assert greeting == "Hello, Luba"
