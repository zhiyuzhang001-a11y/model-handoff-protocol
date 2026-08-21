# 模型交接协议

这是一套可复用、证据优先的双向模型交接协议，用于在规划、实施和复核模型之间
切换，同时避免把聊天记录当成唯一的项目记忆。

它不绑定具体模型。你可以让能力更强的模型承担规划和最终复核，让成本较低的模型
执行边界明确的任务；真正决定权限的是角色、活动里程碑和交接合同，而不是模型名称。

## 核心流程

```text
规划/复核角色制定具体合同
          ↓
实施角色先核对上下文，再执行
          ↓
实施角色交回diff、测试证据和明确问题
          ↓
规划/复核角色独立检查
          ↓
接受阶段 | 具体返工 | 请求决策 | 完成
          ↓
需要时继续循环
```

## 安装到现有项目

先预览，不写文件：

```bash
python3 scripts/install.py /你的/项目路径
```

确认后只创建缺少的文件：

```bash
python3 scripts/install.py /你的/项目路径 --apply
```

安装器不会覆盖已有文件，也不会修改全局Codex、编辑器或Agent配置。

## 切换模型时怎么说

切换前告诉旧模型：

```text
请按照项目的模型交接规则准备完整交接包。更新实时交接单、状态、活动计划和
报告，记录唯一下一步、Git/测试证据、风险、停止条件及仍在运行的资源，然后停止。
```

切换到实施模型：

```text
你现在承担implementer角色。阅读项目规则、MODEL_HANDOFF.md、STATUS.md、
IMPLEMENTATION_PLAN.md、活动里程碑、最近报告和Git状态。修改前先核对合同，
无重大冲突后只执行交接单中的唯一下一步。
```

切换到规划/复核模型：

```text
你现在承担planner/reviewer角色。阅读规则和完整交接，独立检查Git、diff和测试
证据，然后明确选择ACCEPT_STAGE、REFINE、BLOCKED_DECISION或COMPLETE。
如需返工，写出边界、验收、停止条件和唯一第一步。
```

完整可复制提示词位于[`prompts/`](prompts/)，详细流程见
[`docs/MODEL_HANDOFF_PLAYBOOK.md`](docs/MODEL_HANDOFF_PLAYBOOK.md)。

## 文件职责

- `.cursor/rules/`：稳定、始终生效的规则；不写动态进度。
- `MODEL_HANDOFF.md`：每次切换都更新的实时交接包。
- `STATUS.md`：项目当前状态和唯一下一步。
- `docs/IMPLEMENTATION_PLAN.md`：长期目标与里程碑。
- 活动里程碑计划/报告：冻结范围、验收标准和实际证据。

## 隐私

GitHub仓库中应保存空白模板和虚构示例，不应直接公开真实项目的实时交接单。
发布前检查本地路径、用户名、私有仓库名、提交号、日志、客户信息、令牌、内部URL、
进程信息和未发布架构决策。

## 验证

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

公开前可以临时加入项目专属禁止词，而不把私有名称写进本仓库：

```bash
MHP_FORBIDDEN_TERMS='内部项目名,账户名' python3 scripts/validate.py
```

本项目采用Apache License 2.0。
