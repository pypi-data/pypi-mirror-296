from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request
from fastapi.responses import Response
from pydenticore import IdentityErrorDescriber
from pydenticore.authentication import AuthenticationSchemeProvider
from pydenticore.authentication.interfaces import IAuthenticationSchemeProvider
from pydenticore.authorization import AuthorizationHandlerContext
from pydenticore.http.context import IHttpContextAccessor, HttpContext as _HttpContext
from pydenticore.interfaces import IPasswordValidator, IUserValidator, IRoleValidator
from pydenticore.security.claims import ClaimsPrincipal

from fastapi_pydentity.infrastructure import CollectionDependency


class HttpContext(_HttpContext):
    def __init__(
            self,
            request: Request,
            response: Response,
            schemes: Annotated[IAuthenticationSchemeProvider, Depends(AuthenticationSchemeProvider)]
    ):
        super().__init__(request, response, schemes)

    def _getuser(self) -> ClaimsPrincipal | None:
        return self.request.user

    def _setuser(self, value: ClaimsPrincipal | None) -> None:
        self.request.scope["user"] = value


class HttpContextAccessor(IHttpContextAccessor):
    def __init__(self, context: Annotated[HttpContext, Depends()]):
        super().__init__(context)


class FastAPIAuthorizationHandlerContext(AuthorizationHandlerContext):
    def __init__(self, request: Request):
        super().__init__(request)


class PasswordValidatorCollection(CollectionDependency[IPasswordValidator]):
    def __call__(self, errors: Annotated[IdentityErrorDescriber, Depends()]):
        self.kwargs.update({"errors": errors})
        return self


class UserValidatorCollection(CollectionDependency[IUserValidator]):
    def __call__(self, errors: Annotated[IdentityErrorDescriber, Depends()]):
        self.kwargs.update({"errors": errors})
        return self


class RoleValidatorCollection(CollectionDependency[IRoleValidator]):
    def __call__(self, errors: Annotated[IdentityErrorDescriber, Depends()]):
        self.kwargs.update({"errors": errors})
        return self
