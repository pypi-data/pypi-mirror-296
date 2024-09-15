"""Client for API V2.

See https://github.com/actigraph/CentrePoint3APIDocumentation.
"""

import logging
from collections import defaultdict
from typing import Any, Dict, List, Literal, Optional, Union

import requests

from actiapi import ActiGraphClient

tokens: defaultdict[str, Optional[str]] = defaultdict(lambda: None)
session = requests.Session()

logger = logging.getLogger(__name__)


class ActiGraphClientV3(ActiGraphClient):
    """Client for CentrePoint V3 API."""

    BASE_URL = "https://api.actigraphcorp.com"
    AUTH_API = "https://auth.actigraphcorp.com/connect/token"

    @staticmethod
    def _generate_headers(token: str, raw: bool = False):
        headers = {}
        if not raw:
            headers["Accept"] = "application/json"
            headers["Content-Type"] = "application/json"
        headers["Authorization"] = f"Bearer {token}"
        return headers

    def _get_access_token(self, scope: str):
        endpoint = self.AUTH_API
        request_body = {
            "client_id": self.api_access_key,
            "client_secret": self.api_secret_key,
            "scope": scope,
            "grant_type": "client_credentials",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(
            endpoint, data=request_body, headers=headers, verify=True
        )
        try:
            return response.json()["access_token"]
        except KeyError:
            raise RuntimeError(
                "No access token! Make sure you have API_ACCESS_KEY and API_SECRET_KEY!"
            )

    def get_files(
        self,
        user: Union[int, str],
        study_id: int,
        start: Optional[str] = None,
        end: Optional[str] = None,
        data_format: Literal["avro", "csv"] = "avro",
        sensor: Literal[
            "raw-accelerometer",
            "temperature",
            "ppg-green",
            "ppg-green-100-hz",
            "barometer",
            "imu",
            "ppg-red-ir-50-hz",
        ] = "raw-accelerometer",
    ) -> List[str]:
        """Return download URLs to raw AVRO files.

        Parameters
        ----------
        user:
            User id
        study_id:
            Id of the study
        start:
            Start timestamp string in ISO8601 format
        end:
            End timestamp string in ISO8601 format
        data_format:
            Raw data file format; avro (default) or csv.
        sensor:
            Type of raw data (raw-accelerometer, ppg-green or temperature), defaults to
            raw-accelerometer
        """
        assert data_format in ("avro", "csv")

        request_string = (
            f"/dataaccess/v3/files/studies/{study_id}/subjects/{user}"
            f"/{sensor}?fileFormat={data_format}"
        )
        if start is not None:
            request_string += f"&startDate={start}"
        if end is not None:
            request_string += f"&endDate={end}"
        request_string += "&"
        results = self._get_paginated(
            request_string,
            scope="DataAccess",
        )

        results = [x["downloadUrl"] for x in results]

        return results

    def get_study_info(self, study_id) -> List[Dict[str, Any]]:
        """Save high-level study info to file.

        Parameters
        ----------
        study_id:
            Id of the study
        """
        results = self._get_single(
            f"/centrepoint/v3/Studies/{study_id}", scope="CentrePoint"
        )
        return results

    def get_studies(self) -> List[Dict[str, Any]]:
        """Save high-level study info to file.

        Parameters
        ----------
        study_id:
            Id of the study
        """
        results = self._get_paginated("/centrepoint/v3/Studies?", scope="CentrePoint")
        return results

    def get_study_metadata(self, study_id) -> List[Dict[str, Any]]:
        """Save all study metadata to file.

        Parameters
        ----------
        study_id:
            Id of the study
        """
        results = self._get_paginated(
            f"/centrepoint/v3/Studies/{study_id}/Subjects?", scope="CentrePoint"
        )
        return results

    def get_event_markers(self, user: Union[int, str], study_id: int) -> List[str]:
        """Return event marker data.

        Parameters
        ----------
        user:
            User id
        study_id:
            Id of the study
        """
        results = self._get_paginated(
            f"/analytics/v3/Studies/{study_id}/Subjects/{user}/EventMarkers?",
            scope="Analytics",
        )

        return results

    def get_minute_summary(
        self, user: Union[int, str], study_id: int
    ) -> List[Dict[str, Any]]:
        """Return minute level data.

        Parameters
        ----------
        user:
            User id
        study_id:
            Id of the study
        """
        results = self._get_paginated(
            f"/analytics/v3/Studies/{study_id}/Subjects/{user}/MinuteSummaries?",
            scope="Analytics",
        )

        return results

    def get_daily_summary(
        self, user: Union[int, str], study_id: int
    ) -> List[Dict[str, Any]]:
        """Return daily summary data.

        Parameters
        ----------
        user:
            User id
        study_id:
            Id of the study
        """
        results = self._get_paginated(
            f"/analytics/v3/Studies/{study_id}/Subjects/{user}/DailyStatistics?",
            scope="Analytics",
        )

        return results

    def get_sleep_summary(
        self, user: Union[int, str], study_id: int
    ) -> List[Dict[str, Any]]:
        """Return Dustin-Tracy sleep summary data.

        Parameters
        ----------
        user:
            User id
        study_id:
            Id of the study
        """
        results = self._get_paginated(
            f"/analytics/v3/Studies/{study_id}/Subjects/"
            f"{user}/DustinTracySleepPeriods?",
            scope="Analytics",
        )

        return results

    def _get_single(self, request: str, scope: str):
        global tokens
        if tokens[scope] is None:
            tokens[scope] = self._get_access_token(scope)
        logger.info("Requesting %s", request)
        headers = self._generate_headers(str(tokens[scope]))
        response = session.get(self.BASE_URL + request, headers=headers, stream=False)
        reply = validate_response(response)
        return reply

    def _get_paginated(self, request: str, scope: str):
        global tokens
        results = []
        offset = 0
        limit = 100
        while True:
            paginated_request = f"{request}offset={offset}&limit={limit}"
            try:
                reply = self._get_single(request=paginated_request, scope=scope)
                if reply is None:
                    break

                total_count = reply["totalCount"]
            except KeyError:
                tokens[scope] = None
                reply = self._get_single(request=paginated_request, scope=scope)
                if reply is None:
                    break

                total_count = reply["totalCount"]

            for item in reply["items"]:
                results.append(item)
            if offset + limit >= total_count:
                break
            offset += limit
        if len(results) == 0:
            logger.error("No data found for request: %s", request)
            return []
        return results


def validate_response(response):
    """Check response status."""
    if response.status_code == 404:
        logger.error("404 Not Found!")
        result = None
    else:
        result = response.json()
    return result
