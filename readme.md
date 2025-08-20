# Nautobot Job Unit Testing for GIT Sourced, Non-App based Jobs

## Prerequisites

### 1. Git Repository with Jobs and Tests

You'll need a Git repository containing your jobs and tests. Here's an example structure:

```
example_nautobot_job_unit_testing/
├── jobs/
│   ├── __init__.py
│   └── example_custom_form.py
└── tests/
    ├── __init__.py
    └── test_case.py
```

**Example Repository:** [example-nautobot-job-unit-testing](https://github.com/MeganerdDev/example-nautobot-job-unit-testing)

> **Note:** In the demo examples, the Nautobot Git repository object is named "test_git_repo"

### 2. Git Access Token

You'll need a Git access token for the repository clone operation.

### 3. Testing Configuration File

Create a `nautobot_config.py` file for testing. The example below is based on the [Nautobot core test configuration](https://github.com/nautobot/nautobot/blob/develop/nautobot/core/tests/nautobot_config.py).

You can set `GIT_ROOT` and `JOBS_ROOT` in this file or use environment variables when executing in the container shell.

```python
"""Nautobot development configuration file."""

import os

from nautobot.core.settings import *  # noqa: F403  # undefined-local-with-import-star
from nautobot.core.settings_funcs import parse_redis_connection

ALLOWED_HOSTS = ["nautobot.example.com"]

# NOTE: we could use this condition if we wanted to have the same nautobot_config for non test cases
#if "test" in sys.argv:
#   GIT_ROOT = "/tmp/nautobot/git-tests"
#   JOBS_ROOT = "/opt/nautobot/git/test_git_repo/jobs"

# Enable both example apps
PLUGINS = [
    "example_app",
    "example_app_with_view_override",
]

# Hard-code the SECRET_KEY for simplicity
SECRET_KEY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # noqa: S105  # hardcoded-password-string

# Redis variables

# Use *different* redis_databases than the ones (0 and 1) used during non-automated-testing operations.
CACHES["default"]["LOCATION"] = parse_redis_connection(redis_database=2)  # noqa: F405  # undefined-local-with-import-star-usage

# Testing storages within cli.py
#STORAGE_CONFIG = {
#    "AWS_ACCESS_KEY_ID": "ASFWDAMWWOQMEOQMWPMDA<WPDA",
#    "AWS_SECRET_ACCESS_KEY": "ASFKMWADMsacasdaw/dawrt1231541231231",
#    "AWS_STORAGE_BUCKET_NAME": "nautobot",
#    "AWS_S3_REGION_NAME": "us-west-1",
#}

# Use in-memory Constance backend instead of database backend so that settings don't leak between parallel tests.
CONSTANCE_BACKEND = "constance.backends.memory.MemoryBackend"

# Enable test data factories, as they're a pre-requisite for Nautobot core tests.
TEST_USE_FACTORIES = True
# For now, use a constant PRNG seed for consistent results. In the future we can remove this for fuzzier testing.
TEST_FACTORY_SEED = "Nautobot"

# Make Celery run synchronously (eager), to always store eager results, and run the broker in-memory.
# NOTE: Celery does not honor the TASK_TRACK_STARTED config when running in eager mode, so the job result is not saved until after the task completes.
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_STORE_EAGER_RESULT = True
CELERY_BROKER_URL = "memory://"
CELERY_TASK_DEFAULT_QUEUE = "default"

# Metrics need to enabled in this config as overriding them with override_settings will not actually enable them
METRICS_ENABLED = True

METRICS_AUTHENTICATED = True

CONTENT_TYPE_CACHE_TIMEOUT = 0

# Path to the kubernetes pod manifest yaml file used to create a job pod in the kubernetes cluster.
KUBERNETES_JOB_MANIFEST = {
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {"name": "nautobot-job"},
    "spec": {
        "ttlSecondsAfterFinished": 5,
        "template": {
            "spec": {
                "containers": [
                    {
                        "env": [
                            {
                                "name": "MYSQL_DATABASE",
                                "valueFrom": {"configMapKeyRef": {"key": "MYSQL_DATABASE", "name": "dev-env"}},
                            },
                            {
                                "name": "MYSQL_PASSWORD",
                                "valueFrom": {"configMapKeyRef": {"key": "MYSQL_PASSWORD", "name": "dev-env"}},
                            },
                            {
                                "name": "MYSQL_ROOT_PASSWORD",
                                "valueFrom": {"configMapKeyRef": {"key": "MYSQL_ROOT_PASSWORD", "name": "dev-env"}},
                            },
                            {
                                "name": "MYSQL_USER",
                                "valueFrom": {"configMapKeyRef": {"key": "MYSQL_USER", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_ALLOWED_HOSTS",
                                "valueFrom": {"configMapKeyRef": {"key": "NAUTOBOT_ALLOWED_HOSTS", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_CHANGELOG_RETENTION",
                                "valueFrom": {
                                    "configMapKeyRef": {"key": "NAUTOBOT_CHANGELOG_RETENTION", "name": "dev-env"}
                                },
                            },
                            {
                                "name": "NAUTOBOT_CONFIG",
                                "valueFrom": {"configMapKeyRef": {"key": "NAUTOBOT_CONFIG", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_CREATE_SUPERUSER",
                                "valueFrom": {
                                    "configMapKeyRef": {"key": "NAUTOBOT_CREATE_SUPERUSER", "name": "dev-env"}
                                },
                            },
                            {
                                "name": "NAUTOBOT_DB_HOST",
                                "valueFrom": {"configMapKeyRef": {"key": "NAUTOBOT_DB_HOST", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_DB_NAME",
                                "valueFrom": {"configMapKeyRef": {"key": "NAUTOBOT_DB_NAME", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_DB_PASSWORD",
                                "valueFrom": {"configMapKeyRef": {"key": "NAUTOBOT_DB_PASSWORD", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_DB_TIMEOUT",
                                "valueFrom": {"configMapKeyRef": {"key": "NAUTOBOT_DB_TIMEOUT", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_DB_USER",
                                "valueFrom": {"configMapKeyRef": {"key": "NAUTOBOT_DB_USER", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_INSTALLATION_METRICS_ENABLED",
                                "valueFrom": {
                                    "configMapKeyRef": {
                                        "key": "NAUTOBOT_INSTALLATION_METRICS_ENABLED",
                                        "name": "dev-env",
                                    }
                                },
                            },
                            {
                                "name": "NAUTOBOT_LOG_DEPRECATION_WARNINGS",
                                "valueFrom": {
                                    "configMapKeyRef": {"key": "NAUTOBOT_LOG_DEPRECATION_WARNINGS", "name": "dev-env"}
                                },
                            },
                            {
                                "name": "NAUTOBOT_NAPALM_TIMEOUT",
                                "valueFrom": {"configMapKeyRef": {"key": "NAUTOBOT_NAPALM_TIMEOUT", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_REDIS_HOST",
                                "valueFrom": {"configMapKeyRef": {"key": "NAUTOBOT_REDIS_HOST", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_REDIS_PASSWORD",
                                "valueFrom": {"configMapKeyRef": {"key": "NAUTOBOT_REDIS_PASSWORD", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_REDIS_PORT",
                                "valueFrom": {"configMapKeyRef": {"key": "NAUTOBOT_REDIS_PORT", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_SECRET_KEY",
                                "valueFrom": {"configMapKeyRef": {"key": "NAUTOBOT_SECRET_KEY", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_SELENIUM_HOST",
                                "valueFrom": {"configMapKeyRef": {"key": "NAUTOBOT_SELENIUM_HOST", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_SELENIUM_URL",
                                "valueFrom": {"configMapKeyRef": {"key": "NAUTOBOT_SELENIUM_URL", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_SUPERUSER_API_TOKEN",
                                "valueFrom": {
                                    "configMapKeyRef": {"key": "NAUTOBOT_SUPERUSER_API_TOKEN", "name": "dev-env"}
                                },
                            },
                            {
                                "name": "NAUTOBOT_SUPERUSER_EMAIL",
                                "valueFrom": {
                                    "configMapKeyRef": {"key": "NAUTOBOT_SUPERUSER_EMAIL", "name": "dev-env"}
                                },
                            },
                            {
                                "name": "NAUTOBOT_SUPERUSER_NAME",
                                "valueFrom": {"configMapKeyRef": {"key": "NAUTOBOT_SUPERUSER_NAME", "name": "dev-env"}},
                            },
                            {
                                "name": "NAUTOBOT_SUPERUSER_PASSWORD",
                                "valueFrom": {
                                    "configMapKeyRef": {"key": "NAUTOBOT_SUPERUSER_PASSWORD", "name": "dev-env"}
                                },
                            },
                            {
                                "name": "PGPASSWORD",
                                "valueFrom": {"configMapKeyRef": {"key": "PGPASSWORD", "name": "dev-env"}},
                            },
                            {
                                "name": "POSTGRES_DB",
                                "valueFrom": {"configMapKeyRef": {"key": "POSTGRES_DB", "name": "dev-env"}},
                            },
                            {
                                "name": "POSTGRES_PASSWORD",
                                "valueFrom": {"configMapKeyRef": {"key": "POSTGRES_PASSWORD", "name": "dev-env"}},
                            },
                            {
                                "name": "POSTGRES_USER",
                                "valueFrom": {"configMapKeyRef": {"key": "POSTGRES_USER", "name": "dev-env"}},
                            },
                            {
                                "name": "REDISCLI_AUTH",
                                "valueFrom": {"configMapKeyRef": {"key": "REDISCLI_AUTH", "name": "dev-env"}},
                            },
                            {
                                "name": "REDIS_PASSWORD",
                                "valueFrom": {"configMapKeyRef": {"key": "REDIS_PASSWORD", "name": "dev-env"}},
                            },
                        ],
                        "name": "nautobot-job",
                        "image": "local/nautobot-dev:local-py3.11",
                        "ports": [{"containerPort": 8080, "protocol": "TCP"}],
                        "tty": True,
                        "volumeMounts": [
                            {"mountPath": "/opt/nautobot/media", "name": "media-root"},
                            {
                                "mountPath": "/opt/nautobot/nautobot_config.py",
                                "name": "nautobot-cm1",
                                "subPath": "nautobot_config.py",
                            },
                        ],
                    }
                ],
                "volumes": [
                    {"name": "media-root", "persistentVolumeClaim": {"claimName": "media-root"}},
                    {
                        "configMap": {
                            "items": [{"key": "nautobot_config.py", "path": "nautobot_config.py"}],
                            "name": "nautobot-cm1",
                        },
                        "name": "nautobot-cm1",
                    },
                ],
                "restartPolicy": "Never",
            }
        },
        "backoffLimit": 0,
    },
}

# Name of the kubernetes pod created in the kubernetes cluster
KUBERNETES_JOB_POD_NAME = "nautobot-job"

# Namespace of the kubernetes pod created in the kubernetes cluster
KUBERNETES_JOB_POD_NAMESPACE = "default"

# Host of the kubernetes pod created in the kubernetes cluster
KUBERNETES_DEFAULT_SERVICE_ADDRESS = "https://kubernetes.default.svc"
```

## Setup Instructions

### Prepare Nautobot

1. **Clone and setup Nautobot:**
   ```bash
   git clone https://github.com/nautobot/nautobot
   cd nautobot
   ```

2. **Checkout a release version:**
   ```bash
   git checkout <release-tag> # or use 'develop' with caution
   ```

3. **Install dependencies:**
   ```bash
   poetry lock
   poetry install
   ```

4. **Enter Poetry shell:**
   ```bash
   # For Poetry 1.x
   poetry shell
   
   # For Poetry 2.x
   alias poetry-shell='eval $(poetry env activate)'
   poetry-shell
   ```

5. **Make configuration changes:**
   - Modify Dockerfile and ./development files as needed
   - Optionally copy your `testing_nautobot_config.py` into the container now or on Step-9

6. **Build the Docker container:**
   ```bash
   invoke build
   ```

7. **Start the container:**
   ```bash
   invoke start
   ```

8. **Wait for initialization:**
   Monitor the migration progress:
   ```bash
   docker logs -f <container-name>
   # Example: docker logs -f nautobot-2-4-nautobot-1
   ```
   
   > **Tip:** Use `docker ps` to see container names

### Prepare Secrets and Git Repository

9. **Copy test configuration (if not done in step 5):**
   ```bash
   docker cp testing_nautobot_config.py <container-id>:/opt/nautobot/testing_nautobot_config.py
   ```

10. **Login to Nautobot:**
    - Use credentials from ./development config (default: `admin`/`admin`)

11. **Create Secret objects:**
    - HTTP(S) → Token → environment variable
    - HTTP(S) → Username → environment variable

12. **Create Secrets Group:**
    - Group the secret objects together

13. **Create Git Repository object:**
    - Add your example tests repository
    - Run repository sync to download contents to disk

### Running Job Tests

14. **Access the container shell:**
    ```bash
    docker exec -it <container-name> /bin/bash
    ```

15. **Set environment variables (optional):**
    ```bash
    export JOBS_ROOT="/opt/nautobot/git/test_git_repo/jobs"
    export GIT_ROOT="/tmp/nautobot/git-tests" # Sending to anywhere but our actual GIT Root!
    ```

16. **Run the test case:**
    ```bash
    nautobot-server test "/opt/nautobot/git/test_git_repo/tests" \
      --config=/opt/nautobot/testing_nautobot_config.py \
      -v 2 --keepdb --buffer --pattern="test_case.py"
    ```

## Example Test Output

```
Creating 10 supported data rates without any associated objects...
Creating 10 job queues...
Creating 10 tenants without any associated objects...
Creating 20 dynamic groups and StaticGroupAssociations...
Creating 12 metadata types on all content-types...
Creating 24 metadata types on various content-types...
Creating 100 metadata choices...
Creating 100 object changes...
Creating 30 job queues...
Creating 20 job results...
Creating 100 job log entries...
Creating 100 object metadata...
Creating 20 object metadata with contacts...
Creating 20 object metadata with teams...
Database default populated successfully!
System check identified no issues (0 silenced).
test_my_job (test_git_repo.tests.test_case.MyJobTestCase.test_my_job) ... ok

----------------------------------------------------------------------
Ran 1 test in 4.387s

OK
Emptying test database "default"...
Database default emptied!
Preserving test database for alias 'default' ('test_nautobot')...
```

