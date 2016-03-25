from setuptools import setup, find_packages

setup(name="pyfortunes",
      version="0.1",
      description="fortune as a Web service",
      url="http://sd-20870.dedibox.fr/fortunes",
      author="Dimitri Merejkowsky",
      author_email="d.merej@gmail",
      packages=find_packages(),
      include_package_data = True,
      install_requires=[
          # server
          "flask",
          # client
          "beautifulsoup4",
          "pyxdg",
          "requests",
      ],
      license="BSD",
      scripts=[
          "bin/pyf-dtc",
          "bin/pyf-get",
          "bin/pyf-parse",
          "bin/pyf-server",
    ]
)
