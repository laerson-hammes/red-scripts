from system import System


class Linux(System):

    @classmethod
    def get_interface(cls, /) -> str:
        raise NotImplementedError

    @classmethod
    def run_sniffer(cls, /) -> None:
        raise NotImplementedError
