from setuptools import setup

setup(
    name='clp2qr',
    version='1.0.0',
    include_package_data=True,
    description='Clipboard to QR',
    license="MIT",
    install_requires=[
        'pywin32==306',
        'qrcode==7.4.2',
        'qreader==3.14',
    ],
    py_modules=['clp2qr'],
    package_data={
        '': ['clp2qr.py']
    }
)
