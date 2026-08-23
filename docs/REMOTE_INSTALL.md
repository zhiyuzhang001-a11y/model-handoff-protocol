# Remote installation and updates

## One-sentence request for a project model

Usually, give a capable model in the target project only this instruction:

> Install or update `model-handoff-protocol` from
> `https://github.com/zhiyuzhang001-a11y/model-handoff-protocol` as this project's
> rules, following the repository's safe installation and upgrade procedure.

The shortest Chinese instruction is:

> 从 `https://github.com/zhiyuzhang001-a11y/model-handoff-protocol` 安装或更新
> `model-handoff-protocol`，作为当前项目规则；按仓库的安全安装和升级说明执行。

If the target model may act too mechanically, use this explicit safety contract:

> Fetch or update the Model Handoff Protocol from
> `https://github.com/zhiyuzhang001-a11y/model-handoff-protocol`. Preview it
> against the current project first. Install missing files, never overwrite
> `differs` or `conflict`, and merge only protocol-generic changes while
> preserving project-specific rules and live state. Validate the handoff setup
> when finished.

Its Chinese equivalent is:

> 从 `https://github.com/zhiyuzhang001-a11y/model-handoff-protocol` 下载或更新模型交接协议，
> 作为当前项目规则。先预览；只安装缺失文件，绝不覆盖 `differs` 或 `conflict`；更新时只合并
> 协议通用变化，保留本项目规则、实时状态和定制。完成后验证交接配置。

A capable project model should use the public bootstrap or a temporary clone,
inspect the preview, and report any manual merge before changing an existing
file.

## First installation from GitHub

The repository is public. Download the small bootstrap script without credentials,
inspect it when the source is not already trusted, and run it from the target
project. Preview is the default:

```bash
curl -fsSLo /tmp/model-handoff-bootstrap.py \
  https://raw.githubusercontent.com/zhiyuzhang001-a11y/model-handoff-protocol/main/scripts/bootstrap.py
python3 /tmp/model-handoff-bootstrap.py .
python3 /tmp/model-handoff-bootstrap.py . --apply
```

The bootstrap uses Git without a shell, fetches one revision into a temporary
directory, prints the exact commit, and delegates to the repository installer.
Use `--ref <tag-or-commit>` when a reproducible pinned source is required. A
temporary `git clone --depth 1` remains an equivalent fallback.

Installation also creates `.model-handoff/update.py`, so later checks do not need
another manual clone:

```bash
python3 .model-handoff/update.py .
```

That helper uses Git without a shell or interactive credentials, fetches the
latest `main` into a temporary directory, prints the exact commit, and previews
it. Add `--apply` only to create newly introduced missing files. Existing `differs` remain untouched
for manual review and merge. Use `--ref
<tag-or-commit>` when a reproducible pinned source is required.

## Why updates do not overwrite

Some installed files become project-owned immediately: `STATUS.md`,
`MODEL_HANDOFF.md`, the implementation plan, feedback, and often local rule
customizations. A remote updater cannot safely distinguish every intentional
project change from an obsolete protocol copy. The installer therefore treats
`differs` as a review request rather than an overwrite authorization.

This keeps installation simple without making updates destructive. The model can
compare the fetched source with each reported `differs`, carry over only generic
protocol changes, run `.model-handoff/handoff.py check .`, and leave private live
state in the target repository.
