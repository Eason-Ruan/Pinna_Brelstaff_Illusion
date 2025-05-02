import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

def create_frame(frame, num_rings=10, num_segments=36, 
                inner_radius=0.5, outer_radius=4.0, 
                segment_width=0.4, segment_tilt=15,
                scale_factor=0.05, use_gradient=False,
                gradient_start="#000000", gradient_end="#FFFFFF",
                ax=None):
    """
    创建动画的单帧
    
    参数:
    - frame: 当前帧号
    - 其他参数与create_pinna_brelstaff_illusion相同
    - scale_factor: 缩放因子，控制"呼吸"效果的幅度
    - use_gradient: 是否使用渐变填充
    - gradient_start: 渐变起始颜色
    - gradient_end: 渐变结束颜色
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
    else:
        ax.clear()
        
    # 创建缩放效果，模拟向图像靠近/远离
    frame_scale = 1.0 + scale_factor * np.sin(frame * 0.1)
    current_outer_radius = outer_radius * frame_scale
    current_inner_radius = inner_radius * frame_scale
    
    ax.set_aspect('equal')
    ax.set_xlim(-outer_radius*1.2, outer_radius*1.2)
    ax.set_ylim(-outer_radius*1.2, outer_radius*1.2)
    ax.axis('off')
    
    # 创建渐变色映射
    if use_gradient:
        # 根据当前帧动态调整渐变颜色
        phase = np.sin(frame * 0.05) * 0.3 + 0.5  # 0.2 到 0.8 之间变化
        cmap = LinearSegmentedColormap.from_list("custom_gradient", 
                                              [gradient_start, gradient_end], N=256)
    
    # 计算每个环的半径
    radii = np.linspace(current_inner_radius, current_outer_radius, num_rings)
    
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
                # 基于角度、半径位置和当前帧计算渐变颜色
                color_value = (t / 360.0 + r / current_outer_radius + frame / 100.0) % 1.0
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
    
    # 添加标题，显示当前状态（展开或收缩）
    if np.sin(frame * 0.1) > 0:
        status = "扩张"
    else:
        status = "收缩"
    
    plt.title(f'Pinna-Brelstaff 幻觉图像 - {status}中', fontsize=16)
    
    return p

def create_animated_illusion(save_gif=True, use_gradient=False):
    """创建动画版本的Pinna-Brelstaff幻觉
    
    参数:
    - save_gif: 是否保存为GIF文件
    - use_gradient: 是否使用渐变填充
    """
    # 创建图形和坐标轴
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 设置参数
    num_rings = 12
    num_segments = 36
    segment_tilt = 15
    gradient_start = "#000000"
    gradient_end = "#FFFFFF"
    
    # 初始化第一帧
    patch_collection = create_frame(0, num_rings=num_rings, 
                                   num_segments=num_segments,
                                   segment_tilt=segment_tilt,
                                   use_gradient=use_gradient,
                                   gradient_start=gradient_start,
                                   gradient_end=gradient_end,
                                   ax=ax)
    
    # 动画更新函数
    def update(frame):
        patch_collection = create_frame(frame, num_rings=num_rings, 
                                       num_segments=num_segments,
                                       segment_tilt=segment_tilt,
                                       use_gradient=use_gradient,
                                       gradient_start=gradient_start,
                                       gradient_end=gradient_end,
                                       ax=ax)
        return [patch_collection]
    
    # 创建动画
    ani = FuncAnimation(fig, update, frames=100, blit=True, interval=50)
    
    # 如果需要保存GIF
    if save_gif:
        output_filename = 'pinna_brelstaff_animated_gradient.gif' if use_gradient else 'pinna_brelstaff_animated.gif'
        ani.save(output_filename, writer='pillow', fps=20, dpi=100)
    
    # 显示动画
    plt.tight_layout()
    plt.show()
    
    return ani

if __name__ == "__main__":
    # 创建并显示动画，启用渐变效果
    ani = create_animated_illusion(save_gif=True, use_gradient=True) 