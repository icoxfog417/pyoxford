from distutils.core import setup

setup(
    name='pyoxford',
    packages=['pyoxford'],
    install_requires=[
        'PyYAML',
        'requests'
    ],
    version='0.1.1',
    description='Python library to access Microsoft Project Oxford',
    author='icoxfog417',
    author_email='icoxfog417@yahoo.co.jp',
    url='https://github.com/icoxfog417/pyoxford',
    download_url='https://github.com/icoxfog417/pyoxford/tarball/master',
    keywords=['microsoft', 'project oxford', 'machine learning'],
    classifiers=[],
)
