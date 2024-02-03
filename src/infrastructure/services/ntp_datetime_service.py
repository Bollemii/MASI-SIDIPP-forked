import datetime
import ntplib

from src.application.interfaces.idatetime_service import IDatetimeService


class NtpDatetimeService(IDatetimeService):
    """Datetime service that uses NTP server"""

    def __init__(self, ntp_server: str = "pool.ntp.org"):
        self.ntp_server = ntp_server
        self.client = ntplib.NTPClient()

    def get_datetime(self) -> datetime.datetime:
        try:
            response = self.client.request(self.ntp_server)
            return datetime.datetime.fromtimestamp(response.tx_time, datetime.UTC)
        except Exception:
            return datetime.datetime.fromisoformat("1970-01-01T00:00:01+00:00")
