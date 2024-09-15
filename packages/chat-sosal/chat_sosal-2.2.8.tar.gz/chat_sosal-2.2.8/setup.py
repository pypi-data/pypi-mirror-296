from setuptools import setup, find_packages

setup(
    name="chat-sosal",
    version="2.2.8",
    author="feeland",
    author_email="prokuronov.valera@mail.ru",
    description="sosAl?",
    long_description='sosAl?',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=["aiohttp", "pytz", "grapheme", "emoji"],
)
