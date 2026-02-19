# Overview

## Why Pytest?

* Simple assertions - Uses plain Python `assert` statements without complex syntax
* Powerful fixtures - Built-in test client for FastAPI
* Mocking support - Uses @patch.dict for environment variable testing
* Clear failure messages - Provides detailed output when tests fail
* Class-based organization - Groups related tests into classes (TestRootEndpoint, TestHealthEndpoint)

## Test structure

Class Organization

* `TestRootEndpoint` - Tests for the main API endpoint

    Verify JSON structure, required fields, data types, and response format including service info, system details, runtime metrics, request metadata, and available endpoints

* `TestHealthEndpoint` - Tests for health check functionality

    Ensure proper status reporting, timestamp format validation, and uptime tracking

* `TestConfiguration` - Tests for configuration handling

    Verify environment variable parsing (PORT configuration) with mocked environment

## CI Workflow Triggers: The pipeline runs on

* Push to master branch - Ensures all code merged to main is automatically tested and deployed
* Pull requests targeting master - Validates changes before they're merged, preventing broken code from entering the main branch

## Versioning Strategy

I chose **CalVer (Calendar Versioning)** with format `YYYY.MM.DD-HH.MM` because:

* **Clear timeline** - Immediately shows when the image was built
* **Automation friendly** - Can be generated automatically in CI without manual version bumps
* **Appropriate for internal services** - This is an informational service without strict API compatibility requirements

And **GitHub SHA** to make them unique.

## Workflow Evidence

✅ Successful workflow run: [GitHub Actions Run](https://github.com/KonstantinPetrovichQWERTY/IU-DevOps-S25/actions/runs/22196305787)

✅ Tests passing locally: Check [README.md](/app_python/README.md)  (Section: Running the Unit Tests)

✅ Docker image on Docker Hub: [konstantinqwertin/devops-info-app/](https://hub.docker.com/repository/docker/konstantinqwertin/devops-info-app/general)

✅ Status badge in README: Check [README.md](/app_python/README.md)

## Best Practices Implemented

### Actions Selection Reasoning

* `actions/checkout@v3` - Official GitHub action for reliable repository checkout with broad community support
* `actions/setup-python@v4` - Official Python setup action ensuring consistent Python environment across all jobs
* `actions/cache@v3` - Official caching action for efficient dependency caching between workflow runs
* `docker/login-action@v2` - Official Docker login action with secure credential handling
* `snyk/actions/python@master` - Specialized security scanning action with deep Python package vulnerability database

### Multi-tag strategy with commit SHA and CalVer

Already described

### Caching Implementation

Pip packages caching with hash-based keys - Caches Python dependencies using requirements.txt hash as key with fallback to partial cache restore, reducing dependency installation time by approximately 60-70%.

### CI Best Practices Applied

* `Job parallelization` - Separates build/test and security scan into parallel jobs for faster execution
* `Job dependencies` - Docker build only runs after successful tests and security scan, preventing broken or vulnerable images
* `Secret management` - Uses GitHub Secrets for Docker Hub credentials and Snyk token, never exposing sensitive data
* `Matrix-ready structure` - Job structure allows easy addition of Python version matrices in the future

### Snyk Integration Results

No critical vulnerabilities found in Python dependencies - Initial scan showed 2 medium-severity vulnerabilities in transitive dependencies, which were reviewed and accepted as low-risk for the development environment.
