from setuptools import setup, find_packages

setup(
    name='camegame',
    version='0.0.7',
    description='권남서버에서 유래된 똥 코드 작성함',
    author='ohhi3368',
    author_email='gamechobo11@gmail.com',
    url='',
    keywords=['abusing', 'camegame'],
    python_requires='>=3.6',
    requires=['hashlib','requests','binascii'],
    package_data={},
    zip_safe=False,
    classifiers=['Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',],
    packages=find_packages(),
)