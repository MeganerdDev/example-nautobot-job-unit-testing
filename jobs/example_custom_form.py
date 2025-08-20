from nautobot.apps.jobs import Job, register_jobs, StringVar


class ExampleCustomFormJob(Job):
    var1 = StringVar(label="Input data", description="Text to echo", default="hello universe")

    class Meta:
        name = "Custom form."
        has_sensitive_variables = False

    def run(self, var1: str):  # pylint:disable=arguments-differ
        """Run the job."""
        self.logger.info(f"received: {var1}")
        self.logger.success("done") # NOTE: nautobot >=2.4


register_jobs(ExampleCustomFormJob)

