
from setuptools import setup, find_packages
from gcloud_resize import __version__

setup(
    name = 'gcloud-resize',
    version = __version__,
    description='Automatic resizing of persistent disks in Google Cloud.',
    url='https://github.com/gutsul/gcloud-resize',
    author='Yuriy Grigortsevich',
    author_email='GrigortsevichYuriy@gmail.com',
    packages = find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'requests==2.2.1',
        'google-api-python-client==1.6.4',
        'psutil==5.4.1',
        'python-dotenv==0.8.2',
    ],
    entry_points = {
        'console_scripts': [
            'gcloud-resize = gcloud_resize.__main__:main'
        ]
    })