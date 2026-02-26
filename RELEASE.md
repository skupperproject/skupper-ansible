# Skupper Ansible Collection Release Process
  
This document outlines the steps for creating a new release of the `skupper.v2` Ansible collection.

## Major/Minor Release Process
  
Follow these steps for a new **major.minor** release:

1.  If a new **major.minor** version (e.g., 2.1) is being released, first create a branch from `main` or check out the existing major.minor branch.
    ```
    git checkout -b 2.1
    ```
2.  Clean any previous build artifacts.
    ```
    make clean
    ```
3.  Update the target version using the script.
    ```
    ./scripts/update-version.sh 2.1.3
    ```
    *(For reference, [a sample patch for a prepared 2.1.1 release is available here](https://gist.github.com/fgiorgetti/efc158b1ebe9941175952469207aaace).)*
4.  Define the changelog for this release in: `changelogs/changelog.yaml`.
5.  Build the collection, documentation, and changelog.
    ```
    make all build-docs release-changelog
    ```
6.  Run the integration tests and test manually.
    ```
    make install integration
    ```
7.  Commit the changes and push to the official repository as a branch named `<major>.<minor>`, for example, **2.1**.
8.  Create a release tag, like: **2.1.3**.
9.  Push the tag to the upstream (official repo).
    ```
    git push upstream 2.1.3
    ```

## Post-Release: Setting up for Next Preview Version
  
Once the **release** is complete and **only if** it is the **latest version**, follow these steps to prepare the `main` branch for the next preview version:

1.  Create a new local branch from the `main` branch.
    - Example: `main-2.1.4-preview` (considering the latest released version as 2.1.3).
2.  Clean any previous build artifacts.
    ```
    make clean
    ```
3.  Cherry-pick the changes included in the release, including latest versions to galaxy.yml and Makefile (from the `<major>.<minor>` branch's HEAD, e.g., `2.1`'s HEAD).
4.  Update the versions to the next preview version.
    ```
    ./scripts/update-version.sh 2.1.4-preview
    ```
5.  Build the collection, documentation, and changelog.
    ```
    make all build-docs release-changelog
    ```
6.  Commit your changes and open a Pull Request (PR) against the `main` branch.
