# Lumeo Python PyPi package

[Package on PyPI](https://pypi.org/project/lumeo/)

## Development

Uses pyscaffold and tox to manage the project.
```
pipx install tox pyscaffold
pipx inject pyscaffold pyscaffoldext-markdown
```

## How to Make a Release

Releasing a new version of the project involves updating the version number and creating a new tag/release in the repository. Follow the steps below to make a release:

1. **Update the Version Number**:
    - Open the `lumeo/__init__.py` file.
    - Find the line that defines the `__version__` variable. It should look something like this:
      ```python
      __version__ = "x.y.z"
      ```
    - Update the version number to the new version you are releasing. For example, if the current version is `1.2.3` and you are releasing version `1.2.4`, change the line to:
      ```python
      __version__ = "1.2.4"
      ```
    - Save the file.

2. **Commit the Version Update**:
    - Stage the changes to `lumeo/__init__.py`:
      ```sh
      git add lumeo/__init__.py
      ```
    - Commit the change with a descriptive message:
      ```sh
      git commit -m "Bump version to 1.2.4"
      ```

3. **Create a New Tag/Release**:
    - Create a new tag for the release:
      ```sh
      git tag -a v1.2.4 -m "Release version 1.2.4"
      ```
    - Push the tag to the repository:
      ```sh
      git push origin v1.2.4
      ```

    Creating the tag will trigger the CI that will build and publish the new version to pypi.org.