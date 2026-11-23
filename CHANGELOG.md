# Changelog

## [2.1.1](https://github.com/zarmstrong/autoshift/compare/v2.1.0...v2.1.1) (2026-11-23)


### Bug Fixes

* **deps:** bump runtime, dev, and CI dependencies ([#37](https://github.com/zarmstrong/autoshift/issues/37)) ([4972352](https://github.com/zarmstrong/autoshift/commit/49723526d7d52d51bb01e86286032e3bcac6fe9f))

## [2.1.0](https://github.com/zarmstrong/autoshift/compare/v2.0.3...v2.1.0) (2026-11-18)


### Features

* **python:** require Python 3.11 or newer ([7c0c42f](https://github.com/zarmstrong/autoshift/commit/7c0c42f412bd1d2ba12a5256cf7b590123b02392))


### Bug Fixes

* re-login on expired SHiFT session and stop marking codes invalid on 5xx ([#29](https://github.com/zarmstrong/autoshift/issues/29)) ([a7c63cc](https://github.com/zarmstrong/autoshift/commit/a7c63cc4664f6c21e6d7525edce8fbc623dc8193))


### Documentation

* **changelog:** remove duplicate merge-commit entries ([#28](https://github.com/zarmstrong/autoshift/issues/28)) ([741cb79](https://github.com/zarmstrong/autoshift/commit/741cb79a778f6169a15b9f008ea622b00b1fc607))

## [2.0.3](https://github.com/zarmstrong/autoshift/compare/v2.0.2...v2.0.3) (2026-11-18)


### Bug Fixes

* **deps:** bump apprise from 1.12.0 to 2.2.0 ([0aa27ac](https://github.com/zarmstrong/autoshift/commit/0aa27ac41d5474e8312181cb2e73830bcb15689b))
* **deps:** bump requests from 2.28.0 to 2.32.5 ([6e8d764](https://github.com/zarmstrong/autoshift/commit/6e8d764a8175bfb4b256118d58273c3186ee4c5d))
* **deps:** bump the pypi group with 3 updates ([f18f686](https://github.com/zarmstrong/autoshift/commit/f18f686edd6518b6bae4f0b19edd2071e80114db))
* **docker:** follow-ups to [#17](https://github.com/zarmstrong/autoshift/issues/17) (disable globbing, retry wrongly redeemed codes) ([#24](https://github.com/zarmstrong/autoshift/issues/24)) ([93224b9](https://github.com/zarmstrong/autoshift/commit/93224b931172417b36fb1c9ee14fcc7021c81270))
* **docker:** word-split SHIFT_REDEEM, SHIFT_GAMES and SHIFT_PLATFORMS ([8b4fb48](https://github.com/zarmstrong/autoshift/commit/8b4fb4820ed7c4002587d560ca0c3787d336c520))
* **shift:** send a browser User-Agent to SHiFT ([de0a522](https://github.com/zarmstrong/autoshift/commit/de0a522aa7c56b32e459b2c924bba2b7f3649388))

## [2.0.2](https://github.com/zarmstrong/autoshift/compare/v2.0.1...v2.0.2) (2026-07-14)


### Bug Fixes

* compute banner width using both lines and txt to prevent misaligned title ([3969cc9](https://github.com/zarmstrong/autoshift/commit/3969cc969b54a2833f8cd1f468be3f83b5307fba))
* update project author attribution ([1cc9c69](https://github.com/zarmstrong/autoshift/commit/1cc9c69b45099f6b24385c5a1c2a9cba3d664884))

## [2.0.1](https://github.com/zarmstrong/autoshift/compare/v2.0.0...v2.0.1) (2026-07-14)


### Documentation

* use pinned pre-commit lint tooling ([1d7a514](https://github.com/zarmstrong/autoshift/commit/1d7a5148d11a2e2680ff9295e06a97e67a386445))
