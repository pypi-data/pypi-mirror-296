#!/usr/bin/env python

import logging
from set_timestamp import set_timestamp, now

########################################################################################################################


class AppReg(object):
    def __init__(self, results):
        self.results = results
        self.items = []
        self.date_format = "%Y-%m-%dT%H:%M:%S"

    def parse_credentials(self, items, app_id, app_display_name, record_type):
        for item in items:
            ts = None
            age = "-"
            display_name = item.get("displayName")
            if not display_name:
                display_name = "No description"

            key_id = item.get("keyId")
            start_date_time = item.get("startDateTime")
            end_date_time = item.get("endDateTime")
            if end_date_time:
                ts = set_timestamp(end_date_time[:19], date_format=self.date_format)
            if ts:
                age = (now() - ts).days

            if isinstance(age, int) and age > 0:
                comment = f"Expired {abs(age)} days ago."
            elif isinstance(age, int) and age < 0:
                comment = f"Will expire in {abs(age)} days."
            elif isinstance(age, int) and age == 0:
                comment = f"Will expire today."
            else:
                comment = ""

            d = {
                "appId": app_id,
                "displayName": app_display_name,
                "recordDisplayName": display_name,
                "comment": comment,
                "type": record_type,
                "startDateTime": start_date_time[:19],
                "endDateTime": end_date_time[:19]
            }

            self.items.append(d)

    def parse_results(self):
        if not isinstance(self.results, list):
            logging.error(f"The provided results must be a list.")
            return

        for result in self.results:
            app_id = result.get("appId")
            display_name = result.get("displayName")
            key_credentials = result.get("keyCredentials")
            password_credentials = result.get("passwordCredentials")

            if key_credentials:
                self.parse_credentials(key_credentials, app_id, display_name, "Certificate")

            if password_credentials:
                self.parse_credentials(password_credentials, app_id, display_name, "Client secret")

    def get_items_sorted(self):
        return sorted(self.items, key=lambda x: x.get('endDateTime'), reverse=False)

    def get_items(self):
        return self.items

