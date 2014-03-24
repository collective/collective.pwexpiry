from setuptools import setup, find_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = read('collective', 'pwexpiry', 'version.txt').strip()

setup(name='collective.pwexpiry',
      version=version,
      description="Emulate Active Directory password complexity requirements \
                  in Plone",
      long_description=read("README.rst") + "\n" + read("CHANGES.txt"),
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Security",
          "Framework :: Plone",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
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
      ],
      extras_require={
          "test": [
              "Plone",
              "plone.app.testing",
          ],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
