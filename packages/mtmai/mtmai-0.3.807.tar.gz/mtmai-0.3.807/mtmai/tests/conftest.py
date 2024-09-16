import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession
from sqlmodel.pool import StaticPool

from mtmai.core.config import settings
from mtmai.core.db import init_db
from mtmai.core.seed import seed_db
from mtmai.deps import get_db
from mtmai.server import build_app
from mtmai.tests.utils.user import authentication_token_from_email
from mtmai.tests.utils.utils import get_superuser_token_headers

os.environ["PYTEST_CURRENT_TEST"] = "1"
print(
    "testing start ========================================================================================================="
)


@pytest.fixture(scope="module")
def engine() -> Generator:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    yield engine

    print("==================================drop db")
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="module")
async def async_engine():
    engine = create_async_engine(
        "sqlite+aiosqlite://", connect_args={"check_same_thread": False}
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope="module")
async def asession(async_engine) -> AsyncSession:
    async_session = sessionmaker(
        async_engine, class_=SQLModelAsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


# @pytest.fixture(scope="session")
@pytest.fixture(scope="module")
def db(engine) -> Generator:
    with Session(engine) as session:
        seed_db(session)
        init_db(session)
        yield session


def override_get_db(db: Session):
    def _override_get_db() -> Generator[Session, None, None]:
        yield db

    return _override_get_db


@pytest.fixture(scope="module")
def client(db: Session) -> Generator[TestClient, None, None]:
    app = build_app()
    app.dependency_overrides[get_db] = override_get_db(db)
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
async def normal_user_token_headers(
    client: TestClient, db: AsyncSession
) -> dict[str, str]:
    return await authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
