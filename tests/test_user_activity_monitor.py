import importlib
def test_import_user_activity_monitor():
    """Test that the userActivityTracker function is available in the module."""
    module = importlib.import_module("src.user_activity_monitor")
    assert hasattr(module, "userActivityTracker")
