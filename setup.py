from setuptools import setup

setup(
    name='Flask-Zipper',
    description='Pythonic JSON payload validator for requested JSON payload of Flask',
    version='1.0',
    url='https://github.com/JoMingyu/Flask-Zipper',
    license='Apache License 2.0',
    author='PlanB, devArtoria',
    maintainer='PlanB, devArtoria',
    maintainer_email='call.viper.sign@gmail.com',
    install_requires=[
        'Flask',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=['flask_zipper']
)