#!/usr/bin/env python3

import pytest

@pytest.fixture
def pushover():
    import pushover
    return pushover

def test_pushover_exception(pushover):
    with pytest.raises(pushover.PushoverError):
        pushover.Pushover()
