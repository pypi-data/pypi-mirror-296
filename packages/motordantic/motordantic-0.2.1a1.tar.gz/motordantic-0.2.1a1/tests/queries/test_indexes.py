import pytest
import pytest_asyncio
from pymongo import IndexModel

from motordantic.document import Document
from motordantic.exceptions import MotordanticIndexError
from motordantic.utils.pydantic import IS_PYDANTIC_V2
from motordantic.config import ConfigDict


class IndexTicket(Document):
    name: str
    position: int
    config: dict

    if IS_PYDANTIC_V2:
        model_config = ConfigDict(  # type: ignore
            indexes=[
                IndexModel([("position", 1)]),
                IndexModel([("name", 1)]),
            ]
        )
    else:

        class Config:
            indexes = [
                IndexModel([("position", 1)]),
                IndexModel([("name", 1)]),
            ]


@pytest_asyncio.fixture(scope="session", autouse=True)
async def drop_ticket_collection(event_loop):
    await IndexTicket.ensure_indexes()
    yield
    await IndexTicket.Q.drop_collection(force=True)


@pytest.mark.asyncio
async def test_check_indexes(connection):
    result = await IndexTicket.Q.list_indexes()
    assert result == {
        "_id_": {"key": {"_id": 1}},
        "position_1": {"key": {"position": 1}},
        "name_1": {"key": {"name": 1}},
    }


@pytest.mark.asyncio
async def test_check_indexes_if_remove(connection):
    class IndexTicket(Document):
        name: str
        position: int
        config: dict

        if IS_PYDANTIC_V2:
            model_config: ConfigDict = ConfigDict(
                indexes=[
                    IndexModel([("position", 1)]),
                ]
            )
        else:

            class Config:
                indexes = [
                    IndexModel([("position", 1)]),
                ]

    await IndexTicket.ensure_indexes()
    result = await IndexTicket.Q.list_indexes()
    assert result == {
        "_id_": {"key": {"_id": 1}},
        "position_1": {"key": {"position": 1}},
    }


@pytest.mark.asyncio
async def test_drop_index(connection):
    with pytest.raises(MotordanticIndexError):
        result = await IndexTicket.Q.drop_index("position1111")

    result = await IndexTicket.Q.drop_index("position_1")
    assert result == "position_1 dropped."
