from setuptools import setup, find_packages

setup(
    name='leanhtml',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'leanhtml': ['templates/lean.html'],
    },
    install_requires=[
        'flask',
        'htmlmin',
    ],
)
