from pytonapi import schema
from tests.async_tonapi import TestAsyncTonapi

ACCOUNT_ID = "0:0336261f4d3e8a3521b5fc38ee30d203de5ec60d8231a4b3f2e42d512bedd7cc"  # noqa
EVENT_ID = "68656e74d18b10309e41e057191abcfc42f973c82bc84326985cdbf7bf89b126"


class TestJettonMethod(TestAsyncTonapi):

    async def test_get_info(self):
        response = await self.tonapi.jettons.get_info(ACCOUNT_ID)
        self.assertIsInstance(response, schema.jettons.JettonInfo)

    async def test_get_holders(self):
        response = await self.tonapi.jettons.get_holders(ACCOUNT_ID)
        self.assertIsInstance(response, schema.jettons.JettonHolders)

    async def test_get_all_holders(self):
        response = await self.tonapi.jettons.get_all_holders(ACCOUNT_ID)
        self.assertIsInstance(response, schema.jettons.JettonHolders)

    async def test_get_all_jettons(self):
        response = await self.tonapi.jettons.get_all_jettons()
        self.assertIsInstance(response, schema.jettons.Jettons)

    async def test_get_jetton_transfer_event(self):
        response = await self.tonapi.jettons.get_jetton_transfer_event(EVENT_ID)
        self.assertIsInstance(response, schema.events.Event)
