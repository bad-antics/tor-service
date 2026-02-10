from setuptools import setup, find_packages
setup(name="tor-service",version="2.0.0",author="bad-antics",description="Tor hidden service and onion routing toolkit",packages=find_packages(where="src"),package_dir={"":"src"},python_requires=">=3.8")
