#!/usr/bin/env python
import smtplib
import argparse
import doctest
from email.mime.text import MIMEText

def send_mail(filename, sender, *recipients):
    """ Send an email with the current CSV to someone.
        >>> filename = 'mailer.py'
        >>> recipients = ['noreply@denverpost.com']
        >>> send_mail(filename, *recipients)

        """
    fp = open(filename, 'rb')
    msg = MIMEText(fp.read())
    fp.close()

    msg['Subject'] = 'New Wildfire Perimeter Map:'
    msg['From'] = sender
    msg['To'] = recipients[0]

    s = smtplib.SMTP('localhost')
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='', description='Email people when there is a change in the file.',
                                     epilog='')
    parser.add_argument('-s', '--state', dest='state', action='store',
                        default='all',
                        help='a two-letter abbreviation for the state we want to process, i.e. CO CA AZ etc.')
    parser.add_argument('--sender', dest='sender', action='store',
                        help='The "From" field in the email being sent')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument("recipients", action="append", nargs="*")
    args = parser.parse_args()

    if args.verbose:
        doctest.testmod(verbose=args.verbose)

    filename = '%s-fires.csv' % args.state
    send_mail(filename, args.sender, *args.recipients[0])
