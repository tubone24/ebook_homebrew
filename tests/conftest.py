import pytest


def pytest_addoption(parser):
    """Add custom option for pytest"""
    parser.addoption("--it", action="store_true",
                     default=False, help="Do test \"integration test\"")


def pytest_collection_modifyitems(config, items):
    """Check markers for skip specify test cases."""
    if config.getoption("--it"):
        # --it given in cli: do not skip Integration tests
        return
    skip_it = pytest.mark.skip(reason="need --it option to run")
    for item in items:
        if "it" in item.keywords:
            item.add_marker(skip_it)
