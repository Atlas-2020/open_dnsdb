# -*- coding: utf-8 -*-

from __future__ import print_function
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from oslo_config import cfg

from ..library.log import getLogger

log = getLogger(__name__)

CONF = cfg.CONF


def send_email(subject, content, sender=None, receivers=None):
    s = smtplib.SMTP()
    msg = ''
    try:
        if content is None:
            content = ""
        msg = MIMEText(content, 'plain', 'utf-8')
        if sender is None:
            sender = CONF.MAIL.from_addr
        elif not isinstance(sender, str):
            raise TypeError('sender should be str type.')
        if receivers is None:
            receivers = CONF.MAIL.info_list
        elif not isinstance(receivers, str):
            raise TypeError('Receivers should be str type.')
        to_list = receivers.split(';')

        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = Header(sender, 'utf-8')
        msg['To'] = Header(receivers, 'utf-8')
        s = smtplib.SMTP()
        s.connect(CONF.MAIL.server, CONF.MAIL.port)
        s.sendmail(sender, to_list, msg.as_string())
    except Exception as e:
        log.error("Failed to send email:%s, because: %s" % (msg, e))
    finally:
        s.close()


def send_alert_email(content, sender=None):
    receivers = CONF.MAIL.alert_list
    subject = "[DNSDB alarm]"
    send_email(subject, content, sender, receivers)

