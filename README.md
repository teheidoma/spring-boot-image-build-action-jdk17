# Spring Boot Image Build Action

![Spring Boot Image Build Action](https://img.shields.io/badge/Spring%20Boot%20Image%20Build-green?logo=arrow-up-circle)

This action builds your Spring application using 'bootBuildImage' and publishes it.

## Inputs

- `registry_username`: Registry username.
- `registry_password`: Registry password.
- `registry_hostname`: Registry hostname. Default is 'docker.io'.
- `include_commit_sha`: Include commit SHA to image tag. Default is 'false'.

## Outputs

- `tag`: Image name.
- `image_tag`: Image tag.

## Example Usage

```yaml
name: Build and Publish Spring Boot Image

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      - name: Build Spring Boot Image
        uses: teheidoma/spring-boot-image-build-action-jdk17@0.0.2
        with:
          registry_username: ${{ secrets.REGISTRY_USERNAME }}
          registry_password: ${{ secrets.REGISTRY_PASSWORD }}
          registry_hostname: 'docker.io'
          include_commit_sha: 'true'
