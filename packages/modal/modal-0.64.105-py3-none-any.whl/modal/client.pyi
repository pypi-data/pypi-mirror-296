import asyncio.locks
import grpclib.exceptions
import modal_proto.modal_api_grpc
import synchronicity.combined_types
import typing
import typing_extensions

def _get_metadata(
    client_type: int, credentials: typing.Optional[typing.Tuple[str, str]], version: str
) -> typing.Dict[str, str]: ...
async def _http_check(url: str, timeout: float) -> str: ...
async def _grpc_exc_string(
    exc: grpclib.exceptions.GRPCError, method_name: str, server_url: str, timeout: float
) -> str: ...

class _Client:
    _client_from_env: typing.ClassVar[typing.Optional[_Client]]
    _client_from_env_lock: typing.ClassVar[typing.Optional[asyncio.locks.Lock]]

    def __init__(
        self,
        server_url: str,
        client_type: int,
        credentials: typing.Optional[typing.Tuple[str, str]],
        version: str = "0.64.105",
    ): ...
    @property
    def stub(self) -> modal_proto.modal_api_grpc.ModalClientModal: ...
    @property
    def authenticated(self) -> bool: ...
    @property
    def credentials(self) -> tuple: ...
    async def _open(self): ...
    async def _close(self, prep_for_restore: bool = False): ...
    def set_pre_stop(self, pre_stop: typing.Callable[[], typing.Awaitable[None]]): ...
    async def _init(self): ...
    async def __aenter__(self): ...
    async def __aexit__(self, exc_type, exc, tb): ...
    @classmethod
    def anonymous(cls, server_url: str) -> typing.AsyncContextManager[_Client]: ...
    @classmethod
    async def from_env(cls, _override_config=None) -> _Client: ...
    @classmethod
    async def from_credentials(cls, token_id: str, token_secret: str) -> _Client: ...
    @classmethod
    async def verify(cls, server_url: str, credentials: typing.Tuple[str, str]) -> None: ...
    @classmethod
    def set_env_client(cls, client: typing.Optional[_Client]): ...

class Client:
    _client_from_env: typing.ClassVar[typing.Optional[Client]]
    _client_from_env_lock: typing.ClassVar[typing.Optional[asyncio.locks.Lock]]

    def __init__(
        self,
        server_url: str,
        client_type: int,
        credentials: typing.Optional[typing.Tuple[str, str]],
        version: str = "0.64.105",
    ): ...
    @property
    def stub(self) -> modal_proto.modal_api_grpc.ModalClientModal: ...
    @property
    def authenticated(self) -> bool: ...
    @property
    def credentials(self) -> tuple: ...

    class ___open_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self, *args, **kwargs): ...

    _open: ___open_spec

    class ___close_spec(typing_extensions.Protocol):
        def __call__(self, prep_for_restore: bool = False): ...
        async def aio(self, *args, **kwargs): ...

    _close: ___close_spec

    class __set_pre_stop_spec(typing_extensions.Protocol):
        def __call__(self, pre_stop: typing.Callable[[], None]): ...
        def aio(self, pre_stop: typing.Callable[[], typing.Awaitable[None]]): ...

    set_pre_stop: __set_pre_stop_spec

    class ___init_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self, *args, **kwargs): ...

    _init: ___init_spec

    def __enter__(self): ...
    async def __aenter__(self, *args, **kwargs): ...
    def __exit__(self, exc_type, exc, tb): ...
    async def __aexit__(self, *args, **kwargs): ...
    @classmethod
    def anonymous(cls, server_url: str) -> synchronicity.combined_types.AsyncAndBlockingContextManager[Client]: ...
    @classmethod
    def from_env(cls, _override_config=None) -> Client: ...
    @classmethod
    def from_credentials(cls, token_id: str, token_secret: str) -> Client: ...
    @classmethod
    def verify(cls, server_url: str, credentials: typing.Tuple[str, str]) -> None: ...
    @classmethod
    def set_env_client(cls, client: typing.Optional[Client]): ...

HEARTBEAT_INTERVAL: float

HEARTBEAT_TIMEOUT: float

CLIENT_CREATE_ATTEMPT_TIMEOUT: float

CLIENT_CREATE_TOTAL_TIMEOUT: float
