from setuptools import find_packages

from gcloud_resize import __version__, name, APP_HOME, LOG_DIR, shell
from setuptools import setup


setup(
  name = name,
  version = __version__,
  description='Automatic resizing of persistent disks in Google Cloud.',
  url='https://github.com/gutsul/gcloud-resize',
  author='Yuriy Grigortsevich',
  author_email='GrigortsevichYuriy@gmail.com',
  packages = find_packages(exclude=('tests', 'docs')),
  install_requires=[
    'requests==2.2.1',
    'google-api-python-client==1.6.4',
    'psutil==5.4.7',
    'pyasn1==0.4.4',
    'pyasn1-modules==0.2.2'
  ],
  data_files = [
    (APP_HOME, ['gcloud_resize/conf/gcloud-resize.conf']),
    (LOG_DIR, [])
  ],
  entry_points = {
    'console_scripts': [
        'gcloud-resize = gcloud_resize.__main__:main'
    ]
  }
)