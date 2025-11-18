# CI/CD Documentation

## Overview

This repository includes automated CI/CD workflows using GitHub Actions for continuous integration, testing, and Docker image publishing.

## Workflows

### 1. Docker Publish Workflow (`docker-publish.yml`)

**Purpose:** Builds and publishes Docker images to GitHub Container Registry (GHCR).

**Triggers:**
- Manual dispatch via GitHub UI (`workflow_dispatch`)
- Push to `main` branch
- Pull request merged to `main` branch

**Jobs:**

#### `build-and-push`
- Builds Docker image from the repository
- Pushes to `ghcr.io/<owner>/projeto-novo` with two tags:
  - `latest` - most recent build
  - `<commit-sha>` - specific commit identifier
- Uses Docker layer caching for faster builds
- Requires permissions:
  - `contents: read` - to checkout repository
  - `packages: write` - to push to GHCR
  - `id-token: write` - for OIDC authentication

#### `smoke-test`
- Runs after successful build
- Pulls the published Docker image
- Creates sample test data
- Executes the pipeline inside the container
- Validates that expected outputs are generated:
  - `outputs/consolidado_flags.csv`
  - `outputs/consolidado_flags.json`

**Actions Used:**
- `actions/checkout@v4` - Repository checkout
- `docker/setup-qemu-action@v3` - Multi-platform builds
- `docker/setup-buildx-action@v3` - Docker Buildx
- `docker/login-action@v3` - GHCR authentication
- `docker/build-push-action@v5` - Build and push images

### 2. CI Smoke Test Workflow (`smoke.yml`)

**Purpose:** Runs automated tests on pull requests to validate changes.

**Triggers:**
- Pull request opened, synchronized, or reopened

**Jobs:**

#### `smoke`
- Sets up Python 3.11 environment
- Installs dependencies from `requirements.txt`
- Runs pytest test suite
- Creates sample data
- Executes pipeline scripts
- Validates outputs

### 3. Python Package Publish (`python-publish.yml`)

**Purpose:** Publishes Python package to PyPI when releases are created.

**Triggers:**
- GitHub release published

**Jobs:**
- Builds Python distribution packages
- Publishes to PyPI using trusted publishing

## Using the Docker Image

### Pull the Latest Image

```bash
docker pull ghcr.io/<owner>/projeto-novo:latest
```

### Run the Pipeline

```bash
# Create data directory with your CSV files
mkdir -p data
# Place your CSV files in data/

# Run the container
docker run --rm \
  -v "$PWD/data":/app/data \
  -v "$PWD/outputs":/app/outputs \
  ghcr.io/<owner>/projeto-novo:latest
```

### Expected Outputs

The pipeline generates:
- `outputs/consolidado_flags.csv` - Consolidated data with flags
- `outputs/consolidado_flags.json` - JSON format output

## Manual Workflow Dispatch

You can manually trigger the Docker publish workflow:

1. Go to the **Actions** tab in GitHub
2. Select **Build and publish Docker image**
3. Click **Run workflow**
4. Select the branch (usually `main`)
5. Click **Run workflow** button

## Permissions Required

For the workflows to function properly, ensure the repository has:

- **Actions permissions**: Read and write access
- **Packages permissions**: Read and write access
- **GitHub Token**: Automatically provided by GitHub Actions

## Troubleshooting

### Build Failures

Check the workflow logs in the **Actions** tab for detailed error messages.

### Smoke Test Failures

If smoke tests fail:
1. Verify sample data format matches expected CSV structure
2. Check that all required dependencies are in `requirements.txt`
3. Ensure pipeline scripts are executable and have correct paths

### Docker Image Pull Issues

If you can't pull the image:
1. Authenticate with GHCR: `echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin`
2. Verify package visibility settings (public or private with access)

## Development Workflow

1. Create a feature branch
2. Make changes to code
3. Push to GitHub - triggers smoke tests
4. Create pull request - smoke tests run automatically
5. Merge to `main` - triggers Docker build and publish
6. Docker image is available for use

## Maintenance

### Updating Action Versions

Periodically update action versions in workflow files:
- Check for new releases: https://github.com/actions/
- Update version tags (e.g., `@v4` → `@v5`)
- Test in a branch before merging to main

### Adding New Tests

1. Add test files to `tests/` directory
2. Follow existing test patterns
3. Update `smoke.yml` if new test commands are needed

## Security

- All secrets are managed through GitHub Secrets
- Docker images use official Python base images
- Dependencies are pinned in `requirements.txt`
- Regular security scanning via CodeQL (if configured)
