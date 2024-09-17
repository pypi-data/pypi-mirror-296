from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING, Optional

from entegywrapper.errors import EntegyFailedRequestError
from entegywrapper.schemas.content import Document, ExternalContent, TemplateType

if TYPE_CHECKING:
    from entegywrapper import EntegyAPI

sys.path.append(os.path.dirname(__file__))


def add_documents(
    self: EntegyAPI,
    template_type: TemplateType,
    file_documents: list[Document],
    module_id: Optional[int] = None,
    external_reference: Optional[str] = None,
):
    """
    Adds documents to a page.

    Parameters
    ----------
        `template_type` (`TemplateType`): the templateType of the page to add the documents to

        `file_documents` (`list[Document]`): the file documents to add

        `module_id` (`int`): the moduleId of the page to add the documents to

        `external_reference` (`str`): the externalReference of the page to add the documents to

    Raises
    ------
        `ValueError`: if no identifier is specified

        `EntegyFailedRequestError`: if the API request fails
    """
    data = {
        "templateType": template_type,
        "fileDocuments": [document.model_dump() for document in file_documents],
    }

    if module_id is not None:
        data["moduleId"] = module_id
    elif external_reference is not None:
        data["externalReference"] = external_reference
    else:
        raise ValueError("Please specify an identifier")

    response = self.post(self.api_endpoint + "/v2/Document/AddFile", data=data)

    match response["response"]:
        case 200:
            return
        case _:
            raise EntegyFailedRequestError(
                f"{response['response']}: {response.get('message', 'Unknown error')}"
            )


def add_external_content_documents(
    self: EntegyAPI,
    template_type: TemplateType,
    external_content_items: list[ExternalContent],
    module_id: Optional[int] = None,
    external_reference: Optional[str] = None,
):
    """
    Adds external content documents to a page.

    Parameters
    ----------
        `template_type` (`TemplateType`): the templateType of the page to add the documents to

        `external_content_items` (`list[ExternalContent]`): the external content documents to add

        `module_id` (`int`): the moduleId of the page to add the documents to

        `external_reference` (`str`): the externalReference of the page to add the documents to

    Raises
    ------
        `ValueError`: if no identifier is specified

        `EntegyFailedRequestError`: if the API request fails
    """
    data = {
        "templateType": template_type,
        "externalContentItems": external_content_items,
    }

    if module_id is not None:
        data["moduleId"] = module_id
    elif external_reference is not None:
        data["externalReference"] = external_reference
    else:
        raise ValueError("Please specify an identifier")

    response = self.post(self.api_endpoint + "/v2/Document/AddExternalContent", data=data)

    match response["response"]:
        case 200:
            return
        case _:
            raise EntegyFailedRequestError(
                f"{response['response']}: {response.get('message', 'Unknown error')}"
            )
