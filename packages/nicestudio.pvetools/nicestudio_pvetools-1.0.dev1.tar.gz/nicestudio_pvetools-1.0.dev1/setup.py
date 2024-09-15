kwargs = {
    'name': 'nicestudio.pvetools',
    'version': '1.0.dev1',
    'description': 'Python script for PVE.',
    'long_description': open('README.md').read(),
    'author': 'niceStudio, Inc',
    'author_email': 'service@niceStudio.com.tw',
    'license': 'BSD',
    'url': 'https://github.com/niceStudio/nicestudio.pvetools',
    'package_dir': {'': 'src'},
    # 'packages': find_namespace_packages('src'),
    # namespace_packages=['nicestudio', ],
    'include_package_data': True,
    'zip_safe': False,
    'classifiers': [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Buildout",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    'install_requires': open('requirements.txt').read().split('\n'),
    'entry_points': {'console_scripts': [
        'pvetool = nicestudio.pvetools.pvetool.main:main',
    ]},
}

try:
    from setuptools import find_namespace_packages

    kwargs['packages'] = find_namespace_packages(where='src')
except ImportError:
    from setuptools import find_packages

    kwargs['packages'] = find_packages(where='src')
    kwargs['namespace_packages'] = ['nicestudio', ]

from setuptools import setup

setup(**kwargs)
