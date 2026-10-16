# Editable source / 可编辑源文件

`font.ttx` 是 fontTools TTX 主入口，引用同目录的分表和逐字文件。字体轮廓、字距、映射、名称、版权和许可证都在这些 XML 文件里。

```sh
python tools/build.py
```

从仓库根目录运行，输出到 `build/fonts/`。不需要模型推理、原项目目录或系统字体。已安装 `requirements.txt` 中的依赖后，重建可离线进行。

`font._g_l_y_f.*.ttx` 文件包含逐字轮廓（具体名称以主文件的引用为准），`font._h_m_t_x.ttx` 包含字距，`font._c_m_a_p.ttx` 包含编码映射。可用文本编辑器修改，或通过字体编辑软件导入 TTF 并重新导出 TTX。详见 [贡献说明](../CONTRIBUTING.md)。

字体与这些母版采用仓库根目录的 OFL 1.1。生成模型的训练过程不属于此构建所复现的范围。
