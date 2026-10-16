# 字形与工具来源

## 原始便签字形

606 个汉字和 129 个英文、数字、标点与空白字符来自本项目的便签字稿、AI 绘制与轮廓整理。项目发起者确认最初参考设计为本人／项目原创或 AI 生成。小写 e、常、美、可等字经过单独修正。

开源版保留这 735 个字符的轮廓和字距。`qa/original-glyph-digests.json` 记录冻结基线；它是回归检查，不是对字形质量的评分。

## 8105 字扩展

新增 7499 个汉字使用 [MX-Font 官方实现](https://github.com/clovaai/mxfont) 和项目自身的 64 个便签风格参考生成，随后转换、排版并检查。三笔的“士”使用项目直接绘制的矢量母版。

公开版的全部内容条件重新来自 **思源宋体 SC Regular 2.003**：

- 项目：[adobe-fonts/source-han-serif](https://github.com/adobe-fonts/source-han-serif)
- 固定提交：`7889f11bf31170b5d092a083b357c8c8130f89e0`
- 原文件：`OTF/SimplifiedChinese/SourceHanSerifSC-Regular.otf`
- SHA-256：`78aa7a328fd974df2d688c8a9fd74a33d8334dfa84ab24d9d11efb2ffc464117`
- 上游许可：SIL OFL 1.1，原文保留在 `licenses/SourceHanSerif-OFL.txt`。

思源宋体提供字形结构输入，项目便签字提供风格参考；这不是直接复制思源宋体轮廓的拼接字库。按照 [SIL FAQ 1.25](https://openfontlicense.org/ofl-faq/)，OFL 字体经 AI／ML 转换形成的字体仍采用 OFL，版权和来源声明予以保留。

历史内部 v2.000 用过 Windows 宋体／ExtB 内容输入，未作为本项目的开源发布。公开版扩展字已经全部重新生成，原系统字库、逐字输入图和历史输出不包含在本仓库中。因此公开版本与内部 v2.000 的扩展字形会有差异。

## 工具与可复现范围

- MX-Font 提交：`93f3c88517f7c904f16da6333adb2588dcdf3cce`。其主许可为 MIT，但 `models/modules/modules.py` 有 FUNIT 来源例外，详见上游 NOTICE 的 CC BY-NC-SA 4.0。这里不把完整上游推理代码重新标记为 MIT，也不捆绑它或模型权重。
- 上游没有随官方检查点提供完整训练字体清单。本项目记录可核实的检查点摘要、推理输入与生成过程，不声称已审计未公开的训练数据。
- 轮廓转换使用 Potrace；字体编译使用 fontTools。已生成轮廓保存在 `source/`，公开构建只依赖 fontTools。
- 仓库自写构建、验证及 SVG 导出工具采用 MIT；字体及字形母版采用 OFL 1.1。第三方工具的许可证不被本仓库的 MIT 声明替换。
- `python tools/build.py` 从 TTX 轮廓重建字体，不需要模型、Windows 字体或互联网。它复现的是最终轮廓到字体这一阶段；不是承诺跨硬件重新运行神经网络得到逐像素相同输出。

## 字表与覆盖

8105 个规范汉字的序列来自 Unicode 17.0.0 Unihan 的 `kTGH` 映射，对应《通用规范汉字表》2013 版。Unicode 数据许可随附于 `licenses/Unicode-LICENSE.txt`。196 个字符位于 BMP 之外，字体包含 format 12 Unicode cmap。

完整覆盖是字符映射层面的保证，不代表包含所有繁体字、所有异体字、Emoji 或全部 Unicode。人工观察和自动检查的范围以 `qa/review.json` 为准。
