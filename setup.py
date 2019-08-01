from setuptools import setup, find_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.15.0'

setup(name='collective.pwexpiry',
      version=version,
      description="Emulate Active Directory password complexity requirements \
                  in Plone",
      long_description=read("README.rst") + "\n" + read("CHANGES.rst"),
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Security",
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "Framework :: Plone :: 5.0",
          "Framework :: Plone :: 5.1",
          "Framework :: Plone :: 5.2",
          "License :: OSI Approved :: Zope Public License",
      ],
      keywords='',
      author='Enfold Systems, Inc.',
      author_email='info@enfoldsystems.com',
      url='http://www.enfoldsystems.com',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.api',
          'collective.monkeypatcher',
          'six',
      ],
      extras_require={
          'test': [
              'cssselect',
              'lxml',
              'mock',
              'plone.api >=1.8.5',
              'plone.app.robotframework',
              'plone.app.testing [robot]',
              'plone.browserlayer',
              'plone.cachepurging',
              'plone.testing',
              'robotsuite',
              'testfixtures',
              'transaction',
              'tzlocal',
          ],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone

      [zopectl.command]
      notify_and_expire = collective.pwexpiry.scripts.notify_and_expire:entrypoint
      """,
      )
