# Pinna & Brelstaff 幻觉图像生成器

这个项目使用Matplotlib复刻了著名的Pinna & Brelstaff视觉幻觉。这种幻觉由Giovanni Pinna和Gavin J. Brelstaff于1994年首次报道，展示了当观察者靠近或远离由倾斜线段组成的同心环图案时会产生旋转的错觉。

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

## 依赖库

- NumPy
- Matplotlib

安装依赖:
```bash
pip install numpy matplotlib
```

## 科学背景

Pinna-Brelstaff幻觉揭示了人类视觉系统如何处理运动和形状信息。这种幻觉对研究视觉运动处理、空间感知和大脑如何整合视觉信息非常有价值。

## 参考文献

Pinna, B., & Brelstaff, G. J. (2000). A new visual illusion of relative motion. Vision Research, 40(16), 2091-2096. 