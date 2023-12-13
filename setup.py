from setuptools import find_packages, setup

setup(
    name="E_chat",
    version="1.0.0",
    description="A chat web application",
    author="E-code",
    author_email="ecode5814@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask", "gunicorn",],
)
