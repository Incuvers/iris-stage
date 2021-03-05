# Iris Staging Server
[![Lint](https://github.com/Incuvers/iris-staging/actions/workflows/lint.yaml/badge.svg)](https://github.com/Incuvers/iris-staging/actions/workflows/lint.yaml)

![img](/docs/img/Incuvers-black.png)

Modified: 2021-03

## Quickstart
Upgrade pip:
```bash
python3 -m pip install --upgrade pip
```
Install the iris_stage package:
```bash
python3 -m pip install iris_stage
```
Launch the staging server:
```bash
stage
```
Halt the server:
```bash
unstage
```

## Server Requirements
This server is designed to be run on an iris production machine. All the hardware and peripherals should be mounted and ready for integration testing.

### AWS Services
The AWS Python SDK `boto3` requires AWS user tokens and region information. To avoid passing these tokens at runtime and increasing the complexity of the build process I have required that the AWS credentials and configuration are bound to the staging server. Therefore these credentials will exist in the `$HOME` directory as described [here](.aws/README.md)

### IRIS Machine Credentials
The IRIS snap requires production grade machine credentials. I have required that the machine credentials are bound to the staging server in the `$HOME` directory as described [here](.secrets/README.md). These credentials must be production grade as the snap is built pointing to our production api.