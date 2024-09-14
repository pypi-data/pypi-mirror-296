from setuptools import setup, find_packages

setup(
    name="chat-sosal",  # Уникальное имя пакета
    version="2.1.4",  # Увеличивайте версию при каждом изменении
    author="feeland",
    author_email="prokuronov.valera@mail.ru",
    description="This is the simplest module for quick work with files.",
    long_description='222',  # Полное описание, например, из файла README.md
    url="https://github.com/yourusername/yourrepository",  # URL репозитория, если есть
    packages=find_packages(),  # Автоматический поиск всех пакетов
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT Licen"
        "se",  # Лицензия
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Требуемая версия Python
    install_requires=["aiohttp", "pytz", "grapheme", "emoji"],
)
