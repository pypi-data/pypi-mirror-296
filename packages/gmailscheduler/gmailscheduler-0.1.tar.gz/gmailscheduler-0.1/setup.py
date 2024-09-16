from setuptools import setup, find_packages

setup(
    name='gmailscheduler',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'google-auth>=2.0.0',
        'google-auth-oauthlib>=0.4.0',
        'google-auth-httplib2>=0.1.0',
        'google-api-python-client>=2.0.0',
        'pytz>=2021.1'
    ],
    description='A flexible, timezone-aware event scheduler',
    author='Sathish Jindam',
    author_email='sathishjindam98@gmail.com',
    url='https://github.com/yourusername/gmailscheduler',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
