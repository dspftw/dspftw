# Releasing DSPFTW

This document explains how to prepare, test, and publish DSPFTW releases to the Python Package Index (PyPI).

## Version numbers

DSPFTW uses two independent version identifiers:

- **PyPI release version:** A calendar-based identifier in the format `YEAR.DAY_OF_YEAR.MINUTE_OF_DAY`, using UTC. For example, `2026.311.289`.
- **Library maturity version:** A semantic identifier such as `0.2.0`, maintained separately in the README.

The PyPI version changes for each published release. The maturity version changes only when the library reaches a new development milestone.

## Automated workflows

DSPFTW uses two GitHub Actions workflows:

- `.github/workflows/test.yml` runs automated tests on pushes and pull requests.
- `.github/workflows/python-package.yml` tests, builds, and publishes the package when a Git tag beginning with `v` is pushed.

Both workflows test Python 3.10 through 3.14.

Ordinary pushes to `master` do not publish packages to PyPI.

The publishing workflow retains the filename `python-package.yml` because that is the filename registered in the project's PyPI Trusted Publisher configuration.

## Preparing a release

1. Ensure the `master` branch is current and the working directory is clean.

2. Generate a calendar-based release version:

   ```bash
   python3 scripts/generate_version.py
   ```

3. Set the package version in `pyproject.toml` using Poetry. For example:

   ```bash
   .venv-build/bin/poetry version 2026.311.289
   ```

   Replace the example with the generated version.

4. Update the README and other documentation as needed. Review the separate library maturity version.

5. Run local tests:

   ```bash
   tox -e py312
   ```

6. Build the distributions:

   ```bash
   .venv-build/bin/poetry build
   ```

7. Validate the distributions using Twine. For example:

   ```bash
   .venv-build/bin/python -m twine check dist/dspftw-2026.311.289*
   ```

   Replace the example version with the intended release version.

8. Commit and push the release preparation changes to `master`.

9. Wait for the GitHub Actions test workflow to complete successfully.

## Creating a release tag

Once tests have passed, create an annotated Git tag matching the version in `pyproject.toml`.

For example:

```bash
git tag -a v2026.311.289 -m "Release DSPFTW 2026.311.289"
```

Verify the tag:

```bash
git show v2026.311.289
```

Push the tag to GitHub:

```bash
git push origin v2026.311.289
```

**Pushing the tag triggers the publishing workflow.**

The publishing workflow obtains the release version from the tag, runs tests, builds the package, and attempts to publish it to PyPI.

## Verifying publication

Monitor the **Publish release** workflow at:

https://github.com/dspftw/dspftw/actions

After the workflow succeeds, verify the published version at:

https://pypi.org/project/dspftw/

Confirm that the PyPI version matches the Git tag.

## PyPI Trusted Publishing

DSPFTW uses PyPI Trusted Publishing rather than a stored PyPI password or API token.

The expected configuration is:

- GitHub owner: `dspftw`
- Repository: `dspftw`
- Workflow filename: `python-package.yml`
- GitHub environment: `publish`

These settings must match the Trusted Publisher configuration registered on PyPI.

The original project maintainer, Bill Allen, confirmed that the registered workflow filename is `python-package.yml`.

If publishing fails, inspect the GitHub Actions logs and verify the PyPI configuration before retrying.

Never commit publishing credentials to the repository.

## Release checklist

- [ ] Release version generated
- [ ] `pyproject.toml` version reviewed
- [ ] README and maturity version reviewed
- [ ] Local tests passed
- [ ] Distributions built and validated
- [ ] Release preparation committed and pushed
- [ ] GitHub Actions tests passed
- [ ] Annotated release tag created
- [ ] Tag pushed to GitHub
- [ ] Publishing workflow succeeded
- [ ] Published version verified on PyPI

## Important notes

PyPI does not permit replacing an existing published distribution. Each new release must use a version number that has not previously been published.

Do not create or push a release tag until the corresponding code has passed testing.

The `.venv-build` directory is a local development environment used by one maintainer. Other developers may use their own Poetry and Python installations.
