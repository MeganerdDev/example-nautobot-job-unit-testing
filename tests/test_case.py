from django.test import override_settings
from nautobot.apps.testing import TransactionTestCase, get_job_class_and_model, run_job_for_testing
from nautobot.apps.jobs import get_job
from nautobot.extras.models import JobLogEntry, Job

import time

# modified from docs:
# https://docs.nautobot.com/projects/core/en/stable/development/jobs/testing/?h=transactiontest#running-a-job-in-a-test


MODULE = "example_custom_form"
CLASS = "ExampleCustomFormJob"
CLASS_PATH = f"{MODULE}.{CLASS}"


@override_settings(JOBS_ROOT="/opt/nautobot/git/test_git_repo/jobs")
class MyJobTestCase(TransactionTestCase):
    databases = ("default", "job_logs")

    def _collect_logs(self, job_result_id: int, max_wait_s: float = 3.0, poll_interval: float = 0.05) -> list[str]:
        """Poll the job for the full job results."""
        deadline = time.time() + max_wait_s
        appended: list[str] = []
        seen: set[tuple] = set() # schema: (created_iso, message)

        while time.time() < deadline:
            rows_job = list(
                JobLogEntry.objects.using("job_logs")
                .filter(job_result_id=job_result_id)
                .order_by("created", "id")
                .values("created", "message")
            )
            rows_def = list(
                JobLogEntry.objects.using("default")
                .filter(job_result_id=job_result_id)
                .order_by("created", "id")
                .values("created", "message")
            )
            merged = rows_job + [r for r in rows_def if r not in rows_job]
            for r in merged:
                created_iso = r["created"].isoformat() if hasattr(r["created"], "isoformat") else str(r["created"])
                key = (created_iso, r["message"])
                if key not in seen:
                    seen.add(key)
                    appended.append(r["message"])

            time.sleep(poll_interval)

        return appended

    def test_my_job(self) -> None:
        # ensure latest job code, prevent cache
        job_class = get_job(CLASS_PATH, reload=True)
        self.assertIsNotNone(job_class)

        # resolve the job_model and then enable the job in the test database
        job_model = Job.objects.get(module_name=MODULE, job_class_name=CLASS)
        job_model.enabled = True
        job_model.validated_save()
        self.assertIsNotNone(job_model)

        # NOTE: we can use `get_job_class_and_model` which does the same as the above, and marks the job as enabled in the database
        # job_class, job_model = get_job_class_and_model(MODULE, CLASS, source="local")
        # self.assertIsNotNone(job_model)

        job_result = run_job_for_testing(
            job_model,
            var1="hello world",
            log_level="DEBUG"
        )

        msgs = self._collect_logs(job_result.id, max_wait_s=3.0)

        print(f"job messages: {msgs}")
        self.assertTrue(any("hello" in m.lower() for m in msgs))
