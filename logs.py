import logging

# Create and configure logger
logging.basicConfig(filename="user.log", format='%(asctime)s %(lineno)d %(message)s', filemode='a')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)
