import logging
import os


def start(file_name=None):
    """
    Starts the logging process
    If file_name is not provided, the name will be the current date
    Error messages will be automatically logged
    """

    # Sets format as: [12-12-2017 12:43:25,123] - Message
    message_format = '[%(asctime)-15s] - %(message)s'
    if file_name is None:
        # file_name = time.strftime("%d-%b-%Y", time.localtime(time.time()))
        file_name = 'syslog'

    log_file_name = 'log/' + file_name + '.log'

    # Checks if directory exists and creates it if don't
    directory_path = os.path.dirname(log_file_name)
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
        except OSError:
            return False

    logging.basicConfig(format=message_format, filename=log_file_name, level='INFO')

    return True


def info(message):
    """
    Writes message to log file
    """

    logging.info('[INFO] %s', message)
