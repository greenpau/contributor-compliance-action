# contributor-compliance-action

Inspects a pull request for the compliance with contributing guidelines.

## Getting Started

Add the following to a Github workflow, e.g. `.github/workflows/contributors.yml`.

```
on: [push]

jobs:
  inspect_pr:
    runs-on: ubuntu-latest
    name: PR Inspection
    steps:
      - uses: actions/checkout@v2
      - id: inspection
        uses: github.com/greenpau/contributor-compliance-action@v1.0.1
        with:
          cla_consent_required: true
          signed_off_required: true
          issue_required: true
          max_commits: 1
          cla_consent_path: assets/cla/consent.yaml
```
