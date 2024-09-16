from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()

setup(name="Message_client_k2foxspb",
      version="0.1.1",
      description="mess_client",
      long_description=readme(),
      author="@k2Fox",
      author_email="k2foxspb@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']

      )
