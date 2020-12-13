#!/usr/bin/python
# coding=utf-8

from optparse import OptionParser
import smtplib
import logging
import csv
import sys

log_config = {'level': logging.INFO, 'format': '%(asctime)s %(filename)s:%(lineno)-2d %(levelname)-5s - %(message)s'}

parser = OptionParser()
parser.add_option("-v", dest="verbose", action="store_true", default=False,
                  help="Turns on verbose mode, default is off")
parser.add_option("-t", dest="tls", action="store_true", default=False,
                  help="Turns on TLS/SSL mode, default is off")
parser.add_option("-s", dest="smtp_server", help="SMTP server with port, colon delimited")
parser.add_option("-a", dest="smtp_auth", help="SMTP auth user and password, colon delimited")
parser.add_option("-f", dest="mail_from", help="Sender address, for example, \"John Smith <john@smith.com>\"")
(opt, arg) = parser.parse_args()

if opt.verbose:
    log_config["level"] = logging.DEBUG
logging.basicConfig(**log_config)

logging.info("Options: %s" % opt)

(smtp_server, port) = opt.smtp_server.split(":")
(smtp_user, smtp_password) = opt.smtp_auth.split(":")

lines = 0
sent = 0
server = None

try:
    if opt.tls:
        server = smtplib.SMTP_SSL(smtp_server, port)
    else:
        server = smtplib.SMTP(smtp_server, port)

    server.login(smtp_user, smtp_password)

    for email, subject, message in csv.reader(iter(sys.stdin.readline, ''), delimiter=';'):
        lines = lines + 1
        logging.debug("%d: Email = %s, subhect = %s, message = %s" % (lines, email, subject, message))
        try:
            server.sendmail(opt.mail_from, email, message)
            sent = sent + 1
        except smtplib.SMTPException as e:
            logging.error(e)

except Exception as e:
    logging.error(e)

finally:
    if server:
        server.quit()

logging.info("Lines parsed: %d, emails sent: %d" % (lines, sent))
