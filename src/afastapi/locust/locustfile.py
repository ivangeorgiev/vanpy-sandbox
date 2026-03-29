from locust import HttpUser, task

# class SynUser(HttpUser):
#     host = "http://localhost:8080/api"

#     @task
#     def hello_world(self):
#         self.client.get("/hello-sync/")

class DefaultUser(HttpUser):
    host = "http://localhost:8080/api/hello-sync/"

    @task
    def hello_world(self):
        self.client.get("")

# class AsyncUser(HttpUser):
#     host = "http://localhost:8080/api"

#     @task
#     def hello_world(self):
#         self.client.get("/hello-async/")
