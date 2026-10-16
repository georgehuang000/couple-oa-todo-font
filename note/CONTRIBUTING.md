# 修改与贡献

发现缺字、少点画、粘连、字距异常时，请在 Issue 中附上具体文字、字体版本、软件与字号。字符表收录的是通用规范汉字表的 8105 字，不承诺全部繁体字或全部 Unicode 字符。

字体母版在 `source/font.ttx` 及它引用的分表／逐字 TTX 文件中。这是可编辑的 fontTools XML；`glyf` 存储轮廓，`hmtx` 存储字距，`cmap` 存储 Unicode 映射。也可把 TTF 导入支持 TrueType 的字体编辑器，再导出更新后的 TTX。TTX 构建不需要神经网络或原项目。

```sh
python -m venv .venv
# 激活虚拟环境后：
python -m pip install -r requirements.txt
python tools/build.py
python tools/verify.py --fonts build/fonts
python tools/export-svg.py 常 --output build/chang.svg
```

SVG 导出用于检查或矢量编辑，不会自动写回字体。改完轮廓需要更新对应 TTX；发布前也要检查 24px、32px、48px 的实际排版。

既有 735 字的签名是防止误改的基线。如果有意修复其中一个字，应在 PR 中说明原因、附前后图，并在确认后更新 `qa/original-glyph-digests.json`。不要为了让检查通过直接批量更新签名。

修改字库后运行构建，把验收后的字体更新到 `fonts/`，更新版本号、`FONTLOG.md` 和 `qa/release.json`。原始字形的版权、Adobe 上游声明与 OFL 许可须保留。字体贡献按 OFL 1.1；独立工具贡献按 MIT。请只提交自己有权贡献的内容。
