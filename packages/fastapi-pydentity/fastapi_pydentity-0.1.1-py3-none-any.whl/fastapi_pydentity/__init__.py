import inspect
from collections.abc import Iterable, Callable
from typing import get_origin, Annotated, get_args, Union, Generic

from fastapi import Depends
from pydenticore import (
    DefaultUserConfirmation,
    IdentityConstants,
    IdentityErrorDescriber,
    IdentityOptions,
    RoleManager,
    SignInManager,
    UpperLookupNormalizer,
    UserClaimsPrincipalFactory,
    UserManager,
)
from pydenticore.authentication import AuthenticationOptions, AuthenticationSchemeProvider
from pydenticore.authentication.interfaces import IAuthenticationSchemeProvider
from pydenticore.authorization import (
    AuthorizationOptions,
    AuthorizationPolicy,
)
from pydenticore.hashers import Argon2PasswordHasher
from pydenticore.http.context import HttpContext, IHttpContextAccessor
from pydenticore.interfaces import (
    ILogger,
    ILookupNormalizer,
    IPasswordHasher,
    IPasswordValidator,
    IRoleValidator,
    IUserClaimsPrincipalFactory,
    IUserConfirmation,
    IUserValidator,
)
from pydenticore.interfaces.stores import IUserStore, IRoleStore
from pydenticore.types import TUser, TRole
from pydenticore.types.decorators import singleton
from pydenticore.validators import UserValidator, RoleValidator, PasswordValidator

from fastapi_pydentity.builders import (
    AuthenticationBuilder,
    AuthorizationBuilder,
    IdentityBuilder,
)
from fastapi_pydentity.dependencies import HttpContext as FastAPIHttpContext, HttpContextAccessor
from fastapi_pydentity.dependencies import (
    PasswordValidatorCollection,
    RoleValidatorCollection,
    UserValidatorCollection,
)
from fastapi_pydentity.infrastructure import DependenciesContainer


class PydentityBuilder:
    def __init__(self):
        self._dependencies = DependenciesContainer()

    @property
    def dependencies(self) -> DependenciesContainer:
        return self._dependencies

    def add_authentication(self, default_scheme: str | None = None) -> AuthenticationBuilder:
        """
        Registers services required by authentication services.

        :param default_scheme:
        :return:
        """
        self._dependencies.update({
            IAuthenticationSchemeProvider: AuthenticationSchemeProvider,
            HttpContext: FastAPIHttpContext,
            IHttpContextAccessor: HttpContextAccessor,
        })

        options = AuthenticationOptions()
        options.default_authentication_scheme = IdentityConstants.ApplicationScheme
        options.default_sign_in_scheme = IdentityConstants.ExternalScheme

        if default_scheme:
            options.default_scheme = default_scheme
            options.default_authentication_scheme = ""

        return AuthenticationBuilder(options)

    def add_authorization(self, default_policy: AuthorizationPolicy | None = None) -> AuthorizationBuilder:
        """
         Adds authorization policy services.

        :param default_policy:
        :return:
        """
        options = AuthorizationOptions()

        if default_policy:
            options.default_policy = default_policy

        return AuthorizationBuilder(options)

    def add_identity(
            self,
            user_store: type[IUserStore],
            role_store: type[IRoleStore],
            configure: Callable[[IdentityOptions], None] | None = None
    ) -> IdentityBuilder:
        """
        Adds and configures the identity system for the specified User and Role types.

        :param user_store: The type representing a User in the system.
        :param role_store: The type representing a Role in the system.
        :param configure: An action to configure the ``IdentityOptions``.
        :return:
        """
        self.add_authentication().add_identity_cookies()
        self._dependencies.update({
            ILogger["UserManager"]: None,
            ILogger["RoleManager"]: None,
            ILogger["SignInManager"]: None,
            IdentityOptions: singleton(IdentityOptions),
            IUserStore[TUser]: user_store,
            IRoleStore[TRole]: role_store,
            IdentityErrorDescriber: IdentityErrorDescriber,
            IPasswordHasher[TUser]: Argon2PasswordHasher,
            Iterable[IPasswordValidator[TUser]]: PasswordValidatorCollection(),
            Iterable[IUserValidator[TUser]]: UserValidatorCollection(),
            Iterable[IRoleValidator[TRole]]: RoleValidatorCollection(),
            ILookupNormalizer: UpperLookupNormalizer,
            UserManager[TUser]: UserManager,
            RoleManager[TRole]: RoleManager,
            IUserConfirmation[TUser]: DefaultUserConfirmation,
            IUserClaimsPrincipalFactory[TUser]: UserClaimsPrincipalFactory,
            SignInManager[TUser]: SignInManager,
        })

        if configure:
            configure(self._dependencies[IdentityOptions]())

        return IdentityBuilder(self._dependencies)

    def add_default_identity(
            self,
            user_store: type[IUserStore],
            role_store: type[IRoleStore],
    ) -> IdentityBuilder:
        """
        Adds a set of common identity services to the application, token providers,
        and configures authentication to use identity cookies.

        :param user_store: The type representing a User in the system.
        :param role_store: The type representing a Role in the system.
        :return:
        """
        builder = self.add_identity(user_store, role_store)
        builder.add_default_token_providers()
        self._dependencies[Iterable[IPasswordValidator[TUser]]].add(PasswordValidator)
        self._dependencies[Iterable[IUserValidator[TUser]]].add(UserValidator)
        self._dependencies[Iterable[IRoleValidator[TRole]]].add(RoleValidator)
        return builder

    def build(self):
        for cls in self._dependencies.values():
            if cls is None:
                continue

            signature = inspect.signature(cls)
            parameters = []

            for parameter in signature.parameters.values():
                if get_origin(parameter.annotation) is Annotated:
                    parameters.append(parameter)
                    continue

                if get_origin(parameter.annotation) in (Union, Generic,):
                    args = get_args(parameter.annotation)
                    if self._dependencies.get(args[0]):
                        parameters.append(
                            parameter.replace(
                                annotation=Annotated[parameter.annotation, Depends(self._dependencies[args[0]])]
                            )
                        )
                else:
                    if depends := self._dependencies.get(parameter.annotation):
                        parameters.append(
                            parameter.replace(
                                annotation=Annotated[parameter.annotation, Depends(depends)]
                            )
                        )
                    else:
                        parameters.append(parameter)

            cls.__signature__ = signature.replace(parameters=parameters)
