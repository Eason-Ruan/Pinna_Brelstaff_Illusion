import pinna_brelstaff_illusion

if __name__ == '__main__':
    color = ['#000000', '#111111', '#222222', '#333333', '#444444', '#555555','#666666', '#777777', '#888888', '#999999', '#AAAAAA', '#BBBBBB', '#CCCCCC', '#DDDDDD', '#EEEEEE', '#FFFFFF']
    for i in range(8):
        fig = pinna_brelstaff_illusion.create_pinna_brelstaff_illusion(
            inner_radius= 2,
            outer_radius= 2.5,
            gradient_colors=[color[i], color[15-i]],
            inner_polygon_gradient=True)
        fig.savefig(f"results/pinna_brelstaff_illusion_inner_gradient_{i}.png", dpi=300, bbox_inches='tight')