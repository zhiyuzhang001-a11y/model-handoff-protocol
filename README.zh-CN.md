# 模型交接协议

这是一套可复用、证据优先的双向模型交接协议，用于在规划、实施和复核模型之间
切换，同时避免把聊天记录当成唯一的项目记忆。

它不绑定具体模型。默认让经济模型承担大部分边界明确的简单实施，让高级模型制定计划、
按风险要求的独立程度复核，并亲自处理少量判断密集、困难或高风险的代码；真正决定权限的仍是角色、
活动里程碑和交接合同，而不是模型名称。
新模型先读受预算约束的引导摘要，只在必要时展开精确的文件章节，避免项目越长每次
切换的输入越大。

## 核心流程

```text
规划/复核角色制定具体合同
          ↓
实施角色先核对上下文，再执行
          ↓
实施角色交回diff、测试证据和明确问题
          ↓
规划/复核角色按所需独立程度检查
          ↓
接受阶段 | 具体返工 | 请求决策 | 完成
          ↓
需要时继续循环
```

回交同样是强制流程：实施角色完成有边界的执行后，必须记录diff基线、任务自有/既有改动、
命令与退出码/数量/证据路径、失败、偏离、风险、清理状态和一个明确审查决定。
规划/复核角色再检查指定的diff和证据；是否需要独立上下文由风险决定。

## 安装到现有项目

在任意新项目里，可以直接对模型说：

```text
从 https://github.com/zhiyuzhang001-a11y/model-handoff-protocol 安装或更新
model-handoff-protocol，作为当前项目规则；按仓库的安全安装和升级说明执行。
```

高级模型可以根据这句话完成匿名下载、预览、安装和必要的人工合并。当前仓库是公开仓库，
首次安装不需要GitHub登录或Token。完整复制版、首次GitHub安装命令和安全说明见
[`docs/REMOTE_INSTALL.md`](docs/REMOTE_INSTALL.md)。
其中更明确的安全版提示词要求：先预览，绝不覆盖 differs 或 conflict，并保留项目实时状态。

先预览，不写文件：

```bash
python3 scripts/install.py /你的/项目路径
```

确认后只创建缺少的文件：

```bash
python3 scripts/install.py /你的/项目路径 --apply
```

安装器不会覆盖已有文件，也不会修改全局Codex、编辑器或Agent配置。
它会同时安装无依赖的`.model-handoff/handoff.py`检查器。
也会安装`.model-handoff/recover-review-selector.txt`，保存偶发二选一时的一句恢复指令。
还会安装`.model-handoff/CONTROL.md`，用于在不删除任何文件的情况下暂停或恢复协议。
还会安装`.model-handoff/update.py`；以后不必手工再次克隆，需要检查上游更新时只需运行：

```bash
python3 .model-handoff/update.py .
```

该命令只在你明确运行时联网，默认仍是预览，并显示实际获取的提交。需要固定版本时使用
`--ref <标签或提交>`。
对已有文件，预览会区分`identical`、`differs`和`conflict`，仍然不写入；升级时应人工合并
`differs`，以保留项目专属边界和实时状态。

切换前验证实时交接：

```bash
python3 .model-handoff/handoff.py check .
```

切换后先生成紧凑引导摘要：

```bash
python3 .model-handoff/handoff.py snapshot .
```

## 切换模型时怎么说

最简单用法只需要两句：

```text
切换前：我要切换模型。请按项目规则完成并检查交接，然后停止。
切换后：请按项目交接继续。
```

新模型会从交接中的`To role`自动判断是继续执行还是进行审查。

用户可以随时退出合同约束，无需卸载或删除文件：

```text
退出模型交接协议，保留文件。
```

以后要重新使用时只需说：

```text
恢复模型交接协议。
```

这两句只会把`.model-handoff/CONTROL.md`在`active`和`paused`之间切换。
`paused`时普通任务不执行交接合同，snapshot也不注入任务内容；恢复时先重新验证实时状态。

如果仍然偶发Bugbot/Security二选一，不要选1或2，只需发送：

```text
不要选择审查器。退出通用/review，读取项目交接snapshot，按Verification mode继续。
```

这是路由纠正，不是新任务；模型必须保留原合同。如果`EXECUTION_TO_VERIFY`的
模式缺失或损坏，确定性安全回退是`independent`，绝不猜测专项审查。

交接包会明确写入`Verification mode: self | independent | bugbot | security | none`。每个阶段都要
验收，但不一定切换模型：高级模型完成`thin`或`standard`工作、全部门禁通过且没有偏离、
边界变化或独立门禁时，用`self`在同一上下文轻量复核；经济模型产出、`high-risk`工作、
重大偏离或明确独立门禁使用`independent`，切换到独立高级模型或上下文。专项审查才使用
`bugbot`或`security`。普通阶段验收专门使用verification命名，与会弹出二选一的通用
`/review`技能分开。检查器会拒绝缺失或冲突的模式。

这里的“阶段”是共享同一范围、不变量和验收套件的完整执行批次，不是一个文件、测试或
计划小步骤。复核由批次验收边界触发，不由模型切换触发。同一个高级模型规划并完成普通
`thin/standard`批次时，只在当前上下文做一次集成式`self`收尾；不重新加载完整snapshot，
也不重复已有测试证据。只有经济模型产出、高风险、重大偏离、边界变化或明确独立要求才
切换到`independent`。

`python3 .model-handoff/handoff.py check .`只是交接合同检查：验证文件结构、状态/Git新鲜度
和路由一致性，不检查代码正确性，不证明测试，也不等于阶段复核、Bugbot或Security Review。
在实际交接、恢复协议或记录最终协议决定时运行即可，不应在每次编辑或测试后运行。

交接还会写入`Recommended capability: economical | capable`，由旧模型直接告诉你下一步
选择经济模型还是高级模型。`planner/verifier`必须使用`capable`；`implementer`默认选择
`economical`，判断密集的工作可选择`capable`；所有`high-risk`合同都必须选择`capable`
并明确记录覆盖矩阵。

从协议0.5或更早版本升级时，应同时合并规则、Playbook、模板和
`.model-handoff/handoff.py`，然后把实时`MODEL_HANDOFF.md`改为0.6。同时把
`planner/reviewer`改为`planner/verifier`、`Review mode`改为`Verification mode`、
`inline`改为`independent`，并更新两个执行/验收状态。检查器会拒绝部分升级。

切换前告诉旧模型：

```text
请按照项目的模型交接规则准备紧凑、只记录变化量的交接包。更新所属记录，指向精确证据，
运行交接检查，留下可恢复的Git状态，然后停止。
```

切换到实施模型：

```text
你现在承担implementer角色。先运行交接snapshot，只阅读其中标明必须展开的
精确文件章节。修改前核对合同，从唯一下一步开始，在未触发停止条件时完成整个批次。
```

切换到独立规划/复核模型：

```text
你现在承担planner/verifier角色。先运行交接snapshot，再按交接要求的独立程度检查Git diff和证据，
然后明确选择ACCEPT_STAGE、REFINE、BLOCKED_DECISION或COMPLETE。
如需返工，写出边界、验收、停止条件和唯一第一步。
```

完整可复制提示词位于[`prompts/`](prompts/)，详细流程见
[`docs/MODEL_HANDOFF_PLAYBOOK.md`](docs/MODEL_HANDOFF_PLAYBOOK.md)。
示例为了教学而刻意省略字段；真实交接必须从完整模板开始，不要直接复制示例。

## 规划详细度

默认由经济模型执行大多数简单、有边界、可逆且有测试保护的工作。高级模型负责固定
结果、不可变约束、验收、权限、停止条件和第一个可验证动作，按所需独立程度检查执行结果，并在
局部实现本身需要大量判断或风险较高时亲自写代码。无论哪个模型写代码，都临时承担
implementer角色并遵守同一合同。高级模型完成普通任务且全部门禁通过、没有偏离或边界
变化时可以同上下文`self`复核；高级模型写出的高风险代码始终由另一个高级模型或独立
上下文复核。

进入深度阶段后，默认不再按文件或小步骤频繁切换，而是建立一个“最大安全执行批次”：
经济模型一次完成共享同一范围、不变量和验收套件的多个实施、测试与局部修复，
整批通过后才交回高级模型。高级模型验收时发现的小型剩余问题可直接修复并重跑门禁；
系统性问题一次汇总成下一个修正批次，不逐条往返。如果交接解释和预计返工的成本已接近高级模型直接完成，
就应选择`capable-direct`，不为了使用经济模型而强行委派。

高风险行为修复必须覆盖所有适用的值、身份、路径、顺序、观察/发布、替换、失败和中断
维度，并用确定性测试控制时序。同一不变量在修复后第二次失败时，应停止继续打补丁，
回到高级模型重新做高风险计划和覆盖矩阵。

## 文件职责

- `.cursor/rules/`：稳定、始终生效的规则；不写动态进度。
- `MODEL_HANDOFF.md`：每次切换都更新的实时交接包。
- `STATUS.md`：项目当前状态和唯一下一步。
- `docs/IMPLEMENTATION_PLAN.md`：长期目标与里程碑。
- 活动里程碑计划/报告：冻结范围、验收标准和实际证据。
- `.model-handoff/handoff.py`：检查新鲜度和一致性，输出有上限的引导摘要。
- `.model-handoff/FEEDBACK.md`：只记录真实切换摩擦，不作为bootstrap输入。

## 本地持续改进

安装后无需反复下载。当交接出现缺失上下文、重复工作、过期指针、错误角色或输入过大时，
才向`.model-handoff/FEEDBACK.md`追加一条简短证据。先判断是否为项目特例：依赖该项目路径、
工具、产品行为或审批边界的修改留在原项目；可影响多个无关项目的问题才升级为通用
协议候选。

通用候选不应直接推送到GitHub `main`。应在本地协议源的新分支上脱敏重现，做最小修改、
增加回归测试并完整验证；候选分支可上传GitHub供备份和审查，通过后才合并`main`。
随后在原项目运行安装器预览，人工合并相关`differs`。只有后续真实切换证明改进有效时，
才将反馈标记为`RESOLVED`。项目专属规则、实时状态和未脱敏反馈始终不会被自动上传或覆盖。

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
