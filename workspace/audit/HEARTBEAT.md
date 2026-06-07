# HEARTBEAT.md - 周期性自检

_周期性检查本 agent 健康状态。_

## 检查项

- [ ] SOUL.md / AGENTS.md / IDENTITY.md / USER.md / TOOLS.md / MEMORY.md 是否齐全
- [ ] skills/ 目录下的 SKILL.md 是否与父工作区版本一致
- [ ] 是否有未处理的 process 记录
- [ ] 是否有需要写入 MEMORY.md 的新经验

## 自检时间

- 每次 session 启动
- 每次完成审计任务后

## 异常处理

- 工作区文件缺失：参照父工作区结构补齐
- skill 文件漂移：以本工作区为准（单一职责版本）
- 长期无任务：维持现状，等待 main agent 委派
