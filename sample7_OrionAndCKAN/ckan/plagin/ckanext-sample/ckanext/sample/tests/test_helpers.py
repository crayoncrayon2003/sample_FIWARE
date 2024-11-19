"""Tests for helpers.py."""

import ckanext.sample.helpers as helpers


def test_sample_hello():
    assert helpers.sample_hello() == "Hello, sample!"
