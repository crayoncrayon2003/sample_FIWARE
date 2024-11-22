"""Tests for views.py."""

import pytest

import ckanext.sample.validators as validators


import ckan.plugins.toolkit as tk


@pytest.mark.ckan_config("ckan.plugins", "sample")
@pytest.mark.usefixtures("with_plugins")
def test_sample_blueprint(app, reset_db):
    resp = app.get(tk.h.url_for("sample.page"))
    assert resp.status_code == 200
    assert resp.body == "Hello, sample!"
