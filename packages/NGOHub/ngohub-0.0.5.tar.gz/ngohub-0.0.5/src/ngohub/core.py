from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Dict, List, Union

from ngohub.exceptions import HubHTTPException, MissingUserException
from ngohub.network import HTTPClient, HTTPClientResponse


class BaseHub(ABC):
    """
    Abstract class used to define all the required methods for a hub interface
    """

    @abstractmethod
    def __init__(self, api_base_url: str) -> None:
        self.api_base_url: str = api_base_url or ""


class NGOHub(BaseHub):
    def __init__(self, api_base_url: str) -> None:
        super().__init__(api_base_url)

        self.client: HTTPClient = HTTPClient(self.api_base_url)

    def is_healthy(self) -> bool:
        response: HTTPClientResponse = self.client.api_get("/health/")

        response_is_ok: bool = response.to_str() == "OK"

        return response_is_ok

    def get_version(self) -> Dict[str, str]:
        response: HTTPClientResponse = self.client.api_get("/version/")

        response_dict: Dict = response.to_dict()
        version_revision: Dict[str, str] = {
            "version": response_dict["version"],
            "revision": response_dict["revision"],
        }

        return version_revision

    def get_file_url(self, path: str) -> str:
        response: HTTPClientResponse = self.client.api_get(f"/file?path={path}")

        return response.to_str()

    def _get_nomenclature(self, nomenclature: str) -> Any:
        response: HTTPClientResponse = self.client.api_get(f"/nomenclatures/{nomenclature}")

        return response.to_dict()

    def get_cities_nomenclatures(
        self, search: str = None, county_id: int = None, city_id: int = None
    ) -> List[Dict[str, Any]]:
        mandatory_params: List[Any] = [search, county_id]
        if all(param is None for param in mandatory_params):
            raise ValueError("Please provide at least one of the following: county_id, search")

        search_query: List[str] = []
        if search:
            search_query.append(f"search={search}")
        if county_id:
            search_query.append(f"countyId={county_id}")
        if city_id:
            search_query.append(f"cityId={city_id}")

        return self._get_nomenclature(f"cities?{'&'.join(search_query)}")

    def get_counties_nomenclatures(self) -> List[Dict[str, Any]]:
        return self._get_nomenclature("counties")

    def get_domains_nomenclatures(self):
        return self._get_nomenclature("domains")

    def get_regions_nomenclatures(self):
        return self._get_nomenclature("regions")

    def get_federations_nomenclatures(self):
        return self._get_nomenclature("federations")

    def get_coalitions_nomenclatures(self):
        return self._get_nomenclature("coalitions")

    def get_faculties_nomenclatures(self):
        return self._get_nomenclature("faculties")

    def get_skills_nomenclatures(self):
        return self._get_nomenclature("skills")

    def get_practice_domains_nomenclatures(self):
        return self._get_nomenclature("practice-domains")

    def get_service_domains_nomenclatures(self):
        return self._get_nomenclature("service-domains")

    def get_beneficiaries_nomenclatures(self):
        return self._get_nomenclature("beneficiaries")

    def get_issuers_nomenclatures(self):
        return self._get_nomenclature("issuers")

    # User related methods
    def get_profile(self, user_token: str) -> Dict[str, Any]:
        response: HTTPClientResponse = self.client.api_get("/profile/", token=user_token)

        return response.to_dict()

    # Organization related methods
    def get_organization_profile(self, ngo_token: str) -> Dict[str, Any]:
        response: HTTPClientResponse = self.client.api_get("/organization-profile/", token=ngo_token)

        return response.to_dict()

    def get_user_organization_applications(self, ngo_token: str) -> List[Dict[str, Any]]:
        response: HTTPClientResponse = self.client.api_get("/organization/applications/", token=ngo_token)

        return list(response.to_dict())

    def check_user_organization_has_application(self, ngo_token: str, login_link: str) -> Dict[str, Any]:
        organization_applications: List[Dict[str, Any]] = self.get_user_organization_applications(ngo_token)

        for app in organization_applications:
            if app["loginLink"].startswith(login_link) and app["status"] == "active" and app["ongStatus"] == "active":
                return app

        return {}

    # Admin related methods
    def get_application_list(self, admin_token: str) -> List[Dict[str, Any]]:
        response: HTTPClientResponse = self.client.api_get("/application/list/", token=admin_token)

        return list(response.to_dict())

    def get_organization(self, admin_token: str, organization_id: int) -> Dict[str, Any]:
        response: HTTPClientResponse = self.client.api_get(f"/organization/{organization_id}/", token=admin_token)

        return response.to_dict()

    def get_organization_applications(self, admin_token: str, organization_id: int) -> List[Dict[str, Any]]:
        response: HTTPClientResponse = self.client.api_get(
            f"/application/organization/{organization_id}/", token=admin_token
        )

        return list(response.to_dict())

    def get_user(self, admin_token: str, user_id: int) -> Dict[str, Any]:
        try:
            response: HTTPClientResponse = self.client.api_get(f"/user/{user_id}/", token=admin_token)
        except HubHTTPException as e:
            if e.status_code == 404:
                raise MissingUserException(f"User with ID {user_id} not found")

            raise e

        return response.to_dict()

    def get_users(
        self,
        admin_token: str,
        organization_id: int,
        limit: int = 1000,
        page: int = 1,
        search: str = None,
        order_by: str = None,
        order_direction: str = None,
        start: str = None,
        end: str = None,
        status: str = None,
        available_apps_ids: List[int] = None,
    ) -> Dict[str, Any]:
        request_url: str = f"/user?organization_id={organization_id}&limit={limit}&page={page}"
        if search:
            request_url += f"&search={search}"
        if order_by:
            request_url += f"&orderBy={order_by}"
        if order_direction and order_direction.upper() in ["ASC", "DESC"]:
            request_url += f"&orderDirection={order_direction.upper()}"
        if start:
            request_url += f"&start={start}"
        if end:
            request_url += f"&end={end}"
        if status and status.lower() in ["active", "pending", "restricted"]:
            request_url += f"&status={status}"
        if available_apps_ids:
            for app_id in available_apps_ids:
                request_url += f"&availableAppsIds={app_id}"

        response: HTTPClientResponse = self.client.api_get(request_url, token=admin_token)

        return response.to_dict()

    def check_organization_has_application(
        self, admin_token: str, organization_id: int, login_link: str
    ) -> Dict[str, Any]:
        organization_applications: List[Dict[str, Any]] = self.get_organization_applications(
            admin_token, organization_id
        )

        for application in organization_applications:
            if (
                application["loginLink"].startswith(login_link)
                and application["status"] == "active"
                and application["ongStatus"] == "active"
            ):
                return application

        return {}

    def _check_user_has_application(self, admin_token, organization_id, user_id, response) -> Dict[str, Any]:
        continue_searching: bool = True
        page: int = 1

        response: Dict[str, Any] = deepcopy(response)
        searched_application_id = response["application"]["id"]

        while continue_searching:
            organization_users: Dict[str, Union[Dict, List]] = self.get_users(
                admin_token=admin_token, organization_id=organization_id, page=page
            )

            response_metadata = organization_users.get("meta", {})
            response_users = organization_users.get("items", [])

            if response_metadata["totalPages"] <= response_metadata["currentPage"]:
                continue_searching = False
            else:
                page += 1

            for user in response_users:
                if user["id"] == int(user_id):
                    response["user"] = user
                    user_applications: List[Dict[str, Any]] = user["availableAppsIDs"]

                    if searched_application_id in user_applications:
                        response["access"] = True
                        return response

                    response["access"] = False
                    return response

        return response

    def check_organization_user_has_application(
        self,
        admin_token: str,
        organization_id: int,
        user_id: int,
        login_link: str,
    ) -> Dict[str, Any]:

        response: Dict[str, Any] = {"user": None, "application": None, "access": None}

        organization_application: Dict = self.check_organization_has_application(
            admin_token, organization_id, login_link
        )
        if not organization_application:
            return response

        response["application"] = organization_application

        try:
            user_information: Dict = self.get_user(admin_token, user_id)
        except MissingUserException:
            return response

        if not user_information or user_information.get("organizationId") != int(organization_id):
            return response

        response["user"] = user_information

        if user_information.get("role") == "admin":
            response["access"] = True

            return response

        response = self._check_user_has_application(admin_token, organization_id, user_id, response)

        return response
