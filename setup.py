from distutils.core import setup

setup(
    name='InterviewAlexa',
    version='0.1.0',
    author='Carlos E. Rodriguez',
    author_email='crodriguez1a@gmail.com',
    packages=['interview_alexa', 'tests'],
    scripts=['bin/sample_test.py'],
    url='http://pypi.python.org/pypi/InterviewAlexa/',
    license='LICENSE.txt',
    description='A Python Testing Framework for Alexa using ASK CLI',
    long_description=open('README.rst').read(),
    install_requires=[
        "python-lambda-local >= 0.1.5"
    ],
    keywords='alexa aws aws-cli lambda lex'
)
