# Remotion video

<p align="center">
  <a href="https://github.com/remotion-dev/logo">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://github.com/remotion-dev/logo/raw/main/animated-logo-banner-dark.apng">
      <img alt="Animated Remotion Logo" src="https://github.com/remotion-dev/logo/raw/main/animated-logo-banner-light.gif">
    </picture>
  </a>
</p>

Welcome to your Remotion project!

## Commands

**Install Dependencies**

```console
npm i
```

**Start Preview**

```console
npm run dev
```

**Render video**

```console
npx remotion render
```

**Upgrade Remotion**

```console
npx remotion upgrade
```

## Docs

Get started with Remotion by reading the [fundamentals page](https://www.remotion.dev/docs/the-fundamentals).

## Help

We provide help on our [Discord server](https://discord.gg/6VzzNDwUwV).

## Issues

Found an issue with Remotion? [File an issue here](https://github.com/remotion-dev/remotion/issues/new).

## License

Note that for some entities a company license is needed. [Read the terms here](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md).

---

# AIショート動画ファクトリー(2026-07 追加)

このリポジトリには上記Remotionプロジェクトに加えて、AIショート動画事業の**組織・知識・制作パイプライン一式**が入っています。

- **全体像はまず [docs/PROJECT-OVERVIEW.md](docs/PROJECT-OVERVIEW.md) を読む**
- `.company/` — 仮想組織(意思決定ログ・調査レポート・チャンネル企画)
- `docs/` — 環境構築手順・プロンプト知見
- `pipeline/` — 動画組み立てスクリプト(Python)+生成ジョブテンプレ

別マシンで再開する場合: `docs/setup-local-pipeline.md` の手順でComfyUI+Wanを構築し、Claude Code でこのリポジトリを開けば、.company/ の文脈から秘書が続きを引き継げます。
