__version__ = "1.0.0"


## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features.
def get_provider_info():
    return {
        "package-name": "airflow-provider-datazone",
        "name": "Datazone",
        "description": "A provider for Datazone Connection and Operators",
        "connection-types": [
            {
                "connection-type": "datazone",
                "hook-class-name": "datazone_provider.hooks.datazone.DatazoneHook",
            }
        ],
        "extra-links": [
            "datazone_provider.operators.datazone.DatazoneRunExecutionOperatorExtraLink"
        ],
        "versions": [__version__],  # Required
    }
