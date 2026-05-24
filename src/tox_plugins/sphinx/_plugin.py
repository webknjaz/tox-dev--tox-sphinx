"""A tox plugin providing Sphinx documentation environments."""

from __future__ import annotations

import typing as _t
from shlex import join as shlex_join

from tox.config.loader.memory import MemoryLoader
from tox.plugin import impl


if _t.TYPE_CHECKING:
    from collections import abc as _c  # noqa: WPS347

    from tox.config.sets import ConfigSet
    from tox.session.state import State


_PYTHON_CLI_OPTIONS = (
    'python',
    '-bb',
    '-E',
    '-s',
    '-I',
    '-Werror',
    # https://docs.python.org/3/library/io.html#io-encoding-warning
    '-Xwarn_default_encoding',
)

_BUILDER_SPECS = (
    # Per entry: env-name, sphinx-builder, extra-deps, description.
    (
        'build-docs',
        'html',
        (),
        'Build the docs site with Sphinx',
    ),
    (
        'codelinter-docs',
        'codelinter',
        ('sphinxawesome-codelinter',),
        'Lint code snippets in the docs',
    ),
    (
        'coverage-docs',
        'coverage',
        (),
        'Measure documentation coverage',
    ),
    (
        'doctest-docs',
        'doctest',
        (),
        'Run docstring/doctest examples',
    ),
    (
        'linkcheck-docs',
        'linkcheck',
        (),
        'Verify external links in the docs',
    ),
    (
        'spellcheck-docs',
        'spelling',
        ('sphinxcontrib-spelling',),
        'Spellcheck the docs prose',
    ),
)


def _build_sphinx_cmd(builder: str) -> str:
    """Compose a ``python -m sphinx`` invocation for the given builder.

    :param builder: The Sphinx builder name passed via ``-b``; also used
        as the output subdirectory name under ``{envtmpdir}``.
    :returns: A shell-safe command string for tox to execute.
    """
    cmd = (
        *_PYTHON_CLI_OPTIONS,
        '-msphinx',
        '--jobs=auto',  # -j  run in parallel. 'auto' == number of CPU cores
        f'--builder={builder!s}',  # -b        builder to use (default: 'html')
        '--write-all',  # -a       write all files (default: only new+changed)
        # '--fresh-env',  # -E     don't use a saved env, always read all files
        '--nitpicky',  # -n        warn about all missing references
        '--fail-on-warning',  # -W
        # '--show-traceback',  # -T  show full traceback on exception
        # '--pdb',  # -P             run Pdb on exception
        # '--exception-on-warning',  # raise an exception on warnings
        '--keep-going',  # prevent stopping on first error/failure/warning
        '--tag==is_unversioned',  # -t define tag: include "only" blocks w/ TAG
        '--doctree-dir={envtmpdir}/.doctrees',  # -d
        '.',  # SOURCEDIR (relative to `change_dir`)
        f'{{envtmpdir}}/{builder!s}',  # OUTPUTDIR
        # [FILENAMES...]
    )
    return shlex_join(cmd)


@impl
def tox_extend_envs() -> _c.Iterable[str]:
    """Declare the Sphinx documentation environments.

    :returns: The names of the tox environments this plugin provides.
    """
    return tuple(spec[0] for spec in _BUILDER_SPECS)


@impl
def tox_add_core_config(
    core_conf: ConfigSet,  # noqa: ARG001  # pylint: disable=unused-argument
    state: State,
) -> None:
    """Inject default configuration for the docs environments.

    :param core_conf: The core tox configuration set (unused).
    :param state: The tox session state to inject environments into.
    """
    fetch_pre_cmds = (
        f'-{shlex_join(("git", "fetch", "--unshallow"))}',
        f'-{shlex_join(("git", "fetch", "--tags"))}',
    )
    for env_name, builder, extra_deps, description in _BUILDER_SPECS:
        state.conf.memory_seed_loaders[env_name].append(
            MemoryLoader(
                base=[],
                description=f'[tox-sphinx] {description}',
                deps=['sphinx', *extra_deps],
                allowlist_externals=['git'],
                change_dir='docs',
                commands_pre=list(fetch_pre_cmds),
                commands=[_build_sphinx_cmd(builder)],
                commands_post=[],
            ),
        )
