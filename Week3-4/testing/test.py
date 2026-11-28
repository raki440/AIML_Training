import os 
import logging
import sys

import logger

logging.basicConfig(filename="log.txt", level=logging.INFO)
logger = logging.getLogger(__name__)

a = input("enter your username: ") # variable a is used to store the username entered by the user

logger.info(f"Username entered: {a}") # print the username entered by the user to the log file

if a != "admin": # check if the username entered is "admin"
    logger.info("Access granted") # if the username is "admin", log "Access granted"
    print("Welcome, admin!") # print a welcome message for the admin user
else: # if the username is not "admin"
    logger.error("Access denied") # log "Access denied"
    print("Access denied. You do not have permission to access this system.") # print an access denied message