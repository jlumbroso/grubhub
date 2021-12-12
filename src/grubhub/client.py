import functools
import itertools
import json
import random
import re
import urllib


import bs4
import user_agent
import requests


GRUBHUB_BASE_URL = "https://www.grubhub.com"

GRUBHUB_API_DOMAIN = "api-gtm.grubhub.com"
GRUBHUB_API_BASE_URL = "https://{}".format(GRUBHUB_API_DOMAIN)
GRUBHUB_API_ENDPOINT_AUTH = "/auth"

GRUBHUB_DEVICE_ID_PAGE = "/eat/static-content-unauth?contentOnly=1"
GRUBHUB_DEVICE_ID_REGEX = "beta_[a-zA-Z0-9]+"


class GrubHubClient:

    _session = None
    _client_id = None
    _device_id = None
    _access_token = None
    _refresh_token = None
    _login_data = None
    _ud_id = None
    _user_agent = None

    @property
    def session(self):
        self._session = self._session or requests.Session()
        return self._session

    def _fetch_client_id(self, session=None):

        # Credit Gregor
        # See: https://stackoverflow.com/a/62861527/408734

        # use instance session unless otherwise specified
        session = session or self.session

        static = urllib.parse.urljoin(
            GRUBHUB_BASE_URL,
            GRUBHUB_DEVICE_ID_PAGE
        )

        soup = bs4.BeautifulSoup(session.get(static).text, "html.parser")

        # NOTE: this heuristic may break and looks for beta_* hash in this static page
        hits = list(set(itertools.chain(*map(
            lambda x: re.findall(
                GRUBHUB_DEVICE_ID_REGEX, x.encode_contents().decode()),
            soup.find_all("script", {"type": "text/javascript"})
        ))))

        if len(hits) == 0:
            return

        if len(hits) > 1:
            raise Exception(
                "unexpected number of clients candidates: {}".format(hits))

        client_id = hits[0]

        return client_id

    @property
    def client_id(self):
        if self._client_id is None:
            self._client_id = self._fetch_client_id()
        return self._client_id

    def _fetch_device_id(self):
        # Credit Gregor
        # See: https://stackoverflow.com/a/62861527/408734

        # Device ID appears to accept any 10-digit value
        device_id = "{}".format(random.randint(10**9, 10**10-1))
        return device_id

    @property
    def device_id(self):
        if self._device_id is None:
            self._device_id = self._fetch_device_id()
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        # Check for valid values
        if (
            (value is None) or
            (type(value) is int and value >= 10**9 and value <= 10**10-1) or
            (type(value) is str and value.isnumeric() and len(value) == 10)
        ):
            self._device_id = "{}".format(value)
        else:
            self._device_id = None

    def _refresh_auth_tokens(self, session=None):

        # use instance session unless otherwise specified
        session = session or self.session

        # define and add a proper header
        headers = {
            "Authority": GRUBHUB_API_DOMAIN,
            "User-Agent": self._user_agent,
            "Authorization": "Bearer",
            "Content-Type": "application/json; charset=UTF-8",
            "Origin": GRUBHUB_BASE_URL,
        }
        session.headers.update(headers)

        data = {
            "brand": "GRUBHUB",
            "client_id": self.client_id,
            "device_id": self.device_id,
            "scope": "anonymous",
        }

        resp = session.post(
            urllib.parse.urljoin(
                GRUBHUB_API_BASE_URL,
                GRUBHUB_API_ENDPOINT_AUTH
            ),
            data=json.dumps(data)
        )

        data = resp.json()
        access_token = data["session_handle"]["access_token"]
        refresh_token = data["session_handle"]["refresh_token"]

        # update header with new token
        session.headers.update({
            "Authorization": "Bearer {}".format(access_token)
        })

        # update instance with new token
        self._access_token = access_token
        self._refresh_token = refresh_token

        return access_token, refresh_token

    @property
    def access_token(self):
        if self._access_token is None:
            self._refresh_auth_token()
        return self._access_token

    def login(self, username, password, session=None):

        logged_in = False

        data_dict = {
            "brand": "GRUBHUB",
            "client_id": self.client_id,
            "device_id": self.device_id,
        }

        if username is not None and password is not None:
            # refresh auth
            self._refresh_auth_tokens()
            data_dict.update({
                "email": username,
                "password": password,
            })
        elif self._refresh_token is not None:
            data_dict.update({
                "refresh_token": self._refresh_token,
            })
        else:
            raise Exception("need credentials")

        # use instance session unless otherwise specified
        session = session or self.session

        try:
            response = session.post(
                url=urllib.parse.urljoin(
                    GRUBHUB_API_BASE_URL,
                    GRUBHUB_API_ENDPOINT_AUTH
                ),
                data=json.dumps(data_dict)
            )
            logged_in = response.ok

        except requests.exceptions.RequestException:
            logged_in = False

        if logged_in:
            data = response.json()

            if username is not None:
                self._login_data = data
                self._ud_id = self._login_data["credential"]["ud_id"]

            self._access_token = data["session_handle"]["access_token"]
            self._refresh_token = data["session_handle"]["refresh_token"]

        return logged_in

    def _refresh_login(self, session=None):

        refreshed = self.login(
            username=None,
            password=None,
            session=session,
        )

        return refreshed

    def _raw_request(self, endpoint, params=None, data=None, session=None):
        # "stats":{"total_results":64,"result_count":20,"page_size":20},
        # "pager":{"total_pages":4,"current_page":1},
        # "results":{ ... },

        # params
        #         {
        #                     "pageNum": "1",
        #                     "pageSize": "20",
        #                     "facet": "orderType:ALL",
        #                     "sorts": "default",
        #                 }

        # use instance session unless otherwise specified
        if session is None:
            assert self._refresh_login()
            session = self.session

        try:
            response = session.get(
                url=urllib.parse.urljoin(
                    GRUBHUB_API_BASE_URL,
                    endpoint
                ),
                params=params,
                headers={
                    "Authorization": "Bearer {}".format(self.access_token),
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip",
                    "User-Agent": self._user_agent,
                }
            )
        except requests.exceptions.RequestException:
            return

        # print(response)
        # print(response.status_code)
        # print(response.content)
        # print(response.headers)

        try:
            json = response.json()
        except:
            json = None

        return response, json

    def request(self, endpoint, params=None, data=None):

        response, json = self._raw_request(
            endpoint=endpoint,
            params=params,
            data=data,
        )

        if "results" in json and "pager" in json:

            results = []
            params = params or dict()

            results += json["results"]
            for page_num in range(2, int(json["pager"]["total_pages"]) + 1):
                params["pageNum"] = page_num
                response, json = self._raw_request(
                    endpoint=endpoint,
                    params=params,
                    data=data,
                )
                results += json["results"]

            return results

        return json

    def order_history(self):
        endpoint = functools.reduce(urllib.parse.urljoin, [
            "/diners/",
            "{}/".format(self._ud_id),
            "search_listing",
        ])

        results = self.request(
            endpoint=endpoint,
            params={
                "pageNum": "1",
                "pageSize": "20",
                "facet": "orderType:ALL",
                "sorts": "default",
            })

        return results

    def __init__(self):
        # draw some persistent user agent for the session
        self._user_agent = user_agent.generate_user_agent()
