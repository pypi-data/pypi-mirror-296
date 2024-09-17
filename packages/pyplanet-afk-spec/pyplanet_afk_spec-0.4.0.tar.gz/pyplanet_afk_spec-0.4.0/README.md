# afk_spec

PyPlanet plugin to detect AFK players and move them into spectator mode.

This plugin works by repeatedly querying the player's inputs and checking if the player is currently steering, braking or pressing the gas pedal.
If the player is found not to be pressing any inputs for a configurable period of time, they are considered AFK and moved to spectator.

### Installation

    python -m pip install --upgrade pyplanet-afk-spec

Then open `settings/apps.py` with a text editor and append to the list in 'default':

    'feor.afk_spec'

### Configuration

- AFK Timeout: Duration players can stay inactive until they are declared AFK, in seconds. [Default: 120]

- AFk Check Frequency: Time to wait before checking again whether a player is AFK, in seconds. [Default: 10]

- Afk Grace Period: Time to wait before checking again whether a player is AFK again if they have been confirmed not to be AFK, in seconds. [Default: 30]

- AFK Delay: Time to wait before querying a player's inputs again, in ms. Lower values may impact performance. [Default: 1000]