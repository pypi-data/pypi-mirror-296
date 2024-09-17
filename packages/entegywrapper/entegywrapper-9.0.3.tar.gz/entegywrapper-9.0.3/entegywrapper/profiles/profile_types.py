from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from entegywrapper.errors import EntegyFailedRequestError, EntegyNoDataError
from entegywrapper.schemas.profile import ProfileType

if TYPE_CHECKING:
    from entegywrapper import EntegyAPI


def get_profile_type(
    self: EntegyAPI,
    *,
    name: Optional[str] = None,
    external_reference: Optional[str] = None,
) -> ProfileType:
    """
    Returns the profile type specified by the given identifier.

    Parameters
    ----------
        `name` (`str`, optional): the name of the profile type; defaults to `None`

        `external_reference` (`str`, optional): the externalReference of the profile type; defaults to `None`

    Raises
    ------
        `ValueError`: if no identifier is specified

        `EntegyFailedRequestError`: if the API request fails

    Returns
    -------
        `ProfileType`: the profile type specified by the given identifier
    """
    data = {}

    if name is not None:
        data["name"] = name
    elif external_reference is not None:
        data["externalReference"] = external_reference
    else:
        raise ValueError("Please specify an identifier")

    response = self.post(self.api_endpoint + "/v2/ProfileType", data=data)

    match response["response"]:
        case 200:
            return ProfileType(**response["profileType"])
        case 401:
            raise EntegyFailedRequestError("Profile type not found")
        case _:
            raise EntegyFailedRequestError(
                f"{response['response']}: {response.get('message', 'Unknown error')}"
            )


def create_profile_type(self: EntegyAPI, profile_type: ProfileType):
    """
    Creates a profile type from the given data.

    Parameters
    ----------
        `profile_type` (`ProfileType`): the data for the profile type to create

    Raises
    ------
        `EntegyFailedRequestError`: if the API request fails
    """
    data = {"profileType": profile_type.model_dump()}

    response = self.post(self.api_endpoint + "/v2/ProfileType/Create", data=data)

    match response["response"]:
        case 200:
            return
        case 402:
            raise EntegyFailedRequestError("Missing Data")
        case 404:
            raise EntegyFailedRequestError("Malformed Data")
        case 405:
            raise EntegyFailedRequestError("Name is empty")
        case 406:
            raise EntegyFailedRequestError("External reference isn't unique")
        case _:
            raise EntegyFailedRequestError(
                f"{response['response']}: {response.get('message', 'Unknown error')}"
            )


def update_profile_type(
    self: EntegyAPI,
    profile_type: ProfileType,
    *,
    name: Optional[str] = None,
    external_reference: Optional[str] = None,
):
    """
    Updates the profile type with the data passed in the profileType

    Parameters
    ----------
        `profile_type` (`ProfileType`): the data to update

        `name` (`str`, optional): the name of the profile type; defaults to `None`

        `external_reference` (`str`, optional): the externalReference of the profile type; defaults to `None`

    Raises
    ------
        `ValueError`: if no identifier is specified

        `EntegyFailedRequestError`: if the API request fails
    """
    data = {"profileType": profile_type}

    if name is not None:
        data["name"] = name
    elif external_reference is not None:
        data["externalReference"] = external_reference
    else:
        raise ValueError("Please specify an identifier")

    response = self.post(self.api_endpoint + "/v2/ProfileType/Update", data=data)

    match response["response"]:
        case 200:
            return
        case 401:
            raise EntegyFailedRequestError("Profile type not found")
        case 402:
            raise EntegyFailedRequestError("Missing Data")
        case 404:
            raise EntegyFailedRequestError("Malformed Data")
        case 405:
            raise EntegyFailedRequestError("Name is empty")
        case 406:
            raise EntegyFailedRequestError("External reference isn't unique")
        case _:
            raise EntegyFailedRequestError(
                f"{response['response']}: {response.get('message', 'Unknown error')}"
            )


def delete_profile_type(
    self: EntegyAPI,
    *,
    name: Optional[str] = None,
    external_reference: Optional[str] = None,
):
    """
    Deletes a profile type. The type cannot be in use.

    Parameters
    ----------
        `name` (`str`, optional): the name of the profile type; defaults to `None`

        `external_reference` (`str`, optional): the externalReference of the profile type; defaults to `None`

    Raises
    ------
        `ValueError`: if no identifier is specified

        `EntegyFailedRequestError`: if the API request fails
    """
    data = {}

    if name is not None:
        data["name"] = name
    elif external_reference is not None:
        data["externalReference"] = external_reference
    else:
        raise ValueError("Please specify an identifier")

    response = self.delete(self.api_endpoint + "/v2/ProfileType/Delete", data=data)

    match response["response"]:
        case 200:
            return
        case 401:
            raise EntegyFailedRequestError("Profile type not found")
        case 402:
            raise EntegyFailedRequestError("profile type in use")
        case _:
            raise EntegyFailedRequestError(
                f"{response['response']}: {response.get('message', 'Unknown error')}"
            )


def all_profile_types(self) -> list[ProfileType]:
    """
    Returns a list of all profile types.

    Raises
    ------
        `EntegyNoDataError`: if no profile types are found

    Returns
    -------
        `list[ProfileType]`: all profile types
    """
    data = {}

    response = self.post(self.api_endpoint + "/v2/ProfileType/All", data=data)

    if "profileTypes" not in response:
        raise EntegyNoDataError("No profile types found")

    return [ProfileType(**profile_type) for profile_type in response["profileTypes"]]
