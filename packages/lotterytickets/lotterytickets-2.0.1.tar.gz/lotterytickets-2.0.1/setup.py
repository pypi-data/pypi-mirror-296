# coding:UTF-8
import setuptools

setuptools.setup(
    name="lotterytickets",
    version="2.0.0",
    author="Chay",
    author_email="lichenyi_2020@qq.com",
    url="https://github.com/lichenyichay/lotterytickets-Including/",
    description="lotterytickets-Including",
    long_description="彩票一体机",
    python_requires=">=3.5",
    install_requires=['numberandchinese>=1.0'],
    packages_dir={"": "src"},
    packages_data={"": ["*.txt", "*.info", "*.properties"], "": ["data/*.*"]},
    exclude=["*.test", "*.test.*", "test.*", "test"],
    classifiers=['Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 2",
                 "Programming Language :: Python :: 3"
                 ]
)
