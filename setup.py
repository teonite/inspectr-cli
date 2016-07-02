from setuptools import setup

setup(name='inspectr',
      version='0.0.1',
      description='Code quality InspectR',
      url='',
      author='jchmielewski@teonite.com',
      author_email='jchmielewski@teonite.com',
      license='MIT',
      packages=['inspectr'],
      entry_points={
          'console_scripts': ['inspectr=inspectr.main:run'],
      },
      install_requires=[
          "pytz==2016.4",
          "rethinkdb==2.3.0.post4",
          "colorama==0.3.7"
      ],
      setup_requires=['pytest-runner'],
      tests_require=[
          'pytest==2.9.2',
          'pytest-mock==1.1',
          'pyrsistent==0.11.13'
      ],
      zip_safe=False)
