# Development Notes

<!-- begin-markdown-toc -->
## Table of Contents

* [Development Environment](#development-environment)
* [Github Action](#github-action)

<!-- end-markdown-toc -->

## Development Environment

Create experimental directory `~/experimental/gh`:

```bash
mkdir -p ~/experimental/gh && cd ~/experimental/gh
```

Create `contributor-compliance-action` and `test-inspect` repositories in Github.

Next, clone it:

```bash
cd ~/experimental/gh && git clone git@github.com:greenpau/contributor-compliance-action.git
cd ~/experimental/gh && git clone git@github.com:greenpau/test-inspect.git
```

## Github Action

This Github action has access to the following environment variables.

```
GITHUB_BASE_REF=main
GITHUB_HEAD_REF=testactions
GITHUB_REF=refs/pull/1/merge
GITHUB_REF_NAME=1/merge
GITHUB_REF_TYPE=branch
GITHUB_REPOSITORY=greenpau/test-inspect
GITHUB_REPOSITORY_OWNER=greenpau
GITHUB_SHA=e64fe03c2d4be68f190fa6cdf4696210babb67b0
```

The top commit follows:

```
$ git log
commit e64fe03c2d4be68f190fa6cdf4696210babb67b0
Author: Paul Greenberg <greenpau@users.noreply.github.com>
Date:   Sun Jan 23 18:05:40 2022 +0000

    Merge 038d5b41393d15522bd8687aa6836d6d2dbeb66a into e262a588f187a520acb0fe33cab949c1ab44200a
```

The `e64fe03c2d4be68f190fa6cdf4696210babb67b0` (referenced by `GITHUB_SHA`) is
the commit id internal to the github action.

The `038d5b41393d15522bd8687aa6836d6d2dbeb66a` is the top commit in the branch
of the contributor's fork.

The `e262a588f187a520acb0fe33cab949c1ab44200a` is the HEAD of the `main` branch
in the project the contributor sends the pull request to.
