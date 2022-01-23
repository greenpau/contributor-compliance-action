# contributor-compliance-action

Inspects a pull request for the compliance with OSS contributing guidelines.
It covers CLA, Signed-off-by, and other aspects of OSS contributing.

🚩This github action DOES NOT require passing security token to
perform its assessment.

<!-- begin-markdown-toc -->
## Table of Contents

* [Overview](#overview)
* [Getting Started](#getting-started)
* [Commit Message Tags](#commit-message-tags)

<!-- end-markdown-toc -->

## Overview

1. Checks whether a contributor already **signed CLA** in previous PRs
2. If a contributor did not sign CLA, the contributor must do so as part of
  the first commit in the PR. Otherwise, you might be accepting an earlier
  commit without CLA consent
3. Checks whether the commits are **signed by the individual** who signed
  the CLA
4. Checks whether the final commit contains a **reference to an issue**
  related to the committed work. If it fails, that might indicate the
  contributor did not previously discuss the work
5. Checks that **the number of commits** in a PR does not exceed configured
  number
6. Checks that the changes in the commit **do not modify Github workflows**

**Note**: The above checks can be disabled (1) by modifying Github workflow
  or (2) by adding **commit message tags** to the last commit in a PR.

📗Further, this action allows to see the commits in a slightly different
way as it shows in Github PR pages.

## Getting Started

Add the following Github workflow to your project,
e.g. `.github/workflows/contributors.yml`. This workflow assumes the
pull requests are going to be made against `main` branch. You may want to
modify it.

```
on:
  pull_request:
    branches:
    - main

jobs:
  inspect_pr:
    runs-on: ubuntu-latest
    name: PR Inspection
    steps:
      - uses: actions/checkout@v2
      - id: inspection
        uses: greenpau/contributor-compliance-action@v1.0.10
        with:
          cla_consent_required: true
          signed_off_required: true
          issue_required: true
          max_commits: 1
          cla_consent_path: assets/cla/consent.yaml
```

## Commit Message Tags

If a commit message contains the `CONTRIBUTOR_COMPLIANCE=disabled`, then
this Github Action will still perform all the checks. However, it will not
fail the PR request if it finds non-compliance.

```
docs: update README.md

CONTRIBUTOR_COMPLIANCE=disabled
```
