"""Behavioral tests for the tox-sphinx plugin."""

from __future__ import annotations

import typing as _t

import pytest


if _t.TYPE_CHECKING:
    from pytest_subtests import SubTests

    from tox.pytest import ToxProjectCreator


def test_docs_envs_registered(
    tox_project: ToxProjectCreator,
    subtests: SubTests,
) -> None:
    """The plugin contributes the docs envs to the env list.

    :param tox_project: Tox-provided project factory fixture.
    :param subtests: Pytest's subtest fixture for granular reporting.
    """
    project = tox_project({'tox.ini': '[tox]\n'})
    tox_invocation_result = project.run('list')
    tox_invocation_result.assert_success()
    for env_name in (
        'build-docs',
        'codelinter-docs',
        'coverage-docs',
        'doctest-docs',
        'linkcheck-docs',
        'spellcheck-docs',
    ):
        with subtests.test(msg=env_name):
            assert env_name in tox_invocation_result.out


@pytest.mark.parametrize(
    ('env_name', 'expected_builder'),
    (
        pytest.param('build-docs', 'html', id='build-docs'),
        pytest.param('codelinter-docs', 'codelinter', id='codelinter-docs'),
        pytest.param('coverage-docs', 'coverage', id='coverage-docs'),
        pytest.param('doctest-docs', 'doctest', id='doctest-docs'),
        pytest.param('linkcheck-docs', 'linkcheck', id='linkcheck-docs'),
        pytest.param('spellcheck-docs', 'spelling', id='spellcheck-docs'),
    ),
)
def test_env_invokes_expected_builder(
    tox_project: ToxProjectCreator,
    env_name: str,
    expected_builder: str,
) -> None:
    """The plugin's envs invoke ``sphinx`` with the expected builder.

    :param tox_project: Tox-provided project factory fixture.
    :param env_name: Name of the env to query.
    :param expected_builder: Sphinx builder name expected on the command line.
    """
    project = tox_project({'tox.ini': '[tox]\n'})
    tox_invocation_result = project.run(
        'config',
        '-e',
        env_name,
        '-k',
        'commands',
    )
    tox_invocation_result.assert_success()
    assert '-msphinx' in tox_invocation_result.out
    assert f'--builder={expected_builder}' in tox_invocation_result.out
