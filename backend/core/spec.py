import json

from backend.core.backend_app import FormsBackend

jwt_scheme = {
    "type": "http",
    "description": "All requests except for `/auth/login` requires JWT token",
    "in": "header",
    "scheme": "bearer",
    "bearerFormat": "JWT"
}


def application_add_spec(application: FormsBackend):
    """
    Register entities and paths
    """
    # application.spec.components.schema("Category", schema=CategorySchema)
    # application.spec.components.schema("Pet", schema=PetSchema)

    application.spec.components.security_scheme("jwt", jwt_scheme)

    with application.app.test_request_context():
        # application.spec.path(view=)
        pass


def generate_spec(application: FormsBackend):
    return json.dumps(application.spec.to_dict(), indent=2)
