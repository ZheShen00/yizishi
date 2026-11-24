要改，一共 3 处：测试 2 处、门禁 1 处。门禁那处别顺手换成「请勿关闭页面」，第 1 行注释里就有这六个字，字面量真删了门禁照样绿。

## 现在为什么红

在仓库里跑查锚：

```
$ python C:/Users/shenz/Desktop/yizishi/scripts/check_copy_anchors.py --base HEAD
BREAK  smoke/gate.sh:3  「关闭页面会中断」
BREAK  tests/banner.test.ts:3  「关闭页面会中断」
VACUOUS  tests/banner.test.ts:6  「仍在同步」
```

三处锚挂的都是你删掉的那半句：

- 测试第 3 行：锚没了，`toContain("关闭页面会中断")` 直接失败。
- 门禁第 3 行：`grep -qF '关闭页面会中断' src/banner.ts` 匹配不到，退出 1，门禁红。
- 测试第 6 行：`not.toContain("仍在同步")` 里那句全站都不出现了，这条断言从此永远通过，守不住「同步完横幅消失」。它守的不是「旧写法不许回来」，是新旧说法换了措辞，所以必须改，不能留。

## 三处改法

**1. tests/banner.test.ts:3**

```diff
-  expect(syncBanner(false)).toContain("关闭页面会中断");
+  expect(syncBanner(false)).toContain("请勿关闭页面");
```

锚换成新句里意思相同的片段，6 个字，在新句里唯一；测试名「没同步完 → 提醒别关页面」不用动。

**2. tests/banner.test.ts:6**

```diff
-  expect(syncBanner(true)).not.toContain("仍在同步");
+  expect(syncBanner(true)).toBe("");
```

能断精确值就别用反向断言，以后再改文案这条也不会跟着烂。退一步写成 `.not.toContain("同步中")` 也能过，但下次换说法又失效一次。

**3. smoke/gate.sh:3**

```diff
- grep -qF '关闭页面会中断' src/banner.ts || { echo "FAIL 关页提醒不在了"; exit 1; }
+ grep -qE '"[^"]*请勿关闭页面[^"]*"' src/banner.ts || { echo "FAIL 关页提醒不在了"; exit 1; }
```

## 门禁这处为什么必须限定在字面量里

第 1 行注释是「同步横幅：没同步完时提醒「请勿关闭页面」，关了会中断同步」，已经含这六个字。拿它当锚会出这种事：

- 现文件：裸词命中 2 行（第 1 行注释、第 3 行字符串），限定成 `"[^"]*请勿关闭页面[^"]*"` 后命中 1 行。
- 把第 3 行字面量换成别的句子再试：裸词照样退出 0（门禁假绿），限定字面量的版本退出 1（门禁变红，正确）。

## 验证结果

都在临时副本上跑的，没动你的仓库。

- 改前：2 条 BREAK、1 条 VACUOUS，退出码 1。
- 改后：0 条锚会断、0 条反向断言会失效，退出码 0。
- 门禁旧锚：`git grep -qF '关闭页面会中断'` 退出 1，现在是红的；新锚退出 0，`git grep -cE` 计 1 行。
- 单测：仓库里没有 package.json，jest 起不来，没法原样跑；用 node 直接调 `syncBanner` 验了两条断言，返回值 `"同步中，请勿关闭页面"` 和 `""`，都过。
- Windows 上没有 bash，`grep -qF`、`grep -qE` 是用 git 自带的那份 grep 等价跑的。

## 刻意没改的

- `src/banner.ts` 的文案本身：你定的，我不动。
- 测试名、门禁的 FAIL 提示、注释第 1 行。

## 两件要你定的

1. 文案还要不要带上后果。新句没说「关了会中断同步」，短是短了，但用户不知道为什么不能关。要保留的话最省是「同步中，关闭页面会中断同步」。这条得现在定：定了再改锚，别改完锚又改文案，锚还得再动一遍。
2. 锚的颗粒度。上面按「请勿关闭页面」写；如果你决定把后果加回去，门禁和测试改成锚「关闭页面」更省，两种写法里都有这四个字（实测现在命中 1 行，换成带后果的写法也仍命中）。

顺带一句：仓库里没有 `docs/copy-glossary.md`，`detect_industry.py` 也没识别出行业信号，这次按通用规则处理，不影响上面的改法。

要不要我直接把这三处改了，再跑一遍查锚和门禁？
