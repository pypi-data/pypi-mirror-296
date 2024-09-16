from setuptools import setup, find_packages

setup(
    name='envModule',
    version='0.0.3',
    packages=find_packages(),
    description='Library to read .env files',
    author='Mansur Uldanov',
    author_email='uldanovmansur2005@gmail.com',
    url='',  # ссылка на репозиторий (если есть)
    py_modules=['envmodule'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
