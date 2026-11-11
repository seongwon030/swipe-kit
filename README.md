<p align="center"><img src="docs/images/banner.png" alt="swipe-kit" width="100%"></p>

<p align="center"><b>제품 설명만 주면 Claude가 인스타 캐러셀을 기획하고 PNG로 뽑아주는 스킬</b><br>한국어 · <a href="README.en.md">English</a></p>

디자인은 고정, Claude는 기획과 문구만. 몇 번을 만들어도 같은 피드처럼 보여요.

<p align="center"><img src="docs/images/hero.png" alt="예시 캐러셀" width="100%"></p>

## 설치

```bash
# Claude Code
git clone https://github.com/seongwon030/swipe-kit
cp -r swipe-kit/skills/swipe-kit ~/.claude/skills/

# 렌더링 의존성
pip install playwright pillow && playwright install chromium
```

Claude 앱에서는 [Releases](../../releases)의 `swipe-kit.skill`을 스킬 설정에서 업로드하세요.

## 사용

> 커피 구독 서비스 Brewly 홍보 캐러셀 만들어줘. 첫 봉지 무료, 브랜드 컬러 #E4572E.

1080×1350 PNG, 미리보기, 캡션이 나와요. 영어로 요청하면 영어로 써요.

<p align="center"><img src="docs/images/types-1.png" alt="cover, problem, feature" width="100%"><img src="docs/images/types-2.png" alt="steps, point, cta" width="100%"></p>

## License

MIT · 번들 폰트는 SIL OFL 1.1 · 예시 브랜드는 모두 가상
