import logging
class Logit(object):
    def __init__(self, module_name):
        self.logger = logging.getLogger(module_name)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)

    def info(self, msg):
        self.logger.info(msg)
