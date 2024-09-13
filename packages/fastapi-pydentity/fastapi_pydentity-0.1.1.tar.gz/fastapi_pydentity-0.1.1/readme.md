<h1 align="center">FastAPI-Pydentity</h1>

# Installation

First you have to install `fastapi-pydentity` like this:

    pip install fastapi-pydentity

You can also install with your db adapter:

For SQLAlchemy:

    pip install fastapi-pydentity[sqlalchemy]

For Tortoise ORM:

    pip install fastapi-pydentity[tortoise]


## Example

```python
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydenticore import SignInManager, UserManager, RoleManager

from examples.models import User, Role
from examples.schemes import RegisterInputModel, LoginInputModel
from examples.stores import UserStore, RoleStore, ROLES
from fastapi_pydentity import PydentityBuilder
from fastapi_pydentity.authentication import use_authentication
from fastapi_pydentity.authorization import use_authorization, authorize


def add_default_roles():
    role_1 = Role("sysadmin", normalized_name="sysadmin".upper())
    role_2 = Role("admin", normalized_name="admin".upper())
    role_3 = Role("manager", normalized_name="manager".upper())
    role_4 = Role("user", normalized_name="user".upper())

    ROLES.update({
        role_1.normalized_name: role_1,
        role_2.normalized_name: role_2,
        role_3.normalized_name: role_3,
        role_4.normalized_name: role_4,
    })


@asynccontextmanager
async def lifespan(app):
    add_default_roles()
    yield


builder = PydentityBuilder()
builder.add_default_identity(UserStore, RoleStore)
builder.build()

app = FastAPI(lifespan=lifespan)

use_authentication(app)
use_authorization(app)


@app.post("/register")
async def register(
        model: Annotated[RegisterInputModel, Depends()],
        user_manager: Annotated[UserManager, Depends()],
        signin_manager: Annotated[SignInManager, Depends()],
):
    if model.password.get_secret_value() != model.confirm_password.get_secret_value():
        raise HTTPException(status_code=400, detail=["Passwords don't match."])

    user = User(email=model.email, username=model.email)
    result = await user_manager.create(user, model.password.get_secret_value())

    if result.succeeded:
        await signin_manager.sign_in(user, is_persistent=False)
    else:
        raise HTTPException(status_code=400, detail=[err.description for err in result.errors])


@app.post("/register-admin")
async def register_admin(user_manager: Annotated[UserManager, Depends()]):
    user = User(email="admin@example.com", username="admin@example.com")
    result = await user_manager.create(user, "P@ssw0rd")

    if not result.succeeded:
        raise HTTPException(status_code=400, detail=[err.description for err in result.errors])

    await user_manager.add_to_roles(user, "admin")


@app.post("/login")
async def login(model: Annotated[LoginInputModel, Depends()], signin_manager: Annotated[SignInManager, Depends()]):
    result = await signin_manager.password_sign_in(
        model.email,
        model.password.get_secret_value(),
        model.remember_me
    )

    if not result.succeeded:
        raise HTTPException(status_code=401, detail="Invalid login attempt.")

    if result.requires_two_factor:
        return {"requiresTwoFactor": True}

    if result.is_locked_out:
        raise HTTPException(status_code=401, detail="Invalid login attempt.")


@app.post("/logout", dependencies=[authorize()])
async def logout(signin_manager: Annotated[SignInManager, Depends()]):
    await signin_manager.sign_out()


@app.get("/users", dependencies=[authorize()])
async def get_users(user_manager: Annotated[UserManager, Depends()]):
    return [user.email for user in await user_manager.all()]


@app.get("/roles", dependencies=[authorize("admin")])
async def get_roles(role_manager: Annotated[RoleManager, Depends()]):
    return [role.name for role in await role_manager.all()]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
```

