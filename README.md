# User Activity Monitor

Aerthex User Activity Monitor is a modular Python toolkit for tracking and analysing user activity events across digital communities, such as Discord servers. It exposes an asynchronous API to register and retrieve user interactions, persist them to disk, and integrate seamlessly with Discord bots.

## Features

- **Advanced tracking logic** – Monitors users across multiple servers and direct messages with fine‑grained settings.
- **Asynchronous design** – Built on `asyncio` to avoid blocking your bot and integrate cleanly with Discord interactions.
- **Settings management** – Load and update tracked users and selected events in a JSON configuration file.
- **Rich API** – Provides functions to record events, compute time deltas, and build summary reports.
- **Modern GUI scaffold** – Includes an example of a custom `customtkinter` interface for visualising user activity.
- **Extensible** – Designed to be the core of a larger application; can be imported as a library or run as a standalone tool.

## Repository Structure

```
user-activity-monitor/
├── src/
│   ├── user_activity_monitor.py  # Advanced monitor implementation
│   ├── user_activity_tracker.py  # Backwards‑compatible stub importing the new monitor
│   └── __init__.py               # Exposes public APIs
├── tests/
│   └── test_user_activity_monitor.py  # Basic import test (you can expand this)
├── .github/
│   └── workflows/                # Continuous integration configuration
├── LICENSE
├── README.md
└── requirements.txt
```

## Installation

To set up the environment, clone the repository and install the dependencies:

```bash
git clone https://github.com/danisqxas/user-activity-monitor.git
cd user-activity-monitor
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

The primary external dependency is `discord.py`, which is used only if you integrate the monitor into a bot. All other modules are part of the Python standard library.

## Usage

You can import the monitor in your own code and invoke the API functions:

```python
from user_activity_monitor import userActivityTracker

tracker = userActivityTracker()
# Update settings
await tracker.updateUserActivitySettings('tracked_users', [123456789012345678])
# Retrieve settings
settings = await tracker.getUserActivitySettings()
print(settings['tracked_users'])
```

If you want to run the included customtkinter interface, adapt the `user_activity_monitor.py` code to fit your bot or desktop application. The monitor is designed to be extended; feel free to add your own event handlers or outputs.

## Running Tests

This repository uses [pytest](https://docs.pytest.org/) for testing. To run the test suite:

```bash
pytest -q
```

You can expand the tests to cover your custom logic and ensure your modifications stay correct.

## Contributing

Contributions and suggestions are welcome! If you’d like to improve the monitor, build out the GUI, or add more tests, feel free to fork the repository and open a pull request. Please make sure to run the tests and follow Pythonic style before submitting changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
