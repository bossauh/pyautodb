from distutils.core import setup

install_requires = [
    "dnspython==2.2.0",
    "mongita==1.1.1",
    "motor==2.5.1",
    "pymongo==3.12.3"
]


setup(
    name="pyautodb",
    packages=["pyautodb"],
    version="0.1",
    license="MIT",
    description="A library that combines multiple document based databases.",
    author="Philippe Mathew",
    author_email="philmattdev@gmail.com",
    url="",
    download_url="",
    install_requires=install_requires
)
