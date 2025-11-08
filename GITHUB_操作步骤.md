# GitHub 仓库设置步骤

## ✅ 已完成的步骤

1. ✅ Git 用户信息已配置：
   - 用户名：shouqiangzzz
   - 邮箱：shouqiangzzz@gmail.com

2. ✅ Git 仓库已初始化
3. ✅ 代码已提交到本地仓库
4. ✅ 远程仓库地址已配置：https://github.com/shouqiangzzz/tank-ballte-game.git

## 📋 接下来需要你手动完成的步骤

### 步骤 1: 在 GitHub 上创建仓库

1. 访问 https://github.com/shouqiangzzz
2. 点击右上角的 "+" 号，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `tank-ballte-game`
   - **Description**: （可选）坦克大战游戏
   - **Visibility**: 选择 Public（公开）或 Private（私有）
   - ⚠️ **重要**：不要勾选以下选项：
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license
   （因为本地已有这些文件）
4. 点击 "Create repository" 按钮

### 步骤 2: 推送代码到 GitHub

创建仓库后，在终端运行以下命令：

```bash
git push -u origin main
```

### 步骤 3: 如果遇到认证问题

如果提示需要输入用户名和密码：

1. **用户名**：输入 `shouqiangzzz`
2. **密码**：需要输入 GitHub 的**个人访问令牌（Personal Access Token）**，而不是你的 GitHub 密码

#### 如何创建个人访问令牌：

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 填写信息：
   - **Note**: 可以填写 "Git Push Token"
   - **Expiration**: 选择过期时间（建议 90 天或自定义）
   - **Select scopes**: 至少勾选 `repo` 权限
4. 点击 "Generate token"
5. **重要**：复制生成的令牌（只显示一次，请保存好）
6. 在推送时，密码处粘贴这个令牌

### 步骤 4: 验证

推送成功后，访问以下地址查看你的仓库：
https://github.com/shouqiangzzz/tank-ballte-game

## 🔄 如果推送失败

如果遇到连接问题，可以尝试：

1. **检查网络连接**
2. **重试推送**：
   ```bash
   git push -u origin main
   ```
3. **如果还是失败**，可以尝试使用 SSH（需要先配置 SSH 密钥）

## 📝 后续更新代码

当你修改代码后，使用以下命令更新 GitHub：

```bash
git add .
git commit -m "描述你的更改"
git push
```

---

**提示**：如果仓库名拼写有误（tank-ballte-game），可以在 GitHub 创建时使用正确的名称，然后更新本地远程仓库地址：
```bash
git remote set-url origin https://github.com/shouqiangzzz/正确的仓库名.git
```

