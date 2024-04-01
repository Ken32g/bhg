import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def max_intensity_projection_along_all_axes(input_nifti_file, output_png_file):
    # 读取nifti文件
    img = nib.load(input_nifti_file)

    # 获取数据
    data = img.get_fdata()
    spacing = img.header.get_zooms()
    aspect_ratio = spacing[2] / spacing[0]

    # 沿着X轴做最大密度投影
    max_projection_x = np.rot90(np.sum(data, axis=0))
    max_projection_y = np.rot90(np.sum(data, axis=1))
    max_projection_z = np.rot90(np.sum(data, axis=2))

    max_projection_x_resized = np.array(Image.fromarray(max_projection_x).resize((data.shape[1], int(data.shape[2]*aspect_ratio))))
    max_projection_y_resized = np.array(Image.fromarray(max_projection_y).resize((data.shape[0], int(data.shape[2]*aspect_ratio))))
    max_projection_z_resized = np.array(Image.fromarray(max_projection_z).resize((data.shape[0], data.shape[1])))
    
    # 创建子图，分别显示x、y、z轴的投影
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # 绘制子图
    axes[0].imshow(max_projection_x_resized, cmap='viridis')
    axes[0].set_title('X-axis projection')
    axes[1].imshow(max_projection_y_resized, cmap='viridis')
    axes[1].set_title('Y-axis projection')
    axes[2].imshow(max_projection_z_resized, cmap='viridis')
    axes[2].set_title('Z-axis projection')

    # 保存为png
    plt.savefig(output_png_file)

# 使用函数
input_file = '.nii.gz'
output_file = '.png'
max_intensity_projection_along_all_axes(input_file, output_file)
