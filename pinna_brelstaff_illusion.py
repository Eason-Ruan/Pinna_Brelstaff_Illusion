import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, PathPatch
from matplotlib.collections import PatchCollection
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.path import Path
import matplotlib as mpl

def create_pinna_brelstaff_illusion(num_rings= 2, num_segments=30,
                                   inner_radius=3.5, outer_radius=4.0,
                                   segment_width=5, segment_tilt=15,
                                   gradient_colors=["#000000", "#808080"],
                                   inner_polygon_gradient=False):
    """
    Create Pinna & Brelstaff illusion image
    
    Parameters:
    - num_rings: Number of rings
    - num_segments: Number of segments per ring
    - inner_radius: Radius of the innermost ring
    - outer_radius: Radius of the outermost ring
    - segment_width: Width of each segment (in degrees)
    - segment_tilt: Tilt angle of segments (in degrees)
    - gradient_colors: Colors for gradient fill, in list form, containing start and end colors
    - inner_polygon_gradient: Whether to use gradient fill inside individual polygons
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
            
            # 创建线段的多边形顶点
            vertices = np.array([
                [inner_start_x, inner_start_y],
                [inner_end_x, inner_end_y],
                [outer_end_x, outer_end_y],
                [outer_start_x, outer_start_y]
            ])
            
            if inner_polygon_gradient:
                # 使用更简单直接的方式创建渐变填充
                if bd:
                    color_start = gradient_colors[0]
                    color_end = gradient_colors[1]
                else:
                    color_start = gradient_colors[1]
                    color_end = gradient_colors[0]

                # 使用颜色数组直接创建渐变填充的多边形集合
                # 通过创建从一个顶点到另一个顶点的多个三角形，每个三角形使用不同的颜色
                # 这样实现从左上到右下的渐变效果
                
                # 找出多边形的左上角和右下角顶点
                # 获取多边形的边界框
                xmin, ymin = np.min(vertices, axis=0)
                xmax, ymax = np.max(vertices, axis=0)
                
                # 创建一系列细分多边形来模拟渐变
                # 这里我们将原始多边形分割成更多的小多边形
                n_subdivisions = 300  # 增加细分数量以使渐变更平滑
                
                # 将多边形分割成从左上到右下的一系列条带
                for i in range(n_subdivisions):
                    ratio_start = i / n_subdivisions
                    ratio_end = (i + 1) / n_subdivisions
                    
                    # 计算当前细分的颜色
                    color = mcolors.to_rgba(
                        mcolors.rgb2hex(
                            (1-ratio_start) * np.array(mcolors.to_rgb(color_start)) +
                            ratio_start * np.array(mcolors.to_rgb(color_end))
                        )
                    )
                    
                    # 连接多边形顶点的对角线，从左上到右下
                    # 在大多数四边形中，0是左上(inner_start)，2是右下(outer_end)
                    # 创建细分多边形的顶点
                    if i == 0:
                        # 第一个区域（最左上）
                        sub_poly = Polygon([
                            vertices[0],  # inner_start (左上)
                            vertices[0] + (vertices[1] - vertices[0]) * ratio_end,  # inner向右
                            vertices[0] + (vertices[3] - vertices[0]) * ratio_end,  # inner向下
                        ], closed=True, facecolor=color, edgecolor=None)
                        ax.add_patch(sub_poly)
                    elif i == n_subdivisions - 1:
                        # 最后一个区域（最右下）
                        sub_poly = Polygon([
                            vertices[2] + (vertices[1] - vertices[2]) * (1 - ratio_start),  # outer向左
                            vertices[2],  # outer_end (右下)
                            vertices[2] + (vertices[3] - vertices[2]) * (1 - ratio_start),  # outer向上
                        ], closed=True, facecolor=color, edgecolor=None)
                        ax.add_patch(sub_poly)
                    elif  i < n_subdivisions / 2:
                        # 中间区域，创建渐变条带
                        # 计算当前和下一个插值点
                        top_left = vertices[0] + (vertices[1] - vertices[0]) * ratio_start * 2
                        top_right = vertices[0] + (vertices[1] - vertices[0]) * ratio_end * 2
                        bottom_left = vertices[0] + (vertices[3] - vertices[0]) * ratio_start * 2
                        bottom_right = vertices[0] + (vertices[3] - vertices[0]) * ratio_end * 2
                        
                        sub_poly = Polygon([
                            top_left, top_right, bottom_right, bottom_left
                        ], closed=True, facecolor=color, edgecolor=None)
                        ax.add_patch(sub_poly)
                    else:
                        # 中间区域，创建渐变条带
                        # 计算当前和下一个插值点
                        top_left = vertices[2] + (vertices[1] - vertices[2]) * (2 - ratio_start  * 2)
                        top_right = vertices[2] + (vertices[1] - vertices[2]) * (2 - ratio_end  * 2)
                        bottom_left = vertices[2] + (vertices[3] - vertices[2]) * (2 - ratio_start * 2)
                        bottom_right = vertices[2] + (vertices[3] - vertices[2]) *(2 - ratio_end * 2)

                        sub_poly = Polygon([
                            top_left, top_right, bottom_right, bottom_left
                        ], closed=True, facecolor=color, edgecolor=None)
                        ax.add_patch(sub_poly)
                # 绘制边缘线条


            else:
                # 常规方法 - 每个多边形使用单一颜色
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

    
    # 将所有线段添加到图中，如果有的话
    if patches:
        p = PatchCollection(patches, match_original=True)
        ax.add_collection(p)

    ax.scatter(0, 0, color='black', s=100, zorder=10)

    plt.title('Pinna-Brelstaff', fontsize=16)
    return fig

if __name__ == "__main__":
    # 创建基本的Pinna-Brelstaff幻觉图像，使用多边形内部渐变填充
    fig = create_pinna_brelstaff_illusion(
        inner_radius=2,
        outer_radius=2.5,
        inner_polygon_gradient=False)
    
    # 保存图像
    plt.savefig('pinna_brelstaff_illusion_inner_gradient.png', dpi=300, bbox_inches='tight')
    
    # 显示图像
    plt.show() 