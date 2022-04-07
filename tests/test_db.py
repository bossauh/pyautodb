"""
Tests are mostly focused on Mongita itself rather than MongoDB.
"""

import os
import shutil
from maglevapi.testing import Testing
from pyautodb import AutoDBClient, Config
from faker import Faker
from .blueprints import *


class TestDatabase(Testing):

    COLS = ["collection_1", "collection_2", "collection_3", "collection_4"]
    PATH = "./tests/db"
    OPERATION_TEST_ITERS = 1000

    def __init__(self) -> None:
        super().__init__()

        if os.path.exists(self.PATH):
            shutil.rmtree(self.PATH)

        self.faker = Faker()
        self.blueprints = {
            "user": User,
            "coordinates": Coordinates
        }

    async def run_operations(self, db) -> None:
        """
        Simple test operation.
        """

        for i in range(self.OPERATION_TEST_ITERS):
            for col in self.COLS:
                db[col].insert_one({
                    "index": i,
                    "id": self.faker.ean(prefixes=("00", ), length=13),
                    "locale": self.faker.locale(),
                    "address": self.faker.address(),
                    "plate": self.faker.license_plate()
                })

        for col in self.COLS:
            count = db[col].count_documents({})
            assert count == self.OPERATION_TEST_ITERS

    async def retrieve_objects(self, client) -> None:
        for i in self.COLS:
            results = client.find_as_objects(i, "user")
            for r in results:
                assert isinstance(r, User)

        assert client.find_as_objects("coordinates", "coordinates") == []

    async def test_mongita(self) -> None:
        client = AutoDBClient("testing", Config("mongita", path=self.PATH))
        assert os.path.exists(self.PATH)

        db = client.db
        await self.run_operations(db)
        client.internal_client.close()
        shutil.rmtree(self.PATH)

    async def test_mongita_memory(self) -> None:
        client = AutoDBClient("testing", Config(
            "mongita_memory", path=self.PATH))
        assert not os.path.exists(self.PATH)

        db = client.db
        await self.run_operations(db)
        client.internal_client.close()

    async def test_mongita_fallback(self) -> None:
        client = AutoDBClient("testing", Config("mongodb", path=self.PATH))
        assert client.engine == "mongita"

        db = client.db
        await self.run_operations(db)
        client.internal_client.close()
        shutil.rmtree(self.PATH)

    async def test_objectify(self) -> None:
        client = AutoDBClient("testing", Config(
            "mongita", path=self.PATH, blueprints=self.blueprints))
        assert client.blueprints == self.blueprints

        await self.run_operations(client.db)
        await self.retrieve_objects(client)
        client.internal_client.close()
        shutil.rmtree(self.PATH)
