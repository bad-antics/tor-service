from tor_service.core import TorChecker
c=TorChecker()
print(f"Tor running: {c.check_tor_running()}")
