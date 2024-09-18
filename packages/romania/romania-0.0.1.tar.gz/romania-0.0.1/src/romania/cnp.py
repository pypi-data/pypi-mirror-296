class CNP:
    def __init__(self, value: str) -> None:
        self.value = value
    
    @property
    def year(self) -> int:
        raise NotImplementedError


class CNPException(Exception):
    pass
