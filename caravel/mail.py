##########################################################################
# NSAp - Copyright (C) CEA, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
A module to simplify email sending.
"""

# System import
import mimetypes
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailManager:
    """Define a class to simplify emails sending."""

    def __init__(self, smtp_host, smtp_port):
        """Initialize the EmailManager class.

        Parameters
        ----------
        smtp_host: str
            the SMTP host.
        smtp_port: str
            the SMTP port.
        """
        self.host = smtp_host
        self.port = smtp_port

    def send_mail(
        self, to_addrs, subject, body, from_addr="noreply@cea.fr", files=None
    ):
        """Send an email.

        Parameters
        ----------
        to_addrs: list of str
            the destination emails
        subject: str
            the subject of the email.
        body: str
            the body of the email.
        from_addr: str, default 'noreply@cea.fr'
            the sender email.
        files: list of str default None
            a list of files to be attached.
        """
        # Create the container with the email message.
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = ", ".join(to_addrs)
        msg.attach(MIMEText(body, "plain", "utf-8"))
        files = files or []
        for path in files:
            attachment = self._create_attachment(path)
            msg.attach(attachment)

        # Send the email via our own SMTP server.
        with smtplib.SMTP(self.host, self.port) as server:
            server.send_message(msg)

    def _create_attachment(self, path):
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        with open(path, "rb") as fp:
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
        encoders.encode_base64(attachment)
        filename = os.path.basename(path)
        attachment.add_header("Content-Disposition", "attachment", filename=filename)
        return attachment
