from setuptools import setup,find_packages


requires = ["pycryptodome>=3.16.0","aiohttp>=3.13.2","httpx[http2]==0.26.0","tinytag>=1.10.1","mutagen>=1.47.0","nest_asyncio>=1.6.0"]

extras = {"pillow": ["pillow==9.5.0; python_version < '3.10'","pillow>=12.0.0; python_version >= '3.10'"],"websocket": ["websocket-client>=1.8.0"],"all": ["pillow==9.5.0; python_version < '3.10'","pillow>=12.0.0; python_version >= '3.10'","websocket-client>=1.8.0"]}

_long_description = open("README.md",'r',encoding = 'utf-8').read()


setup(
    name = "Arsein",
    version = "8.8.5",
    author = "arian abasi nedamane",
    author_email = "aryongram@gmail.com",
    description = (" library Robot Rubika"),
    license = "MIT",
    keywords = ["Arsein","Arseinrubika","ArseinRubika","arsein","bot","Bot","BOT","Robot","ROBOT","robot","self","api","API","Api","rubika","Rubika","RUBIKA","Python","python","aiohttp","asyncio"],
    url = "https://github.com/ArseinRubikaApp",
    packages = find_packages(),
    long_description =_long_description,
    long_description_content_type = 'text/markdown',
    install_requires = requires,
    extras_require = extras ,
    classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: Implementation :: PyPy",
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
    'Programming Language :: Python :: 3.14'
    ],
)
