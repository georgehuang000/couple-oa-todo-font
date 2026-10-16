# 参与改进

欢迎报告缺字、错字、笔画拥挤和字距问题。Issue 请包含：字符与 Unicode、使用字号、浏览器 / 设计软件名称，以及能说明问题的最短文本或截图。请勿上传私人聊天或无权公开的图片。

目前维护的是 604 汉字设计母版；缺字列表见 `data/characters.json`。提出新增字符时，请说明使用场景；不要用其他字形代替后仅修改 Unicode 映射。

`sources/ttx/CoupleOATodo-Regular.ttx` 是构建入口，各字形拆分为独立 TTX。`sources/svg/` 用于查看与设计编辑；只改 SVG 不会自动改动编译结果，提交时需要把最终轮廓同步回 TTX。普通贡献者可以先提交 SVG 建议，由维护者完成字形导入与度量核对。

修改字体后，在独立目录构建，对比样张，并运行 `python scripts/verify.py`。正式更新需同步字体、SVG、`data/characters.json` 中的摘要、`project.json`、字体内部版本和 FONTLOG。不要把单纯的哈希变化当作视觉验收。

提交者应有权按对应目录许可提供贡献：字形与字体源码使用 OFL-1.1，构建和页面代码使用 MIT。保留必要的第三方版权、来源和修改说明。


便签手记的修改方式请看[对应贡献说明](https://github.com/georgehuang000/couple-oa-todo-font/blob/main/note/CONTRIBUTING.md)。以上流程适用于待办手写体。
