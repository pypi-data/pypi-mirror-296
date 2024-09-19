"""
Integration test suite for the API v1 views.
"""

from __future__ import annotations

import requests
from ddt import data as ddt_data
from ddt import ddt, unpack
from django.conf import settings as ds
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

settings = ds.INTEGRATION_TEST_SETTINGS

FAKE_USER_DATA = iter(
    [
        {
            "username": "athickpenny0",
            "email": "athickpenny0@indiegogo.com",
            "fullname": "Antoni Thickpenny",
            "password": "jD3_u)67VfHce",
            "activate_user": True,
            "mailing_address": "70736 Haas Parkway",
            "year_of_birth": 1996,
            "gender": "f",
            "level_of_education": "p",
            "city": "Solikamsk",
            "goals": "Maecenas leo odio, condimentum id",
        },
        {
            "username": "smenchenton1",
            "email": "smenchenton1@networksolutions.com",
            "fullname": "Sonia Menchenton",
            "password": "hO9\\Pni)",
            "activate_user": True,
            "mailing_address": "7543 Eagle Crest Terrace",
            "year_of_birth": 1998,
            "gender": "m",
            "level_of_education": "m",
            "city": "Diourbel",
            "goals": "Sed sagittis.",
        },
        {
            "username": "arealff2",
            "email": "arealff2@phpbb.com",
            "fullname": "Alexis Realff",
            "password": 'zY2(yq!(>4"_',
            "activate_user": True,
            "mailing_address": "0 Grim Drive",
            "year_of_birth": 2005,
            "gender": "f",
            "level_of_education": "b",
            "city": "Gongyi",
            "goals": "Proin interdum mauris non ligula pellentesque ultrices.",
        },
        {
            "username": "ddilon3",
            "email": "ddilon3@geocities.com",
            "fullname": "Dotty Dilon",
            "password": 'mV9"3zRdRr#bTP',
            "activate_user": True,
            "mailing_address": "6859 Lerdahl Road",
            "year_of_birth": 2002,
            "gender": "m",
            "level_of_education": "a",
            "city": "La Curva",
            "goals": "Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl.",
        },
        {
            "username": "lties4",
            "email": "lties4@addthis.com",
            "fullname": "Loreen Ties",
            "password": 'iU6@R"`/t3>/DT',
            "activate_user": True,
            "mailing_address": "64 Clemons Terrace",
            "year_of_birth": 1994,
            "gender": "f",
            "level_of_education": "hs",
            "city": "Xianyang",
            "goals": "In est risus, auctor sed, tristique in, tempus sit amet, sem.",
        },
        {
            "username": "lbattisson5",
            "email": "lbattisson5@360.cn",
            "fullname": "Lynett Battisson",
            "password": "oB3?1JWFM\\=S>",
            "activate_user": True,
            "mailing_address": "89 Vermont Pass",
            "year_of_birth": 2000,
            "gender": "m",
            "level_of_education": "jhs",
            "city": "Lyudinovo",
            "goals": "Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum.",
        },
        {
            "username": "jniset6",
            "email": "jniset6@virginia.edu",
            "fullname": "Jacquelin Niset",
            "password": "aC2/anhtj",
            "activate_user": True,
            "mailing_address": "83984 8th Pass",
            "year_of_birth": 2003,
            "gender": "f",
            "level_of_education": "el",
            "city": "Erie",
            "goals": "Donec quis orci eget orci vehicula condimentum.",
        },
        {
            "username": "mdoumenc7",
            "email": "mdoumenc7@chicagotribune.com",
            "fullname": "Martin Doumenc",
            "password": "dQ9't{0(",
            "activate_user": True,
            "mailing_address": "8 Scoville Plaza",
            "year_of_birth": 1993,
            "gender": "f",
            "level_of_education": "none",
            "city": "Boaco",
            "goals": "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae.",
        },
        {
            "username": "lchampagne8",
            "email": "lchampagne8@buzzfeed.com",
            "fullname": "Locke Champagne",
            "password": "tW7_SYC1qUf!K'0C",
            "activate_user": True,
            "mailing_address": "79 Milwaukee Place",
            "year_of_birth": 1996,
            "gender": "f",
            "level_of_education": "other",
            "city": "Linjiang",
            "goals": "In hac habitasse platea dictumst.",
        },
        {
            "username": "zczyz9",
            "email": "zczyz9@gravatar.com",
            "fullname": "Zolly Czyz",
            "password": "jN3~/&1ZMG%",
            "activate_user": True,
            "mailing_address": "5 Victoria Place",
            "year_of_birth": 2000,
            "gender": "f",
            "level_of_education": "p",
            "city": "'s-Hertogenbosch",
            "goals": "Suspendisse potenti.",
        },
        {
            "username": "athickpenny0",
            "email": "athickpenny0@indiegogo.com",
            "fullname": "Antoni Thickpenny",
            "password": "jD3_u)67VfHce",
            "activate_user": False,
            "mailing_address": "70736 Haas Parkway",
            "year_of_birth": 1996,
            "gender": "f",
            "level_of_education": "m",
            "city": "Solikamsk",
            "goals": "Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo.",
        },
    ]
)


class BaseAPIIntegrationTest(TestCase):
    """
    Base class for the integration test suite.
    """

    def setUp(self):
        """
        Set up the test suite.
        """
        self.default_site = self.get_tenant_data()
        self.tenant_x = self.get_tenant_data("tenant-x")
        self.tenant_y = self.get_tenant_data("tenant-y")

    def get_tenant_data(self, prefix: str = "") -> dict:
        """
        Get the tenant data.

        If no prefix is provided, the default site data is returned.

        Args:
            prefix (str): The tenant prefix.

        Returns:
            dict: The tenant data.
        """
        domain = f"{prefix}.{settings['LMS_BASE']}" if prefix else settings["LMS_BASE"]
        return {
            "base_url": f"http://{domain}",
            "domain": domain,
        }

    def get_access_token(self, tenant_base_url: str) -> str:
        """
        Get an access token for a tenant.

        Args:
            tenant_base_url (str): The tenant base URL.

        Returns:
            str: The access token.
        """
        data = {
            "client_id": settings["CLIENT_ID"],
            "client_secret": settings["CLIENT_SECRET"],
            "grant_type": "client_credentials",
        }
        url = f"{tenant_base_url}/oauth2/access_token/"
        response = requests.post(url, data=data, timeout=settings["API_TIMEOUT"])
        return response.json()["access_token"]

    # pylint: disable=too-many-arguments
    def make_request(
        self,
        tenant: dict,
        method: str,
        url: str,
        json: dict | None = None,
        data: dict | None = None,
        params: dict | None = None,
        with_auth: bool = True,
    ) -> requests.Response:
        """
        Make a request to a tenant.

        Args:
            tenant (dict): The tenant data.
            method (str): The HTTP method ('GET', 'POST', etc.).
            url (str): The URL to make the request to.
            json (dict, optional): The JSON data for POST, PATCH and PUT requests.
            data (dict, optional): The data for POST, PATCH and PUT requests.
            params (dict, optional): The parameters for GET and DELETE requests.
            with_auth (bool, optional): Whether to include the access token in the request headers.

        Returns:
            requests.Response: The response object.
        """
        headers = {"Host": tenant["domain"]}
        if with_auth:
            access_token = self.get_access_token(tenant["base_url"])
            headers["Authorization"] = f"Bearer {access_token}"
        full_url = f"{tenant['base_url']}/{url}"

        method = method.upper()
        if method not in ("GET", "POST", "PATCH"):
            raise ValueError(f"Unsupported HTTP method: {method}")

        return requests.request(
            method,
            full_url,
            json=json,
            data=data,
            params=params,
            headers=headers,
            timeout=settings["API_TIMEOUT"],
        )


@ddt
class TestUsersAPIIntegration(BaseAPIIntegrationTest):
    """Integration test suite for the Users API"""

    def setUp(self):
        """Set up the test suite"""
        self.user_url = f"{settings['EOX_CORE_API_BASE']}{reverse('eox-api:eox-api:edxapp-user')}"
        self.user_updater_url = f"{settings['EOX_CORE_API_BASE']}{reverse('eox-api:eox-api:edxapp-user-updater')}"
        super().setUp()

    def create_user_in_tenant(self, tenant: dict, user_data: dict) -> requests.Response:
        """
        Create a new user in a tenant.

        Args:
            tenant (dict): The tenant data.
            user_data (dict): The user data.

        Returns:
            requests.Response: The response object.
        """
        return self.make_request(tenant, "POST", url=self.user_url, data=user_data)

    def get_user_in_tenant(self, tenant: dict, params: dict | None = None) -> requests.Response:
        """
        Get a user in a tenant by username or email.

        Args:
            tenant (dict): The tenant data.
            params (dict, optional): The query parameters for the request.

        Returns:
            requests.Response: The response object.
        """
        return self.make_request(tenant, "GET", url=self.user_url, params=params)

    def update_user_in_tenant(self, tenant: dict, user_data: dict) -> requests.Response:
        """
        Update a user in a tenant.

        Args:
            tenant (dict): The tenant data.
            user_data (dict): The user data.

        Returns:
            requests.Response: The response object.
        """
        return self.make_request(tenant, "PATCH", url=self.user_updater_url, json=user_data)

    @ddt_data(
        {"is_staff": False, "is_superuser": False},
        {"is_staff": True, "is_superuser": False},
        {"is_staff": False, "is_superuser": True},
        {"is_staff": True, "is_superuser": True},
    )
    def test_create_user_in_tenant_success(self, permissions: dict) -> None:
        """
        Test creating a user in a tenant.

        Open edX definitions tested:
        - `create_edxapp_user`
        - `check_edxapp_account_conflicts`

        Expected result:
        - The status code is 200.
        - The user is created successfully in the tenant with the provided data.
        """
        data = next(FAKE_USER_DATA)
        data.update(permissions)

        response = self.create_user_in_tenant(self.tenant_x, data)

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["email"], data["email"])
        self.assertEqual(response_data["username"], data["username"])
        self.assertTrue(response_data["is_active"])
        self.assertFalse(response_data["is_staff"])
        self.assertFalse(response_data["is_superuser"])

    def test_create_user_missing_required_fields(self) -> None:
        """
        Test creating a user in a tenant with invalid data.

        Open edX definitions tested:
        - `check_edxapp_account_conflicts`

        Expected result:
        - The status code is 400.
        - The response contains the missing fields.
        - The user is not created in the tenant.
        """
        data = next(FAKE_USER_DATA)
        del data["email"]
        del data["username"]

        response = self.create_user_in_tenant(self.tenant_x, data)

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response_data)
        self.assertIn("username", response_data)

    def test_create_user_in_tenant_user_already_exists(self) -> None:
        """
        Test creating a user in a tenant that already exists.

        Open edX definitions tested:
        - `check_edxapp_account_conflicts`

        Expected result:
        - The status code is 400.
        - The response contains an error message.
        - The user is not created in the tenant.
        """
        data = next(FAKE_USER_DATA)
        self.create_user_in_tenant(self.tenant_x, data)

        response = self.create_user_in_tenant(self.tenant_x, data)

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response_data)

    @ddt_data("username", "email")
    def test_get_user_in_tenant_success(self, query_param: str) -> None:
        """
        Test getting a user in a tenant.

        Open edX definitions tested:
        - `get_edxapp_user`

        Expected result:
        - The status code is 200.
        - The response contains the user data.
        """
        data = next(FAKE_USER_DATA)
        self.create_user_in_tenant(self.tenant_x, data)

        response = self.get_user_in_tenant(self.tenant_x, {query_param: data[query_param]})

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data[query_param], data[query_param])

    def test_get_user_of_another_tenant(self) -> None:
        """
        Test getting a user that belongs to another tenant.

        Open edX definitions tested:
        - `get_edxapp_user`

        Expected result:
        - The status code is 404.
        - The response contains an error message.
        """
        data = next(FAKE_USER_DATA)
        self.create_user_in_tenant(self.tenant_x, data)

        response = self.get_user_in_tenant(self.tenant_y, {"username": data["username"]})

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response_data)
        self.assertEqual(
            response_data["detail"],
            f"No user found by {{'username': '{data['username']}'}} on site {self.tenant_y['domain']}.",
        )

    @ddt_data(
        ("username", "user-not-found"),
        ("email", "user-not-found@mail.com"),
    )
    @unpack
    def test_get_user_in_tenant_user_not_found(self, param: str, value: str) -> None:
        """
        Test getting a user in a tenant that does not exist.

        Open edX definitions tested:
        - `get_edxapp_user`

        Expected result:
        - The status code is 404.
        - The response contains an error message.
        """
        response = self.get_user_in_tenant(self.tenant_x, {param: value})

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response_data)
        self.assertEqual(
            response_data["detail"],
            f"No user found by {{'{param}': '{value}'}} on site {self.tenant_x['domain']}.",
        )

    def test_update_user_in_tenant_success(self) -> None:
        """
        Test updating a user in a tenant.

        Open edX definitions tested:
        - `get_edxapp_user`
        - `get_user_profile`
        - `check_edxapp_account_conflicts`
        - `get_user_read_only_serializer`

        Expected result:
        - The status code is 200.
        - The user is updated successfully in the tenant with the provided data.
        """
        data = next(FAKE_USER_DATA)
        self.create_user_in_tenant(self.tenant_x, data)
        updated_data = next(FAKE_USER_DATA)
        updated_data["username"] = data["username"]
        updated_data["email"] = data["email"]

        response = self.update_user_in_tenant(self.tenant_x, user_data=updated_data)

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["username"], data["username"])
        self.assertEqual(response_data["email"], data["email"])
        self.assertEqual(response_data["name"], updated_data["fullname"])
        self.assertEqual(response_data["mailing_address"], updated_data["mailing_address"])
        self.assertEqual(response_data["year_of_birth"], updated_data["year_of_birth"])
        self.assertEqual(response_data["gender"], updated_data["gender"])
        self.assertEqual(response_data["level_of_education"], updated_data["level_of_education"])
        self.assertEqual(response_data["goals"], updated_data["goals"])
        self.assertTrue(response_data["is_active"])

    @ddt_data(
        ("username", "user-not-found"),
        ("email", "user-not-found@mail.com"),
    )
    @unpack
    def test_update_user_in_tenant_user_not_found(self, param: str, value: str) -> None:
        """
        Test updating a user in a tenant that does not exist.

        Open edX definitions tested:
        - `get_edxapp_user`

        Expected result:
        - The status code is 404.
        - The response contains an error message.
        """
        response = self.update_user_in_tenant(self.tenant_x, {param: value})

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response_data)
        self.assertEqual(
            response_data["detail"],
            f"No user found by {{'{param}': '{value}'}} on site {self.tenant_x['domain']}.",
        )


class TestInfoView(BaseAPIIntegrationTest):
    """
    Integration test suite for the info view.
    """

    def setUp(self):
        """
        Set up the test suite.
        """
        self.url = f"{settings['EOX_CORE_API_BASE']}{reverse('eox-info')}"
        super().setUp()

    def test_info_view_success(self) -> None:
        """Test the info view.

        Expected result:
        - The status code is 200.
        - The response contains the version, name and git commit hash.
        """
        response = self.make_request(self.default_site, "GET", url=self.url, with_auth=False)

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("version", response_data)
        self.assertIn("name", response_data)
        self.assertIn("git", response_data)
