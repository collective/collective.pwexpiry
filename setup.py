from setuptools import setup, find_namespace_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0.0'

setup(name='collective.pwexpiry',
      version=version,
      description="Emulate Active Directory password complexity requirements \
                  in Plone",
      long_description=read("README.rst") + "\n" + read("CHANGES.rst"),
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: 3.12",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Security",
          "Framework :: Plone",
          "Framework :: Plone :: 5.2",
          "Framework :: Plone :: 6.0",
          "License :: OSI Approved :: Zope Public License",
      ],
      keywords='',
      author='Enfold Systems, Inc.',
      author_email='info@enfoldsystems.com',
      url='http://www.enfoldsystems.com',
      license='ZPL',
      packages=find_namespace_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.api',
          'collective.monkeypatcher',
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

      [plone.autoinclude.plugin]
      target = plone

      [zopectl.command]
      notify_and_expire = collective.pwexpiry.scripts.notify_and_expire:entrypoint
      """,
      )
