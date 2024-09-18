<p align="center">
<img src="assets/icon.png">

<p align="center">➡️ <a href="methods.md">Method References</a> ⬅️</p>

<p align="center">Satisfactory Dedicated Server HTTP API Python wrapper<br>
<code>pip install pyfactorybridge</code>
</p>

# Overview
This is a Python wrapper for the Satisfactory Dedicated Server HTTP API. It is designed to make it easier to interact with the API and to provide a more Pythonic interface.

# Features
Direct 1:1 implementation to the offical documentation. All API endpoints supported. No need to manually construct URLs or handle HTTP requests. Easy to use and understand.

# Demo

*All methods are documented in the [methods.md](methods.md) file.*

```py
from pyfactorybridge import API
from pyfactorybridge.exceptions import SaveGameFailed

# Authenticate with the password... (not recommended)
# satisfactory = API(address="XXXX:7777", password="XXXX")

# Or with the token...
satisfactory = API(address="XXXX:7777", token="XXXX")

try:
    satisfactory.save_game(SaveName="Test")
except SaveGameFailed as error:
    print("Could not save game!")

print(satisfactory.get_server_options())

satisfactory.shutdown()
```
