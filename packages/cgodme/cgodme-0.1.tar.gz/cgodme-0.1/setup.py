from setuptools import setup, find_packages

setup(
    name="cgodme",
    version="0.1",
    description="Recalibrate Path Flows to Achieve Target OD Flow Consistency",
    author="Taehooie Kim, Ph.D., Xin Wu, Ph.D., Han Zheng, Ph.D., Xuesong Zhou, Ph.D.",
    author_email="taehooie.kim@gmail.com, xin.wu@villanova.edu, hzheng73@asu.edu, xzhou74@asu.edu",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'cgodme': ["config.yaml"]
    }
)