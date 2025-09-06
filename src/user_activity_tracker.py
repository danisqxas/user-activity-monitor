"""
Entry point script for the User Activity Monitor.

This script imports the `userActivityTracker` callable from
 the `user_activity_monitor` module and invokes it when run directly.

The User Activity Monitor tracks selected user activity across Discord servers
or direct messages, logs events, and stores settings in a JSON file. By
exposing this launcher, you can run the monitor standalone without diving
into the package internals.
"""

from .user_activity_monitor import userActivityTracker


def main() -> None:
    """Run the user activity tracker."""
    userActivityTracker()


if __name__ == "__main__":
    main()
