import setuptools #导入setuptools打包工具
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="nonebot-plugin-QRrender", # 用自己的名替换其中的YOUR_USERNAME_
    version="0.0.6",    #包版本号，便于维护版本
    author="Funny1Potato",    #作者，可以写自己的姓名
    author_email="funny_potato@126.com",    #作者联系方式，可写自己的邮箱地址
    description="将文本转为二维码，可自定义样式",#包的简述
    long_description=long_description,    #包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    install_requires=("nonebot2>=2.3","nonebot-adapter-onebot>=2.4","httpx>=0.27","amzqr>=0.0.1","nonebot-plugin-localstore>=0.7"),
    url="https://github.com/Funny1Potato/nonebot-plugin-QRrender",    #自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',    #对python的最低版本要求
)
