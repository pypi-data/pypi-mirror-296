# content of conftest.py
def pytest_addoption(parser):
    parser.addoption("--cmdopt2", action="store", help="Name of an calibration")
