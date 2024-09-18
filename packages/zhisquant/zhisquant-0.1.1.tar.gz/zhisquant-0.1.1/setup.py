from setuptools import setup, find_packages

setup(
    name='zhisquant',  # 包名
    version='0.1.1',
    description='ZhiSQuant SDK for interacting with the ZhiSQuant API',
    author='Maple',
    author_email='mapleccs@outlook.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.0.0',
        'pandas>=1.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
