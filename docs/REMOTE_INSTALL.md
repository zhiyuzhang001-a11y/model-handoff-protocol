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

A capable project model with repository access should use an authenticated
temporary clone, inspect the preview, and report any manual merge before changing
an existing file. If access is unavailable, it must report that fact without
requesting or exposing a token in chat.

## First installation from GitHub

The repository is currently private, so anonymous `raw.githubusercontent.com`
downloads return 404. Use the machine's existing Git or GitHub CLI credentials;
never paste a token into the project prompt. From the target project, fetch a
temporary source clone and run its installer. Preview is the default:

```bash
protocol_source="$(mktemp -d -t model-handoff-source)"
git clone --depth 1 \
  https://github.com/zhiyuzhang001-a11y/model-handoff-protocol.git \
  "$protocol_source"
python3 "$protocol_source/scripts/install.py" .
python3 "$protocol_source/scripts/install.py" . --apply
```

The model should remove its temporary source clone after the installation reaches
a recoverable state. It may use `gh repo clone` instead when the GitHub CLI owns
the authenticated session.

Installation also creates `.model-handoff/update.py`, so later checks do not need
another manual clone:

```bash
python3 .model-handoff/update.py .
```

That helper uses Git without a shell, disables credential prompts, fetches the
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
