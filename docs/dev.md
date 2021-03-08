# Development Guide

![img](/docs/img/Incuvers-black.png)

Modified: 2021-03

## Packaging and Deploying
This repository hosts the `iris-stage` client package. It is hosted on `pypi` and can be installed on any machine using pip:
```bash
python3 -m pip install iris-stage
```

Here I will describe how we build and publish new package distributions based on [this](https://www.codementor.io/@arpitbhayani/host-your-python-package-using-github-on-pypi-du107t7ku) guide:

1. First you will need a `pypi` and `testpypi` account, if you do not have both of these you will need to create these accounts.
2. Create a `.pypirc` file in the home directory with the following structure replacing USERNAME and PASSWORD with your account credentials:
    ```rc
    [distutils]
    index-servers =
        pypi
        testpypi

    [pypi]
    repository: https://upload.pypi.org/legacy/
    username: USERNAME
    password: PASSWORD

    [testpypi]
    repository: https://test.pypi.org/legacy/
    username: USERNAME
    password: PASSWORD
    ```
3. Write some updates on a feature branch and create a pull request into master. Ensure your code passes CI.
4. After it is merged into master increment the version number appropriately in [here](../iris_stage/__version__.py)
5. Build the distribution:
    ```bash
    ./scripts/build.sh
    ```
6. Publish the distribution to the testpypi repository:
    ```bash
    ./scripts/publish.sh testpypi
    ```
7. Test installing the package from `testpypi`
    ```bash
    python3 -m pip install --no-cache -i https://test.pypi.org/simple/ iris-stage
    ```
8. After validating the package works push to pypi:
    ```bash
    ./scripts/publish.sh pypi
    ```
