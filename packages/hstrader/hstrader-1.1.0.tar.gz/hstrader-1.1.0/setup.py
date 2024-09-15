# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hstrader',
 'hstrader.config',
 'hstrader.helpers',
 'hstrader.hstrader',
 'hstrader.models',
 'hstrader.services']

package_data = \
{'': ['*']}

install_requires = \
['pydantic', 'requests', 'websockets']

setup_kwargs = {
    'name': 'hstrader',
    'version': '1.1.0',
    'description': 'HsTrader SDK for Python',
    'long_description': '# HsTrader SDK for Python\n\n![PyPI - Version](https://img.shields.io/pypi/v/hstrader)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hstrader)\n[![Documentation](https://img.shields.io/badge/docs-latest-blue)](https://staging.hstrader.com/trader/docs/)\n[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n\n\nhstrader-sdk-py is the [HsTrader](https://hstrader.com) SDK for Python.\n\nThe HsTrader SDK requires a minimum version of Python 3.7.\n\n## Installation\n\n```bash\npip install hstrader\n```\n\n## Documentation\n\nYou can find the latest documentation at the official [HsTrader API documentation](https://demo.hstrader.com/trader/docs)\n\n## Getting Started\n\n### Http Example\n\n```python\nfrom hstrader import HsTrader\n\n\n# Its recommended to use environment variables to store your credentials\nCLIENT_ID = "<YOUR_CLIENT_ID>"\nCLIENT_SECRET = "<YOUR_CLIENT_SECRET>"\nURL = "<YOUR_BROKER_URL>"\n\n\n# Create a new instance of HSTrader\nclient = HsTrader(CLIENT_ID, CLIENT_SECRET, URL)\n\ntry:\n\n    # Get the EURUSD symbol\n    eurusd = client.get_symbol("EURUSD")\n    print(\n        f"Symbol ID: {eurusd.id}, Name: {eurusd.symbol}, Last Bid: {eurusd.last_bid}, Last Ask: {eurusd.last_ask}"\n    )\n\nexcept Exception as e:\n    print(e)\n\n\n```\n\n### Websocket Example\n\n```python\nfrom hstrader import HsTrader\nfrom hstrader.models import Event, Tick\n\n\n# Its recommended to use environment variables to store your credentials\nCLIENT_ID = "<YOUR_CLIENT_ID>"\nCLIENT_SECRET = "<YOUR_CLIENT_SECRET>"\nURL = "<YOUR_BROKER_URL>"\n\n\n# Create a new instance of HSTrader\nclient = HsTrader(CLIENT_ID, CLIENT_SECRET, URL)\n\n\n# Create a callback function to handle market updates\n@client.subscribe(Event.MARKET) # alternatively, you can use @client.subscribe("market")\ndef on_market(tick: Tick):  # this function will be called whenever a new market update is received\n    print(\n        f"Received tick for symbol {tick.symbol_id}: bid = {tick.bid} ask = {tick.ask}"\n    )\n\n\n# Start listening to real-time data\nclient.start()\n\n\n```\n\nFor more examples, please refer to the [examples](/examples/) directory.\n## Contributing\n\nContributions are welcome.<br/>\nIf you\'ve found a bug within this project, please open an issue to discuss what you would like to change.<br/>\nIf it\'s an issue with the API, please open a topic at [Contact Us](https://hstrader.com/contact-us/).\n',
    'author': 'Hybrid Solutions',
    'author_email': 'dev@hybridsolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
