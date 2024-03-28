import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
import matplotlib.cm as cm
import matplotlib.animation as animation
from skimage import measure, transform
import sys

import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy import ndimage
from scipy.spatial import ConvexHull
from scipy import ndimage
from scipy import ndimage as ndi
from skimage import measure

def crop_zero_voxels(matrix):
    # Find the indices of non-zero elements along each axis
    non_zero_indices = np.nonzero(matrix)
    min_indices = np.min(non_zero_indices, axis=1)
    max_indices = np.max(non_zero_indices, axis=1)
    
    # Crop the matrix based on non-zero indices
    cropped_matrix = matrix[min_indices[0]:max_indices[0]+1, 
                            min_indices[1]:max_indices[1]+1, 
                            min_indices[2]:max_indices[2]+1]
    
    return cropped_matrix

def get_aha17_segment_gif(seg_result ,n_view=36, interval=100):
   
    img = nib.load(seg_result).get_fdata()
    
    img = crop_zero_voxels(img).astype(np.uint8)
    # img = rotz(img)
    img =  np.rot90(img, k=1, axes=(2, 1))
    resize_factor = 1
    resized_img = np.int_(img[::resize_factor, ::resize_factor, ::resize_factor])


    colors = cm.Spectral(np.linspace(0, 1, 17))
    colors_rgb = colors[:, :3]  
    np.random.shuffle(colors_rgb)

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='3d'))
    for idx, label in enumerate(range(1, np.int_(resized_img.max()) + 1)):
            # points = np.argwhere(resized_img == label)
            # ax.scatter(points[:,0],points[:,1],points[:,2], s =250, c  = colors_rgb[idx])

            verts, faces, _, _ = measure.marching_cubes(resized_img == label, step_size=1)
            ax.plot_trisurf( verts[:, 1], verts[:, 0],faces, verts[:, 2], color = colors_rgb[idx], lw=1, antialiased=True ,shade=True)
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    def update(frame):
        print(frame)
        ax.view_init(elev=0, azim= 360/n_view*frame, roll=0)
    
    ani = animation.FuncAnimation(fig, update, frames=n_view, interval=interval)
    ani.save('segmentation_animation.gif', writer='imagemagick', fps=4)

    plt.show()


seg_result = "PA702_merged_result.nii.gz"
get_aha17_segment_gif(seg_result, n_view = 36, interval=150)
