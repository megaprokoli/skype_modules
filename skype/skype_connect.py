import time
import logging
import threading
from skpy import Skype
from skpy import SkypeAuthException
from skype import input_handler as inp_handler


class SkypeConnector:
    instance = None
    hour_10 = 36000.0       # 10h in sec

    def __init__(self, user_name, password):
        self.user = user_name
        self.pwd = password
        self.token_file = ".tokens-web"
        self.skype = Skype(connect=False)
        self.connection = self.skype.conn
        self.input_handler = None
        self.start_time = .0
        self.logger = logging.getLogger("SkyModules")

        self.connection.setTokenFile(self.token_file)

    @staticmethod
    def get_instance():
        return SkypeConnector.instance

    def reconnect(self):
        self.skype.conn.setUserPwd(self.user, self.pwd)
        self.skype.conn.getSkypeToken()
        self.start_time = time.time()
        self.logger.debug("new token requested")

    def connect(self):

        try:
            self.skype.conn.readToken()
            self.start_time = time.time()
            self.logger.debug("token reused")
        except SkypeAuthException:
            self.reconnect()

        self.input_handler = inp_handler.InputHandler(tokenFile=self.token_file, autoAck=True)

        self.logger.debug("starttime: " + str(self.start_time))
        self.logger.info("connected")

    def refresh_token(self):
        while True:
            if time.time() >= self.start_time + self.hour_10:
                self.reconnect()

    def run(self):
        if self.connection.connected:

            tr = threading.Thread(target=self.refresh_token)
            tr.start()

            self.input_handler.loop()
