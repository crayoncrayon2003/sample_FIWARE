"""Tests for action.py."""

import pytest

import ckan.tests.helpers as test_helpers


@pytest.mark.ckan_config("ckan.plugins", "sample")
@pytest.mark.usefixtures("with_plugins")
def test_sample_get_sum():
    result = test_helpers.call_action(
        "sample_get_sum", left=10, right=30)
    assert result["sum"] == 40
