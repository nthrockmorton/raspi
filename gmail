#!/usr/bin/env python

import RPi.GPIO as GPIO, imaplib, time

DEBUG = 1

USERNAME = "xxx"     # just the part before the @ sign, add yours here
PASSWORD = "xxx"

NEWMAIL_OFFSET = 1        # my unread messages never goes to zero, yours might
MAIL_CHECK_FREQ = 15      # check mail every 60 seconds

GPIO.setmode(GPIO.BOARD)
GREEN_LED = 13
RED_LED = 11
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

M = imaplib.IMAP4_SSL('imap.gmail.com','993')
sessionValid = True

try:
    M.login(USERNAME, PASSWORD)
    print "LOGIN SUCCESS"

except imaplib.IMAP4.error,e:
    print str(e)
    print "LOGIN FAILED!!! "
    sessionValid = False

while sessionValid:

        M.select()

        newmails = len(M.search(None, 'UnSeen')[1][0].split())  # from http://stackoverflow.com/a/3984850 

        if newmails > 0:
                GPIO.output(GREEN_LED, True)
                GPIO.output(RED_LED, False)
        else:
                GPIO.output(GREEN_LED, False)
                GPIO.output(RED_LED, True)

        time.sleep(MAIL_CHECK_FREQ)
