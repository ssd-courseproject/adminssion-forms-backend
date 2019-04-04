from flask_restful import Resource


class TestsList(Resource):
    def get(self):
        pass


class TestManagement(Resource):
    def post(self):
        pass

    def get(self, test_id):
        pass

    def put(self, test_id):
        pass

    def delete(self, test_id):
        pass


class TestSubmissions(Resource):
    def get(self, test_id):
        pass


class TestStart(Resource):
    def post(self, test_id):
        pass
