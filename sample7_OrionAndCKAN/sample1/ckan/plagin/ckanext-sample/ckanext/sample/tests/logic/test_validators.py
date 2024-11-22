"""Tests for validators.py."""

import pytest

import ckan.plugins.toolkit as tk

from ckanext.sample.logic import validators


def test_sample_reauired_with_valid_value():
    assert validators.sample_required("value") == "value"


def test_sample_reauired_with_invalid_value():
    with pytest.raises(tk.Invalid):
        validators.sample_required(None)
