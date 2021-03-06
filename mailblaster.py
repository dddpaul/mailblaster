#!/usr/bin/env python3
# coding=utf-8
import csv
import logging
import smtplib
import sys
import argparse
from email.header import Header
from string import Template

parser = argparse.ArgumentParser()
parser.add_argument("--server", dest="smtp_server", required=True, help="SMTP server with port, colon delimited (required)")
parser.add_argument("--auth", dest="smtp_auth", help="SMTP auth user and password, colon delimited")
parser.add_argument("--from", dest="mail_from", required=True, help="Sender address e.g. \"John Smith <john@smith.com>\" (required)")
parser.add_argument("--subject", required=True, help="Message subject (required)")
parser.add_argument("--template", required=True, help="Message template filename (required)")
parser.add_argument("--delimiter", default=",", help="CSV delimiter, default is \",\"")
parser.add_argument("--ssl", action="store_true", default=False, help="Turns on TLS/SSL mode, default is off")
parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Turns on verbose mode, default is off")
opt = parser.parse_args()

log_config = {'level': logging.INFO, 'format': '%(asctime)s %(filename)s:%(lineno)-2d %(levelname)-5s - %(message)s'}
if opt.verbose:
    log_config["level"] = logging.DEBUG
logging.basicConfig(**log_config)
logging.info(f"Options: {opt}")

(smtp_server, port) = opt.smtp_server.split(":")
server = None
lines = 0
sent = 0
failed = 0

try:
    if opt.ssl:
        server = smtplib.SMTP_SSL(smtp_server, port)
    else:
        server = smtplib.SMTP(smtp_server, port)

    if opt.smtp_auth:
        (smtp_user, smtp_password) = opt.smtp_auth.split(":")
        server.login(smtp_user, smtp_password)

    with open(opt.template, "r") as f:
        template = f.read()

    for mail_to, placeholder1 in csv.reader(iter(sys.stdin.readline, ''), delimiter=opt.delimiter):
        lines += 1
        logging.debug(f"{lines}: Mail to = {mail_to}, subject = {opt.subject}, placeholder1 = {placeholder1}")

        headers = {
            "Content-Type": "text/plain; charset=utf-8",
            "Content-Disposition": "inline",
            "Content-Transfer-Encoding": "8bit",
            "From": opt.mail_from,
            "To": mail_to,
            "Subject": Header(opt.subject, 'utf-8').encode()
        }

        message = ""
        for key, value in headers.items():
            message += f"{key}: {value}\n"

        content = Template(template).substitute(placeholder1=placeholder1)
        message += f"\n{content}\n"

        try:
            server.sendmail(opt.mail_from, mail_to, message.encode("utf8"))
            sent += 1
        except smtplib.SMTPException as e:
            logging.error(e)
            failed += 1

except Exception as e:
    logging.error(e)

finally:
    if server:
        server.quit()

logging.info(f"Lines parsed: {lines}, messages sent: {sent}, messages failed: {failed}")
