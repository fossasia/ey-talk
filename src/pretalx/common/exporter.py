from io import BytesIO
from urllib.parse import quote
from xml.etree import ElementTree as ET

import qrcode
import qrcode.image.svg
from defusedcsv import csv
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.utils.encoding import force_bytes
from base64 import b64encode

from pretalx.common.urls import EventUrls

class BaseExporter:
    """The base class for all data exporters."""

    def __init__(self, event):
        self.event = event

    def __str__(self):
        """The identifier may be used for callbacks and debugging."""
        return self.identifier

    @property
    def verbose_name(self) -> str:
        """A human-readable name for this exporter.

        This should be short but self-explaining. Good examples include
        'JSON' or 'Microsoft Excel'.
        """
        raise NotImplementedError()  # NOQA

    @property
    def identifier(self) -> str:
        """A short and unique identifier for this exporter.

        This should only contain lower-case letters and in most cases
        will be the same as your package name.
        """
        raise NotImplementedError()  # NOQA

    @cached_property
    def quoted_identifier(self) -> str:
        return quote(self.identifier)

    @property
    def public(self) -> bool:
        """Return True if the exported data should be publicly available once
        the event is public, False otherwise."""
        raise NotImplementedError()  # NOQA

    @property
    def cors(self) -> str:
        """If you want to let this exporter be accessed with JavaScript, set
        cors = '*' for all accessing domains, or supply a specific domain."""
        return None

    @property
    def show_qrcode(self) -> bool:
        """Return True if the link to the exporter should be shown as QR code,
        False (default) otherwise.

        Override the get_qr_code method to override the QR code itself.
        """
        return False

    @property
    def icon(self) -> str:
        """Return either a fa- string or some other symbol to accompany the
        exporter in displays."""
        raise NotImplementedError()  # NOQA

    @property
    def group(self) -> str:
        """Return either 'speaker' or 'submission' to indicate on which
        organiser export page to list this export.

        Invalid values default to 'submission', which is also where all
        schedule exports live.
        """
        return "submission"

    def render(self, **kwargs) -> tuple[str, str, str]:
        """Render the exported file and return a tuple consisting of a file
        name, a file type and file content."""
        raise NotImplementedError()  # NOQA

    class urls(EventUrls):
        """The base attribute of this class contains the relative URL where
        this exporter's data will be found, e.g. /event/schedule/export/my-
        export.ext Use ``exporter.urls.base.full()`` for the complete URL,
        taking into account the configured event URL, or HTML export URL."""

        base = "{self.event.urls.export}{self.quoted_identifier}"

    def get_qrcode(self):
        """Generate and return a QR code for the exporter's URL."""
        qr_url = self.urls.base.full()  # Retrieve the full URL
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_url)
        qr.make(fit=True)
        image = qr.make_image(fill='black', back_color='white')

        output = BytesIO()
        image.save(output, format='PNG')
        img_base64 = b64encode(output.getvalue()).decode('utf-8')
        return mark_safe(f'<img src="data:image/png;base64,{img_base64}" alt="QR Code">')

class CSVExporterMixin:
    def render(self, **kwargs):
        fieldnames, data = self.get_data()
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        content = output.getvalue()
        return self.filename, "text/plain", content
