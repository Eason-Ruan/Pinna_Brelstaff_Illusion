# Pinna-Brelstaff 错觉生成器

这是一个生成 Pinna-Brelstaff 视觉错觉的 Python 工具。这种错觉在旋转时会产生奇特的视觉感受，静止的同心环在旋转时会产生扭曲感。

## 功能特点

- 生成基于 Pinna-Brelstaff 原理的视觉错觉图像
- 支持自定义参数（环数、段数、内外半径等）
- 提供渐变填充选项
- 高质量图像导出功能

## 安装要求

```
numpy
matplotlib
```

安装依赖包：

```bash
pip install numpy matplotlib
```

## 使用方法

```python
import matplotlib.pyplot as plt
from pinna_brelstaff_illusion import create_pinna_brelstaff_illusion

# 创建基本的 Pinna-Brelstaff 错觉图像
fig = create_pinna_brelstaff_illusion(
    inner_radius=2,
    outer_radius=2.5,
    inner_polygon_gradient=False
)

# 保存图像
plt.savefig('pinna_brelstaff_illusion.png', dpi=300, bbox_inches='tight')

# 显示图像
plt.show()
```

## 参数说明

- `num_rings`：环的数量（默认2）
- `num_segments`：每个环的线段数量（默认30）
- `inner_radius`：最内环的半径（默认3.5）
- `outer_radius`：最外环的半径（默认4.0）
- `segment_width`：每个线段的宽度(角度)（默认5）
- `segment_tilt`：线段的倾斜角度(角度)（默认15）
- `gradient_colors`：渐变填充的颜色，列表形式（默认["#000000", "#808080"]）
- `inner_polygon_gradient`：是否在单个多边形内部使用渐变填充（默认False）

## Pinna-Brelstaff 错觉原理

Pinna-Brelstaff 错觉是由 Pinna 和 Brelstaff 发现的一种动态视觉错觉。当观察者接近或远离由倾斜线条组成的同心环图案时，静止的图案会产生旋转的错觉。这种现象与人类视觉系统处理运动信息的方式有关。

通过旋转本项目生成的图像，你将能观察到这种奇妙的视觉效果。

## 幻觉原理

Pinna-Brelstaff幻觉是一种动态视觉幻觉，通过静态图像产生运动感知。当观察者向图像靠近或远离时，大脑将径向的缩放运动误解为旋转运动。这种效果是由于图像中倾斜的线段以特定方式排列导致的。

## 文件说明

本项目包含三个主要脚本:

1. **pinna_brelstaff_illusion.py** - 基本版本，生成静态图像
2. **pinna_brelstaff_interactive.py** - 交互版本，可以调整参数
3. **pinna_brelstaff_animated.py** - 动画版本，自动模拟靠近/远离效果

## 使用方法

### 基本版本

```bash
python pinna_brelstaff_illusion.py
```

这将生成一个基本的Pinna-Brelstaff幻觉图像并保存为PNG文件。

### 交互版本

```bash
python pinna_brelstaff_interactive.py
```

运行交互版本后，你可以:
- 调整倾斜角度滑块来改变线段的倾斜程度
- 改变环数来增加或减少同心环的数量
- 修改每环段数来调整细节程度
- 点击重置按钮恢复默认设置

### 动画版本

```bash
python pinna_brelstaff_animated.py
```

动画版本会自动生成一个GIF文件，模拟向图像靠近和远离时产生的效果。

## 观察方法

为了最好地体验这种幻觉:
1. 固定视线在图像中心
2. 缓慢向图像靠近或远离
3. 观察同心环似乎在顺时针或逆时针方向旋转的感觉

## 科学背景

Pinna-Brelstaff幻觉揭示了人类视觉系统如何处理运动和形状信息。这种幻觉对研究视觉运动处理、空间感知和大脑如何整合视觉信息非常有价值。

## 参考文献

Pinna, B., & Brelstaff, G. J. (2000). A new visual illusion of relative motion. Vision Research, 40(16), 2091-2096. 