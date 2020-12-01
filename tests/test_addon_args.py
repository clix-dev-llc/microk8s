"""Tests addon argument parsing."""

import sh
import pytest
import yaml


def test_invalid_addon():
    with pytest.raises(sh.ErrorReturnCode_1):
        sh.microk8s.enable.foo()


def test_help_text():
    status = yaml.load(sh.microk8s.status(format='yaml').stdout)
    expected = {a['name']: 'disabled' for a in status['addons']}
    expected['ha-cluster'] = 'enabled'

    assert expected == {a['name']: a['status'] for a in status['addons']}

    for addon in status['addons']:
        sh.microk8s.enable(addon['name'], '--', '--help')

    assert expected == {a['name']: a['status'] for a in status['addons']}

    for addon in status['addons']:
        sh.microk8s.disable(addon['name'], '--', '--help')

    assert expected == {a['name']: a['status'] for a in status['addons']}
