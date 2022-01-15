

class CrowlerBaseException(Exception):
    pass


class VideoPageHasNoHLSLinkException(CrowlerBaseException):
    pass


class NoMoreProxiesException(CrowlerBaseException):
    pass
