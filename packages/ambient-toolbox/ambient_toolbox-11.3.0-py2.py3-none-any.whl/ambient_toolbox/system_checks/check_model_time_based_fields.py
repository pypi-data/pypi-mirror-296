from django.apps import apps
from django.conf import settings
from django.db.models import DateField, DateTimeField


def check_model_time_based_fields():
    """
    Checks all model time fields ('DateField', 'DateTimeField') for a "correct" ending in their name.
    """
    project_apps = [
        app.split(".")[-1] for app in settings.INSTALLED_APPS if app.startswith(settings.ROOT_URLCONF.split(".")[0])
    ]
    results = []

    # Iterate all registered models...
    for model in apps.get_models():
        # Check if the model is from your project...
        if model._meta.app_label in project_apps:
            # Iterate over all fields...
            for field in model._meta.get_fields():
                # TODO: have a whiteliste for "good" endings via settings-variable
                #  (get from scrubber? do we have some here?)
                if isinstance(field.__class, DateField):
                    if not (field.name.lower().endswith("_date") or field.name.lower().endswith("_at")):
                        results.append(f"Model '{model.__name__}.{field.name}' doesn't end with '_date' or '_at'.")
                elif isinstance(field.__class, DateTimeField):
                    if not (field.name.lower().endswith("_date") or field.name.lower().endswith("_at")):
                        results.append(f"Model '{model.__name__}.{field.name}' doesn't end with '_date' or '_at'.")

    # TODO: throw system check warning per finding instead of return
    return results
