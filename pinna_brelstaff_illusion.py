import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

def create_pinna_brelstaff_illusion(num_rings= 2, num_segments=36,
                                   inner_radius=3.5, outer_radius=4.0,
                                   segment_width=4, segment_tilt=15,
                                   use_gradient=True, 
                                   gradient_colors=["#000000", "#808080"]):
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
    - gradient_colors: 渐变填充的颜色，列表形式，包含起始和结束颜色
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor('#808080')
    ax.set_aspect('equal')
    ax.set_facecolor('#808080')
    ax.set_xlim(-outer_radius-1, outer_radius+1)
    ax.set_ylim(-outer_radius-1, outer_radius+1)
    ax.axis('off')
    
    # 计算每个环的半径
    is_outer = [True, False]

    # 计算每个段的角度
    theta = np.linspace(0, 360, num_segments, endpoint=False)
    
    # 创建渐变颜色映射
    if use_gradient:
        cmap = LinearSegmentedColormap.from_list("custom_gradient", gradient_colors, N=256)
    
    # 创建每个环的线段
    patches = []
    
    for bd in is_outer:
        for t in theta:
            r = outer_radius if bd else inner_radius
            # 计算线段的角度范围
            t_start = t
            t_end = t + segment_width
            
            # 给线段添加倾斜角度
            tilt = segment_tilt if bd else 0
            
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
            
            # 使用渐变填充或纯色填充
            if use_gradient:
                # 计算渐变颜色值（基于角度位置）
                color_value = t / 360.0
                facecolor = cmap(color_value)
            else:
                facecolor = '#808080'
                
            polygon = Polygon(vertices, closed=True,
                              facecolor=facecolor, edgecolor=None)
            
            edge1_x = [vertices[0][0], vertices[1][0]]
            edge1_y = [vertices[0][1], vertices[1][1]]
            ax.plot(edge1_x, edge1_y, color='black' if bd else 'white', linewidth=1)

            edge2_x = [vertices[1][0], vertices[2][0]]
            edge2_y = [vertices[1][1], vertices[2][1]]
            ax.plot(edge2_x, edge2_y, color='black' if bd else 'white', linewidth=1)

            edge3_x = [vertices[2][0], vertices[3][0]]
            edge3_y = [vertices[2][1], vertices[3][1]]
            ax.plot(edge3_x, edge3_y, color='black' if not bd else 'white', linewidth=1)

            edge4_x = [vertices[3][0], vertices[0][0]]
            edge4_y = [vertices[3][1], vertices[0][1]]
            ax.plot(edge4_x, edge4_y, color='black' if not bd else 'white', linewidth=1)
            patches.append(polygon)
    
    # 将所有线段添加到图中
    p = PatchCollection(patches, match_original=True)
    ax.add_collection(p)

    ax.scatter(0, 0, color='black', s=100, zorder=10)

    plt.title('Pinna-Brelstaff', fontsize=16)
    return fig

if __name__ == "__main__":
    # 创建基本的Pinna-Brelstaff幻觉图像，使用渐变填充
    fig = create_pinna_brelstaff_illusion(use_gradient=True, 
                                        gradient_colors=["#000000", "#FFFFFF"])
    
    # 保存图像
    plt.savefig('pinna_brelstaff_illusion_gradient.png', dpi=300, bbox_inches='tight')
    
    # 显示图像
    plt.show() 