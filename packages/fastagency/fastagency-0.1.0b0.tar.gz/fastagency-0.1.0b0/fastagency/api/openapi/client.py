import importlib
import inspect
import re
import shutil
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from types import ModuleType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Literal,
    Optional,
)

import requests
from fastapi_code_generator.__main__ import generate_code

from .fastapi_code_generator_helpers import patch_get_parameter_type
from .security import BaseSecurity, BaseSecurityParameters

if TYPE_CHECKING:
    from autogen.agentchat import ConversableAgent

__all__ = ["OpenAPI"]


@contextmanager
def add_to_globals(new_globals: dict[str, Any]) -> Iterator[None]:
    old_globals: dict[str, Any] = {}
    try:
        for key, value in new_globals.items():
            if key in globals():
                old_globals[key] = globals()[key]
            globals()[key] = value
        yield
    finally:
        for key, value in old_globals.items():
            globals()[key] = value


class OpenAPI:
    def __init__(
        self, servers: list[dict[str, Any]], title: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Proxy class to generate client from OpenAPI schema."""
        self.servers = servers
        self.title = title
        self.kwargs = kwargs
        self.registered_funcs: list[Callable[..., Any]] = []
        self.globals: dict[str, Any] = {}

        self.security: dict[str, BaseSecurity] = {}
        self.security_params: dict[Optional[str], BaseSecurityParameters] = {}

    @staticmethod
    def _get_params(
        path: str, func: Callable[..., Any]
    ) -> tuple[set[str], set[str], Optional[str], bool]:
        sig = inspect.signature(func)

        params_names = set(sig.parameters.keys())

        path_params = set(re.findall(r"\{(.+?)\}", path))
        if not path_params.issubset(params_names):
            raise ValueError(f"Path params {path_params} not in {params_names}")

        body = "body" if "body" in params_names else None

        security = "security" in params_names

        q_params = set(params_names) - path_params - {body} - {"security"}

        return q_params, path_params, body, security

    def _process_params(
        self, path: str, func: Callable[[Any], Any], **kwargs: Any
    ) -> tuple[str, dict[str, Any], dict[str, Any]]:
        q_params, path_params, body, security = OpenAPI._get_params(path, func)

        expanded_path = path.format(**{p: kwargs[p] for p in path_params})

        url = self.servers[0]["url"] + expanded_path

        body_dict = (
            {
                "json": kwargs[body].model_dump()
                if hasattr(kwargs[body], "model_dump")
                else kwargs[body].dict()
            }
            if body and body in kwargs
            else {}
        )
        body_dict["headers"] = {"Content-Type": "application/json"}
        if security:
            q_params, body_dict = kwargs["security"].add_security(q_params, body_dict)
            # body_dict["headers"][security] = kwargs["security"]

        params = {k: v for k, v in kwargs.items() if k in q_params}

        return url, params, body_dict

    def set_security_params(
        self, security_params: BaseSecurityParameters, name: Optional[str] = None
    ) -> None:
        if name is not None:
            security = self.security.get(name)
            if security is None:
                raise ValueError(f"Security is not set for '{name}'")

            if not security.accept(security_params):
                raise ValueError(
                    f"Security parameters {security_params} do not match security {security}"
                )

        self.security_params[name] = security_params

    def _get_security_params(self, name: str) -> Optional[BaseSecurityParameters]:
        # check if security is set for the method
        security = self.security.get(name)
        if security is None:
            return None

        security_params = self.security_params.get(name)
        if security_params is None:
            # check if default security parameters are set
            security_params = self.security_params.get(None)
            if security_params is None:
                raise ValueError(
                    f"Security parameters are not set for {name} and there are no default security parameters"
                )

        # check if security matches security parameters
        if not security.accept(security_params):
            raise ValueError(
                f"Security parameters {security_params} do not match security {security}"
            )

        return security_params

    def _request(
        self,
        method: Literal["put", "get", "post", "delete"],
        path: str,
        description: Optional[str] = None,
        security: Optional[BaseSecurity] = None,
        **kwargs: Any,
    ) -> Callable[..., dict[str, Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., dict[str, Any]]:
            name = func.__name__

            if security is not None:
                self.security[name] = security

            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> dict[str, Any]:
                url, params, body_dict = self._process_params(path, func, **kwargs)

                security = self.security.get(name)
                if security is not None:
                    security_params = self._get_security_params(name)
                    if security_params is None:
                        raise ValueError(
                            f"Security parameters are not set for '{name}'"
                        )
                    else:
                        security_params.apply(params, body_dict, security)

                response = getattr(requests, method)(url, params=params, **body_dict)
                return response.json()  # type: ignore [no-any-return]

            wrapper._description = (  # type: ignore [attr-defined]
                description or func.__doc__.strip()
                if func.__doc__ is not None
                else None
            )

            self.registered_funcs.append(wrapper)

            return wrapper

        return decorator  # type: ignore [return-value]

    def put(self, path: str, **kwargs: Any) -> Callable[..., dict[str, Any]]:
        return self._request("put", path, **kwargs)

    def get(self, path: str, **kwargs: Any) -> Callable[..., dict[str, Any]]:
        return self._request("get", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Callable[..., dict[str, Any]]:
        return self._request("post", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Callable[..., dict[str, Any]]:
        return self._request("delete", path, **kwargs)

    @classmethod
    def _get_template_dir(cls) -> Path:
        path = Path(__file__).parents[3] / "templates"
        if not path.exists():
            raise RuntimeError(f"Template directory {path.resolve()} not found.")
        return path

    @classmethod
    def generate_code(
        cls,
        input_text: str,
        output_dir: Path,
        disable_timestamp: bool = False,
        custom_visitors: Optional[list[Path]] = None,
    ) -> str:
        if custom_visitors is None:
            custom_visitors = []
        custom_visitors.append(Path(__file__).parent / "security_schema_visitor.py")

        with patch_get_parameter_type():
            generate_code(
                input_name="openapi.json",
                input_text=input_text,
                encoding="utf-8",
                output_dir=output_dir,
                template_dir=cls._get_template_dir(),
                disable_timestamp=disable_timestamp,
                custom_visitors=custom_visitors,
            )
            # Use unique file name for main.py
            main_name = f"main_{output_dir.name}"
            main_path = output_dir / f"{main_name}.py"
            shutil.move(output_dir / "main.py", main_path)

            # Change "from models import" to "from models_unique_name import"
            with open(main_path) as f:  # noqa: PTH123
                main_py_code = f.read()
            main_py_code = main_py_code.replace(
                "from .models import", f"from models_{output_dir.name} import"
            )
            with open(main_path, "w") as f:  # noqa: PTH123
                f.write(main_py_code)

            # Use unique file name for models.py
            models_name = f"models_{output_dir.name}"
            models_path = output_dir / f"{models_name}.py"
            shutil.move(output_dir / "models.py", models_path)

            return main_name

    def set_globals(self, main: ModuleType, suffix: str) -> None:
        xs = {k: v for k, v in main.__dict__.items() if not k.startswith("__")}
        self.globals = {
            k: v
            for k, v in xs.items()
            if hasattr(v, "__module__")
            and v.__module__ in [f"models_{suffix}", "typing"]
        }

    @classmethod
    def create(
        cls, openapi_json: Optional[str] = None, openapi_url: Optional[str] = None
    ) -> "OpenAPI":
        if openapi_json is None and openapi_url is None:
            raise ValueError("Either openapi_json or openapi_url should be provided")

        if openapi_json is None and openapi_url is not None:
            with requests.get(openapi_url, timeout=10) as response:
                response.raise_for_status()
                openapi_json = response.text

        with tempfile.TemporaryDirectory() as temp_dir:
            td = Path(temp_dir)
            suffix = td.name

            main_name = cls.generate_code(
                input_text=openapi_json,  # type: ignore [arg-type]
                output_dir=td,
            )
            # add td to sys.path
            try:
                sys.path.append(str(td))
                main = importlib.import_module(main_name, package=td.name)  # nosemgrep
            finally:
                sys.path.remove(str(td))

            client: OpenAPI = main.app  # type: ignore [attr-defined]
            client.set_globals(main, suffix=suffix)

            return client

    def register_for_llm(self, agent: "ConversableAgent") -> None:
        with add_to_globals(self.globals):
            for f in self.registered_funcs:
                agent.register_for_llm()(f)

    def register_for_execution(self, agent: "ConversableAgent") -> None:
        for f in self.registered_funcs:
            agent.register_for_execution()(f)
