from locust import FastHttpUser, task, constant_throughput


class QuickstartUser(FastHttpUser):
    wait_time = constant_throughput(5)

    def get(self, *args, **kwargs):
        kwargs['verify'] = False
        return self.client.get(*args, **kwargs)

    @task
    def get_root(self):
        self.get("/", verify=False)

    @task
    def get_api(self):
        self.get("/api/v1", verify=False)
