import logging, hmac, time

class Handshake:
    def __init__(self, config):
        self.loungeACL = config["ACL"]
        self.pretzel = config["SETTINGS"]["pretzel"]
        self.serverAddr = config["SETTINGS"]["serverAddr"]
        self.window = config["SETTINGS"]["HMACWindow"]
        self.logger = logging.getLogger("Handshake")

    def send(self, netID, user):
        self.createLink(netID, user)

    def createLink(self, netID, user):
        validFrom = time.time()
        message = netID+user+str(validFrom)
        userHMAC = hmac.new(str(self.pretzel), message).hexdigest()
        url = "http://{0}/ums/provision/{1}/{2}/{3}/{4}/".format(self.serverAddr, netID, user, userHMAC, validFrom)
        self.logger.debug("Composed %s's URL: %s", netID, url)

    def verify(self, netID, user, userHMAC, linkTime):
        if time.time()-float(linkTime) < self.window:

            validFrom = linkTime
            message = netID+user+str(validFrom)
            validHMAC = unicode(hmac.new(str(self.pretzel), message).hexdigest())
            self.logger.debug("valid: %s", validHMAC)
            self.logger.debug("user: %s", userHMAC)
            if hmac.compare_digest(userHMAC, validHMAC):
                self.logger.debug("HMAC from %s valid", netID)
                return True
            else:
                self.logger.warning("HMAC from %s INVALID", netID)
                return False
        else:
            self.logger.warning("%s used an outdated link", netID)
            return False

    def sendMail(self, link, netID):
        pass
