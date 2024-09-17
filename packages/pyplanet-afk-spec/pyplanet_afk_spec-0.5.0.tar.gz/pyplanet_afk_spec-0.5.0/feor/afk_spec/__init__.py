import logging
import asyncio

from pyplanet.apps.config import AppConfig

from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from .views import AFKWidget
from pyplanet.core.signals import pyplanet_start_after
from pyplanet.contrib.setting import Setting

logger = logging.getLogger(__name__)


class AfkSpecApp(AppConfig):
    game_dependencies = ['trackmania']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = AFKWidget(self)
        self.setting_afk_timeout = Setting(
            'afk_timeout', 'AFK Timeout', Setting.CAT_BEHAVIOUR, type=int,
            description='Duration players can stay inactive until they are declared AFK, in seconds. [Default: 120]',
            default=120
        )
        self.setting_afk_timeout_frequence_check = Setting(
            'afk_timeout_frequence_check', 'AFK Check Frequence', Setting.CAT_BEHAVIOUR, type=int,
            description=' Time to wait before checking again whether a player is AFK, in seconds. [Default: 10]',
            default=10)
        
        self.setting_afk_timeout_sleep_delay = Setting(
            'afk_timeout_sleep_delay', 'AFK Delay', Setting.CAT_BEHAVIOUR, type=int,
            description="Time to wait before querying a player's inputs again, in ms. Lower values may impact performance. [Default: 1000]",
            default=1000)
        
        self.setting_afk_grace_period = Setting(
            'afk_grace_period', 'AFK Grace Period', Setting.CAT_BEHAVIOUR, type=int,
            description='Time to wait before checking again whether a player is AFK again if they have been confirmed not to be AFK, in seconds. [Default: 30]',
            default=30)
        
    async def on_start(self):
        self.context.signals.listen(mp_signals.player.player_connect, self.player_connect)
        self.context.signals.listen(mp_signals.map.map_begin, self.map_start)
        self.context.signals.listen(pyplanet_start_after, self.on_after_start)
        
        # Register settings
        await self.context.setting.register(self.setting_afk_timeout)
        await self.context.setting.register(self.setting_afk_timeout_frequence_check)
        await self.context.setting.register(self.setting_afk_timeout_sleep_delay)
        await self.context.setting.register(self.setting_afk_grace_period)

    async def player_connect(self, player, **kwargs):
        await self.widget.display(player)

    async def map_start(self, *args, **kwargs):
        await self.widget.display()

    async def on_after_start(self, *args, **kwargs):
        await asyncio.sleep(1)
        asyncio.ensure_future(asyncio.gather(*[
            self.player_connect(p) for p in self.instance.player_manager.online
        ]))
