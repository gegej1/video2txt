# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 项目概述

video2txt - 视频转文本工具项目

---

## 开发约束

### 通用规范
1. **仅完成用户明确要求的任务，不擅自扩展范围**
2. 创建文件夹/服务前，**先检测是否已存在**，避免重复
3. 若发现 npm/node/包管理器缺失，请先检查其他目录是否已安装，再决定是否安装
4. **每接到新任务必须重新编写全局计划**，并在执行前通盘考虑
5. **每次生成代码都必须运行测试**；测试失败不得提交
6. 前端组件/Card **必须结构化设计 + 结构化调用**，使用 **React/JSX/Node.js** 等现代技术栈
7. 所有问答和注释均使用中文

---

## TDD 开发流程规范

### TDD 三步骤（红-绿-重构）

#### 🔴 红阶段：先写失败的测试
- 编写全面的测试用例，覆盖所有场景和边界条件
- 测试必须包含：正常流程、边界情况、异常处理
- 运行测试确认全部失败
- 提交测试代码

#### 🟢 绿阶段：编写最少代码让测试通过
- 严禁修改已提交的测试
- 只编写让测试通过的最小实现
- 运行测试确认全部通过
- 提交实现代码

#### 🔵 重构阶段：优化代码质量
- 保持测试不变的前提下重构
- 提升代码可读性和性能
- 每次重构后运行测试确保通过

### TDD 测试编写要求
- **边界测试**：空值、零值、负值、超大值
- **异常测试**：无效输入、错误状态、资源不足
- **集成测试**：多个功能组合使用场景
- **性能测试**：大数据量、并发操作

### TDD 提交规范
```bash
# 第一次提交：失败的测试
git add tests/
git commit -m "test: 添加功能TDD测试用例（预期失败）"

# 第二次提交：实现代码
git add src/
git commit -m "feat: 实现功能，通过所有TDD测试"
```

---

## 路径 & 版本号安全检查

1. **禁止**在运行时用 `fs.readFileSync()`/`existsSync()` 直接查找 `package.json`
   - ✅ **方案 A**：在 `tsconfig.json` 打开 `resolveJsonModule`：
     ```typescript
     import pkg from '../package.json';
     console.log('v' + pkg.version);
     ```
   - ✅ **方案 B（推荐）**：构建脚本注入 `APP_VERSION=$npm_package_version`，运行时代码仅读 `process.env.APP_VERSION`

2. 若必须读文件，请统一调用自定义工具 `resolveFromProjectRoot(relPath)`，兼容任意 `src`/`dist` 目录差异

3. 应用启动首行打印：
   ```typescript
   console.log('cwd=', process.cwd(), 'dirname=', __dirname);
   ```

4. CI/CD 中务必在**构建产物**上执行启动测试，如 `node dist/main.js`，确保生产环境可用

5. 当路径逻辑不确定时，应暂停生成并提示开发者人工确认，而不要猜测

---

## 约束作用范围

这些约束适用于以下文件类型：
- `**/*.ts`
- `**/*.tsx`
- `**/*.js`
- `**/*.jsx`
