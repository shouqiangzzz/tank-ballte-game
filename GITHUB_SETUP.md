# 将项目关联到 GitHub 仓库

## 步骤 1: 配置 Git 用户信息（如果还没有配置）

在命令行中运行以下命令，替换为你的实际信息：

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

或者只为当前仓库配置（不使用 --global）：

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## 步骤 2: 在 GitHub 上创建新仓库

1. 登录 GitHub (https://github.com)
2. 点击右上角的 "+" 号，选择 "New repository"
3. 填写仓库名称（例如：tank-battle-game）
4. 选择是否公开（Public）或私有（Private）
5. **不要**初始化 README、.gitignore 或 license（因为本地已有文件）
6. 点击 "Create repository"

## 步骤 3: 关联本地仓库到 GitHub

在 GitHub 创建仓库后，你会看到一个页面，显示如何关联现有仓库。运行以下命令：

```bash
# 添加远程仓库（将 YOUR_USERNAME 和 REPOSITORY_NAME 替换为你的实际信息）
git remote add origin https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git

# 或者使用 SSH（如果你配置了 SSH 密钥）
# git remote add origin git@github.com:YOUR_USERNAME/REPOSITORY_NAME.git
```

## 步骤 4: 提交代码并推送到 GitHub

```bash
# 创建初始提交（如果还没有提交）
git add .
git commit -m "Initial commit: 坦克大战游戏"

# 将代码推送到 GitHub
git branch -M main  # 将分支重命名为 main（GitHub 默认分支）
git push -u origin main
```

## 步骤 5: 验证

在浏览器中刷新你的 GitHub 仓库页面，你应该能看到所有文件都已经上传。

## 后续更新代码

当你修改代码后，使用以下命令更新 GitHub：

```bash
git add .
git commit -m "描述你的更改"
git push
```

## 常见问题

### 如果遇到认证问题

GitHub 现在要求使用个人访问令牌（Personal Access Token）而不是密码：

1. 在 GitHub 设置中创建个人访问令牌：
   - Settings → Developer settings → Personal access tokens → Tokens (classic)
   - 点击 "Generate new token"
   - 选择适当的权限（至少需要 repo 权限）
   - 复制生成的令牌

2. 推送时使用令牌作为密码，用户名为你的 GitHub 用户名

### 如果想使用 SSH（推荐）

1. 生成 SSH 密钥：
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```

2. 将公钥添加到 GitHub：
   - 复制 `~/.ssh/id_ed25519.pub` 的内容
   - GitHub → Settings → SSH and GPG keys → New SSH key

3. 使用 SSH URL 添加远程仓库：
   ```bash
   git remote set-url origin git@github.com:YOUR_USERNAME/REPOSITORY_NAME.git
   ```

