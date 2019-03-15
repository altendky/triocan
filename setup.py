import setuptools
import versioneer


with open('README.rst') as f:
    readme = f.read()


extras_require_test = [
    'coverage',
    'pytest',
    'pytest-cov',
    'tox',
]


setuptools.setup(
    name='triocan',
    author='Kyle Altendorf',
    description='CANbus, be it with a pair of wires or a trio',
    long_description=readme,
    long_description_content_type='text/x-rst',
    url='https://github.com/altendky/triocan',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='MIT',
    classifiers=[
        # complete classifier list:
        #   https://pypi.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
    ],
    entry_points={
        'console_scripts': [
            'triocan = triocan.cli:main',
        ],
    },
    python_requires='>=3.5',
    install_requires=[
        'python-can',
        'trio'
    ],
    extras_require={
        'dev': [
            'gitignoreio',
            *extras_require_test,
        ],
        'test': extras_require_test,
    },
)
