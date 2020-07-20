from setuptools import find_packages, setup


# with open('README.rst') as f:
#     LONG_DESC = f.read()

setup(
    name='nea',
    version='0.0.1',
    url='http://example.com',
    description='Test exercise to build a server and clients over TLS',
    # long_description=LONG_DESC,
    author='Pynchia', author_email='pyncha@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'],
    keywords=['nea', ],
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    entry_points="""
    [console_scripts]
    clientcli = nea.client.cli:cli
    servercli = nea.server.cli:cli
    """,
    install_requires=[]
)
