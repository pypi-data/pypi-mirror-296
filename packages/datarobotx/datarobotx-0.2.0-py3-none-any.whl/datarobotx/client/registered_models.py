import logging

from datarobotx.common.client import raise_value_error, session
from datarobotx.common.types import ModelKind

logger = logging.getLogger("drx")


async def create_external_registered_model(
    name: str, description: str, target_name: str, model_kind: ModelKind
) -> str:
    """Create a registered model for external deployment.
    Note relies on `/modelPackage/fromJSON` which is undocumented.
    """
    #     if model_id is not None:
    #     payload["modelId"] = model_id
    # if model_description is not None:
    #     payload["modelDescription"] = model_description
    # if datasets is not None:
    #     payload["datasets"] = datasets
    # if timeseries is not None:
    #     payload["timeseries"] = timeseries
    # if registered_model_name is not None:
    #     payload["registeredModelName"] = registered_model_name
    # if registered_model_id is not None:
    #     payload["registeredModelId"] = registered_model_id
    # if tags is not None:
    #     payload["tags"] = tags
    # if registered_model_tags is not None:
    #     payload["registeredModelTags"] = registered_model_tags
    # if registered_model_description is not None:
    #     payload["registeredModelDescription"] = registered_model_description
    if model_kind.isBinary:
        target_type_payload = "Binary"
    elif model_kind.isRegression:
        target_type_payload = "Regression"
    elif model_kind.isTextGen:
        target_type_payload = "TextGeneration"
    elif model_kind.isMultiClass:
        target_type_payload = "Multiclass"
    elif model_kind.isMultilabel:
        target_type_payload = "Multilable"
    model_description = {
        "modelName": name,
        "description": description,
        "buildEnvironmentType": "Other",
        "location": "Other",
    }
    json = {
        # "modelDescription": description,
        "registeredModelName": name,
        "registeredModelDescription": description,
        "modelDescription": model_description,
        "name": name,
        "target": {"name": target_name, "type": target_type_payload},
    }
    url = "/modelPackages/fromJSON"
    async with session.post(url, json=json) as resp:
        if resp.status == 201:
            json = await resp.json()
        else:
            await raise_value_error(resp)
    return str(json["id"])


async def create_registered_model_from_datarobot_model(
    name: str,
    description: str,
    model_id: str,
    registered_model_id: str = None,
) -> str:
    url = "/modelPackages/fromLeaderboard"
    if registered_model_id:
        json = {
            "modelId": model_id,
            "name": name,
            "description": description,
            "registeredModelId": registered_model_id,
        }
    else:
        json = {"modelId": model_id, "name": name, "description": description}
    async with session.post(url, json=json) as resp:
        if resp.status in (202, 200):
            json = await resp.json()
        else:
            await raise_value_error(resp)
    return str(json["id"])
