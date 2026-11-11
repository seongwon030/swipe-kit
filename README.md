<p align="center"><img src="docs/images/banner.png" alt="swipe-kit" width="100%"></p>

<p align="center"><b>A Claude skill that turns a product description into an Instagram carousel.</b><br><a href="README.ko.md">한국어</a> · English</p>

The design is locked; Claude only plans the deck and writes the copy. Every carousel looks like the same feed.

<p align="center"><img src="docs/images/hero.png" alt="Example carousel" width="100%"></p>

## Install

```bash
# Claude Code
git clone https://github.com/seongwon030/swipe-kit
cp -r swipe-kit/skills/swipe-kit ~/.claude/skills/

# rendering dependencies
pip install playwright pillow && playwright install chromium
```

In the Claude app, upload `swipe-kit.skill` from [Releases](../../releases) in your skill settings.

## Use

> Make an Instagram carousel for Brewly, a coffee subscription. First bag free, brand color #E4572E.

You get 1080×1350 PNGs, a preview and a caption.

<p align="center"><img src="docs/images/types-1.png" alt="cover, problem, feature" width="100%"><img src="docs/images/types-2.png" alt="steps, point, cta" width="100%"></p>

## License

MIT · bundled fonts under SIL OFL 1.1 · all example brands are fictional
