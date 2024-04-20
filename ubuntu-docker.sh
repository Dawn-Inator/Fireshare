#!/bin/bash

# 更新APT包索引
apt-get update

# 安装必要的包
apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# 添加Docker的官方APT仓库的GPG密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# 自动确认添加Docker的官方APT仓库
add-apt-repository -y "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# 更新APT包索引以包含Docker的仓库
apt-get update

# 安装Docker CE
apt-get install -y docker-ce

# 添加docker用户组（如果尚未存在）
groupadd docker

# 将当前用户添加到docker组，这里使用root作为示例
usermod -aG docker $USER

# 启动Docker服务
systemctl start docker

# 使Docker服务开机自启
systemctl enable docker

# 下载指定版本的Docker Compose
curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 赋予Docker Compose执行权限
chmod +x /usr/local/bin/docker-compose


# 显示Docker和Docker Compose的版本，确认安装成功
docker version
docker-compose version
