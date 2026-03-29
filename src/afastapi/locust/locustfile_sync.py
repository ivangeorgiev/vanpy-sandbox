from locust import HttpUser, task

class SynUser(HttpUser):
    host = "http://localhost:8080/api"

    @task
    def hello_world(self):
        self.client.get("/hello-sync/")
