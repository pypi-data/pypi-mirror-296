from setuptools import setup

setup(
    name='sublister',
    version='1.0',
    packages=['sublister'],
    package_dir={'sublister': '.'},
    py_modules=['sublister'],
    entry_points={
        'console_scripts': [
            'sublister = sublister:main',
        ]
    },
    author='Mathias Bochet (aka Zen)',
    description='A tool to find subdomains passively',
    long_description="sublister is a tool designed to enumerate subdomains using search engines, websites and apis.",
    url='https://github.com/42zen/sublister',
    install_requires=[
        'requests',
        'beautifulsoup4',
        'fake-useragent',
        'python-dotenv',
    ],
)