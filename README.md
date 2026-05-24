[![SWUbanner]][SWUdocs]

[![tox-dev badge]][tox-dev]
[![pre-commit.ci status badge]][pre-commit.ci results page]
[![GH Sponsors badge]][GH Sponsors URL]

[SWUbanner]:
https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg
[SWUdocs]:
https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md

[tox-dev]: https://github.com/tox-dev
[tox-dev badge]:
https://img.shields.io/badge/project-yellow?label=tox-dev&labelColor=c3cc39&color=7f833e

[pre-commit.ci status badge]:
https://results.pre-commit.ci/badge/github/tox-dev/tox-sphinx/main.svg
[pre-commit.ci results page]:
https://results.pre-commit.ci/latest/github/tox-dev/tox-sphinx/main

[GH Sponsors badge]:
https://img.shields.io/badge/%40webknjaz-transparent?logo=githubsponsors&logoColor=%23EA4AAA&label=Sponsor&color=2a313c
[GH Sponsors URL]:
https://github.com/sponsors/webknjaz


# tox-sphinx

A tox plugin providing Sphinx documentation environments.


## Usage

Add `tox-sphinx` to your project's `tox` requirements -- either
in `tox.toml`:

```toml
requires = [
  "tox-sphinx",
]
```

...or in `tox.ini`:

```ini
[tox]
requires =
  tox-sphinx
```

Then invoke any of the six docs envs the plugin exposes:

```console
$ tox run -q -e build-docs        # build the HTML docs site
$ tox run -q -e codelinter-docs   # lint code snippets in the docs
$ tox run -q -e coverage-docs     # measure documentation coverage
$ tox run -q -e doctest-docs      # run docstring/doctest examples
$ tox run -q -e linkcheck-docs    # verify external links
$ tox run -q -e spellcheck-docs   # spellcheck the docs prose
```
