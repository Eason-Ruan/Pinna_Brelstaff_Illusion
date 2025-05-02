import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.widgets import Slider, Button, CheckButtons
from matplotlib.colors import LinearSegmentedColormap

def create_pinna_brelstaff_illusion(num_rings=10, num_segments=36, 
                                   inner_radius=0.5, outer_radius=4.0, 
                                   segment_width=0.4, segment_tilt=15,
                                   use_gradient=False, gradient_start="#000000", 
                                   gradient_end="#FFFFFF", ax=None):
    """
    创建Pinna & Brelstaff幻觉图像
    
    参数:
    - num_rings: 环的数量
    - num_segments: 每个环的线段数量
    - inner_radius: 最内环的半径
    - outer_radius: 最外环的半径
    - segment_width: 每个线段的宽度(角度)
    - segment_tilt: 线段的倾斜角度(角度)
    - use_gradient: 是否使用渐变填充
    - gradient_start: 渐变起始颜色
    - gradient_end: 渐变结束颜色
    - ax: matplotlib坐标轴对象，如果为None则创建新的
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
    else:
        ax.clear()
        fig = ax.figure
    
    ax.set_aspect('equal')
    ax.set_xlim(-outer_radius-1, outer_radius+1)
    ax.set_ylim(-outer_radius-1, outer_radius+1)
    ax.axis('off')
    
    # 创建渐变色映射
    if use_gradient:
        cmap = LinearSegmentedColormap.from_list("custom_gradient", 
                                               [gradient_start, gradient_end], N=256)
    
    # 计算每个环的半径
    radii = np.linspace(inner_radius, outer_radius, num_rings)
    
    # 计算每个段的角度
    theta = np.linspace(0, 360, num_segments, endpoint=False)
    
    # 创建每个环的线段
    patches = []
    
    for r in radii:
        for t in theta:
            # 交替改变线段的颜色
            is_black = (int(t / (360 / num_segments)) % 2 == 0)
            
            # 计算线段的角度范围
            t_start = t
            t_end = t + segment_width
            
            # 给线段添加倾斜角度
            tilt = segment_tilt if is_black else -segment_tilt
            
            # 计算线段的四个顶点
            inner_start_x = r * np.cos(np.radians(t_start + tilt))
            inner_start_y = r * np.sin(np.radians(t_start + tilt))
            
            inner_end_x = r * np.cos(np.radians(t_end + tilt))
            inner_end_y = r * np.sin(np.radians(t_end + tilt))
            
            outer_start_x = (r + 0.3) * np.cos(np.radians(t_start + tilt))
            outer_start_y = (r + 0.3) * np.sin(np.radians(t_start + tilt))
            
            outer_end_x = (r + 0.3) * np.cos(np.radians(t_end + tilt))
            outer_end_y = (r + 0.3) * np.sin(np.radians(t_end + tilt))
            
            # 创建线段的多边形
            vertices = np.array([
                [inner_start_x, inner_start_y],
                [inner_end_x, inner_end_y],
                [outer_end_x, outer_end_y],
                [outer_start_x, outer_start_y]
            ])
            
            if use_gradient:
                # 基于角度和半径位置计算渐变颜色
                color_value = (t / 360.0 + r / outer_radius) / 2
                facecolor = cmap(color_value)
            else:
                if is_black:
                    facecolor = 'black'
                else:
                    facecolor = 'white'
                
            polygon = Polygon(vertices, closed=True, 
                            facecolor=facecolor, edgecolor=None)
                
            patches.append(polygon)
    
    # 将所有线段添加到图中
    p = PatchCollection(patches, match_original=True)
    ax.add_collection(p)
    
    plt.title('Pinna-Brelstaff 幻觉图像 - 移动鼠标靠近/远离图像查看旋转效果', fontsize=14)
    return fig

def interactive_illusion():
    """创建一个交互式的Pinna-Brelstaff幻觉图像"""
    # 创建图形和子图
    fig = plt.figure(figsize=(12, 10))
    ax_illusion = plt.axes([0.1, 0.25, 0.8, 0.7])  # 主图区域
    
    # 初始参数
    init_num_rings = 10
    init_num_segments = 36
    init_inner_radius = 0.5
    init_outer_radius = 4.0
    init_segment_width = 0.4
    init_segment_tilt = 15
    init_use_gradient = False
    gradient_start = "#000000"
    gradient_end = "#FFFFFF"
    
    # 创建初始幻觉图像
    create_pinna_brelstaff_illusion(
        init_num_rings, init_num_segments, 
        init_inner_radius, init_outer_radius,
        init_segment_width, init_segment_tilt,
        init_use_gradient, gradient_start, gradient_end,
        ax=ax_illusion
    )
    
    # 创建滑块区域
    ax_tilt = plt.axes([0.25, 0.18, 0.65, 0.03])
    ax_rings = plt.axes([0.25, 0.13, 0.65, 0.03])
    ax_segments = plt.axes([0.25, 0.08, 0.65, 0.03])
    
    # 创建滑块
    slider_tilt = Slider(ax_tilt, '倾斜角度', 0, 30, valinit=init_segment_tilt)
    slider_rings = Slider(ax_rings, '环数', 5, 20, valinit=init_num_rings, valstep=1)
    slider_segments = Slider(ax_segments, '每环段数', 12, 72, valinit=init_num_segments, valstep=4)
    
    # 创建重置按钮
    ax_reset = plt.axes([0.1, 0.03, 0.1, 0.03])
    button_reset = Button(ax_reset, '重置')
    
    # 创建渐变切换按钮
    ax_gradient = plt.axes([0.55, 0.03, 0.2, 0.03])
    check_gradient = CheckButtons(ax_gradient, ['启用渐变填充'], [init_use_gradient])
    
    # 滑块更新函数
    def update(val):
        num_rings = int(slider_rings.val)
        num_segments = int(slider_segments.val)
        segment_tilt = slider_tilt.val
        use_gradient = check_gradient.get_status()[0]
        
        create_pinna_brelstaff_illusion(
            num_rings, num_segments, 
            init_inner_radius, init_outer_radius,
            init_segment_width, segment_tilt,
            use_gradient, gradient_start, gradient_end,
            ax=ax_illusion
        )
        fig.canvas.draw_idle()
    
    # 渐变切换函数
    def toggle_gradient(label):
        update(None)
    
    # 重置按钮函数
    def reset(event):
        slider_tilt.reset()
        slider_rings.reset()
        slider_segments.reset()
        check_gradient.set_active(0, False)
        update(None)
    
    # 注册滑块更新函数
    slider_tilt.on_changed(update)
    slider_rings.on_changed(update)
    slider_segments.on_changed(update)
    
    # 注册渐变切换按钮
    check_gradient.on_clicked(toggle_gradient)
    
    # 注册重置按钮函数
    button_reset.on_clicked(reset)
    
    # 提示文本
    fig.text(0.5, 0.01, '提示: 观察图像时，移动头部靠近或远离屏幕可以看到旋转效果', 
             ha='center', fontsize=12, color='red')
    
    plt.show()

if __name__ == "__main__":
    interactive_illusion() 