from locust import HttpUser, task, between

class FermataCompleteProjectUser(HttpUser):
    # ተጠቃሚው ከአንድ ጥያቄ ወደ ሌላ ሲሸጋገር ከ 1 እስከ 3 ሰከንድ ይጠብቃል
    wait_time = between(1, 3)

    @task(5)
    def test_buses(self):
        self.client.get("/api/buses/")

    @task(4)
    def test_routes(self):
        self.client.get("/api/routes/")

    @task(4)
    def test_users(self):
        self.client.get("/api/users/")

    @task(3)
    def test_comments(self):
        self.client.get("/api/comments/")

    @task(3)
    def test_worker(self):
        self.client.get("/api/worker/")

    @task(2)
    def test_home(self):
        self.client.get("/api/home")

    @task(2)
    def test_about(self):
        self.client.get("/api/about/")

    @task(2)
    def test_get_ticket(self):
        self.client.get("/api/get_ticket/")

    @task(2)
    def test_city(self):
        self.client.get("/api/city/")

    @task(1)
    def test_service_fee(self):
        self.client.get("/api/service_fee/")

    @task(1)
    def test_select_bus(self):
        self.client.get("/api/Selectbus/")

    @task(1)
    def test_schema(self):
        self.client.get("/api/schema/")

    @task(1)
    def test_docs(self):
        self.client.get("/api/docs/")
