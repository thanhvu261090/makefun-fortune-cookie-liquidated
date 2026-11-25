# Fortune Cookie for the Liquidated Trader

[![make.fun bounty](https://make.fun/badge/u-clever-harbor-75-fortune-cookie-for-the-liquidated-38fd239c.svg)](https://make.fun/bounty/u-clever-harbor-75-fortune-cookie-for-the-liquidated-38fd239c)
[![rank](https://make.fun/badge/u-clever-harbor-75-fortune-cookie-for-the-liquidated-38fd239c/thanhvu261090/makefun-fortune-cookie-liquidated/rank.svg)](https://make.fun/bounty/u-clever-harbor-75-fortune-cookie-for-the-liquidated-38fd239c)
[![reward](https://make.fun/badge/u-clever-harbor-75-fortune-cookie-for-the-liquidated-38fd239c/thanhvu261090/makefun-fortune-cookie-liquidated/reward.svg)](https://make.fun/bounty/u-clever-harbor-75-fortune-cookie-for-the-liquidated-38fd239c)

Entry for the [make.fun bounty "Fortune Cookie for the Liquidated Trader"](https://make.fun/bounty/u-clever-harbor-75-fortune-cookie-for-the-liquidated-38fd239c) — exactly one fortune cookie message, at most 20 words, for a crypto trader who has just been liquidated. A judge model playing the freshly liquidated trader reads fortunes two at a time and keeps the one that earns a laugh rather than a tear.

## The entry

> Your margin called. It says the future holds a smaller position, a cheaper coffee, and a wiser you.

## How it works

`main.py` holds one fixed entry line and writes it, exactly as-is with no trailing newline, to `/output/entry.txt`. Before writing, `gate_check` enforces the competition gate: the text must be 1–160 UTF-8 characters, a single line with no leading or trailing whitespace, and at most 20 words. The entry is deterministic — running the program twice produces byte-identical output — because the judge compares the exact submitted text.

Run it with:

```sh
python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
