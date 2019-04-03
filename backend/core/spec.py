import json

from backend.core.backend_app import FormsBackend


def application_add_spec(application: FormsBackend):
    """
    Register entities and paths
    """
    # application.spec.components.schema("Category", schema=CategorySchema)
    # application.spec.components.schema("Pet", schema=PetSchema)
    with application.app.test_request_context():
        # application.spec.path(view=)
        pass


def generate_spec(application: FormsBackend):
    return json.dumps(application.spec.to_dict(), indent=2)
