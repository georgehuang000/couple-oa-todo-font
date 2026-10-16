# 便签手记 8105

**Couple OA Note 8105** 是一款用于便签、寄语和小纸条的细笔手写字体。它保留真实文本，安装后可以在设计软件中直接改文案、字号与颜色。

与「两人待办手写体」在[同一个字体项目](https://github.com/georgehuang000/couple-oa-todo-font)中维护。

[在线试字](https://georgehuang000.github.io/couple-oa-todo-font/note/) · [下载字体与源码包](https://github.com/georgehuang000/couple-oa-todo-font/releases/tag/note-v2.100) · [English](README.en.md) · [OFL 1.1](OFL.txt) · [来源说明](PROVENANCE.md)

![便签手记实际字体样张](assets/specimen.png)

## 覆盖

- 《通用规范汉字表》全部 **8105 个汉字**，含 196 个非 BMP 字符。
- 英文大小写、数字、常用标点与空格，共 **8234 个字符**。
- 一个 Regular 字重，提供 **TTF** 安装字体和 **WOFF** 网页字体。
- 原有 735 个字符保持轮廓和字距，包括修正后的小写 e、“常”“美”“可”。

这是通用简体字库，不涵盖所有繁体、异体字、Emoji 或全部 Unicode。建议便签短句从 24–40px 试排，复杂字可从 32px 起试；细笔字在小字号下会较轻。

## 使用

1. 下载 Release 的 `Use.zip`，解压后安装 `fonts/CoupleOANote8105-Regular.ttf`。
2. 在支持本地字体的软件中选择 **Couple OA Note 8105**，输入自己的文字。
3. 打开包内 `index.html` 可离线试字、检查覆盖并搜索 8105 字表，字体已内嵌。

网页可以引用包内 `font.css`：

```html
<link rel="stylesheet" href="font.css">
<p class="couple-note">今天也有值得记录的小事。</p>
```

完整 WOFF 约 4 MB，适合在便签功能内按需加载。超出字库范围的字符需要回退字体，试字页会明确标示。

## 可修改的源码

克隆整个项目后先进入 `note/`；单独下载 Source ZIP 时直接在解压目录运行下列命令。

`source/font.ttx` 及其引用的逐字文件包含轮廓、字距和 Unicode 映射。安装 Python 3.10 或更新版本及依赖后：

```sh
python -m pip install -r requirements.txt
python tools/build.py
python tools/verify.py --fonts build/fonts --compare-release
```

字体输出到 `build/fonts/`。重建不需要模型、Windows 字体或原应用项目；安装依赖后可离线执行。TTF 按摘要核对，WOFF 逐字轮廓与字体信息也会核对；不同 zlib 版本的压缩字节可能不同。

修改方法见 [CONTRIBUTING.md](CONTRIBUTING.md)。字形反馈请说明具体字符、版本、软件与字号。

## 版本与来源

公开版本 **2.100** 保留原始便签字形，将 7499 个扩展字的内容条件改为 OFL 的思源宋体后重新生成。因此它与早期内部 v2.000 的扩展字形存在差异。生成风格参考仍来自项目自身的便签字。

来源、AI 辅助生成过程和第三方工具说明见 [PROVENANCE.md](PROVENANCE.md)。检查记录见 [qa/review.json](qa/review.json) 和 [qa/engineering.json](qa/engineering.json)；字符覆盖与工程检查不等于每一笔都绝对无误。

## 许可

字体和字形母版采用 **SIL Open Font License 1.1**：允许商用、嵌入、修改和再分发；分发需保留版权与许可证，修改版字体继续采用 OFL，字体本身不能单独出售。使用字体排版的设计作品不需要按 OFL 开源。完整条件以 [OFL.txt](OFL.txt) 为准。

独立构建及验证工具采用 [MIT](LICENSE-CODE)。Unicode 数据及思源宋体的上游许可保留在 `licenses/`；字体许可与工具许可分别适用。

维护者：[georgehuang000](https://github.com/georgehuang000)。感谢 Adobe 思源宋体、Unicode、MX-Font、Potrace 与 fontTools 项目。
