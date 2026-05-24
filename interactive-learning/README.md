# A Course in Time Series Analysis 交互学习实验室

这是一个面向本仓库中文讲义的静态交互学习站点原型。它把全书 15 章和 2 个附录组织成章节导航，每章提供一个可操作的动态实验，用滑块、开关和实时图形帮助读者理解核心概念。

当前页面同时面向本科生和研究生：

- 本科导学：强调概念定义、图形直觉、实验操作和常见误区。
- 研究生深化：强调模型假设、极限理论、估计推断和证明线索。
- 每章包含直觉入口、实验步骤、数学锚点、观察任务、易错提醒和讨论延伸。
- 每章提供 3 个可切换的交互演示，全书当前共 51 个演示。
- 学习焦点支持“预习概念、实验探究、理论推导、复习自测”四种课堂使用方式。
- 每章包含一题课堂自测，可手动显示或隐藏参考答案。

## 本地打开

直接在浏览器中打开：

```text
interactive-learning/index.html
```

也可以用任意静态服务器托管：

```powershell
python -m http.server 8000
```

然后访问：

```text
http://localhost:8000/interactive-learning/
```

## 部署到 GitHub Pages

1. 把仓库推送到 GitHub。
2. 在仓库 Settings → Pages 中选择部署分支。
3. 访问 `https://用户名.github.io/仓库名/interactive-learning/`。

## 后续扩展方式

- 在 `app.js` 的 `chapters` 数组中为章节追加 `demos`。
- 每个 demo 可以指定 `kind`、参数名、默认值、公式和观察任务。
- 批量扩展演示时，可以在 `demoExtensions` 中按章节追加更多演示。
- 在 `chapterEnrichment` 中补充每章的本科/研究生分层学习内容。
- 在 `quizBank` 中维护每章的课堂自测题和参考答案。
- 若要把 Python 脚本生成的数据接入页面，可以把结果导出为 JSON，再在静态站点中读取或直接嵌入。
