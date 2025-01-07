# 项目为企业科研课题
### author: fengye7

## 如何运行
1. anaconda环境准备好
2. conda create -n <环境名> python=3.8.20 **创建一个隔离的python环境**
3. pip install -r requirements.txt  **安装所有相关依赖**

## 如何协作
1. git clone <仓库地址>
2. git branch -a ：查看所有分支
3. git branch <分支name> : 创建分支（请创建自己的分支，在自己的分支上进行更改）
4. git checkout <分支name> : 切换到某一分支
5. git branch -d <分支name> : 不小心创建多余分支，进行删除
6. git push -u origin <自己的分支名>: -u表示设为默认
7. git pull origin main ： 每次工作前运行此命令确保同步主分支内容
8. 完成更改请到github仓库创建pull request