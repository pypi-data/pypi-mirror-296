from setuptools import setup, find_packages


setup(
    name='genoforge',
    version='0.0.3',

    url='https://github.com/Jorgelzn/Genoforge',
    author='Jorge Lizcano',
    author_email='jorgelizgo@gmail.com',

    long_description_content_type='text/markdown',
    long_description=open('README.md').read().replace('<img src="bees.gif" alt="drawing" width="200"/>',''),

    packages=find_packages(include=['genoforge']),

    install_requires=['numpy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=4'],
    test_suite='tests'
)