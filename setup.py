from setuptools import setup

setup(
    name='fld_toolbox',
    version="0.0.5",
    description='A simple Python toolbox',
    url='https://github.com/soberz-fld/fld_toolbox',
    author='Lars Wilting',
    license='GNU GENERAL PUBLIC LICENSE',
    package_dir={'fld_toolbox': 'src'},
    packages=['fld_toolbox', 'fld_toolbox.calcs', 'fld_toolbox.networking', 'fld_toolbox.connectors', 'fld_toolbox.media', 'fld_toolbox.files'],
    install_requires=[
        'requests',
        'Levenshtein',
        'mariadb',
        'pyModbusTCP',
        'schedule',
        'opencv-python',
        'numpy',
        'geopy',
        'pyproj',
        'pytz'
    ],
    classifiers=[],
)
