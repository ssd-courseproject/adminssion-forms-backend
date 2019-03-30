import json
from server import application


def application_add_spec():
    # Register entities and paths
    # application.spec.components.schema("Category", schema=CategorySchema)
    # application.spec.components.schema("Pet", schema=PetSchema)
    with application.app.test_request_context():
        # application.spec.path(view=
        pass


def generate_spec():
    return json.dumps(application.spec.to_dict(), indent=2)
