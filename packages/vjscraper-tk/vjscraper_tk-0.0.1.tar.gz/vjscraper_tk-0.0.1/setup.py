from setuptools import setup

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="vjscraper-tk",
    version="0.0.1",
    license="MIT License",
    author="Renan de Souza Rodrigues",
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email="renanrodrigues7110@gmail.com",
    keywords=[
        "vjscraper",
        "tiktok",
        "tiktok-scraper",
        "vjscraper-tk",
    ],
    description="Scraper de views do TikTok",
    packages=["vjscraper_tk"],
    install_requires=["playwright"],
)
