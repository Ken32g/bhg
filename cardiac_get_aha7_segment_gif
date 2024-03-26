import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
import matplotlib.cm as cm
import matplotlib.animation as animation

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

def get_aha17_segment_gif(seg_result ,n_view = 36, interval=100):
   
    img = nib.load(seg_result).get_fdata()

    img = crop_zero_voxels(img)
    resize_factor = 2
    resized_img = img[::resize_factor, ::resize_factor, ::resize_factor].astype(np.uint8)

    colors = cm.Spectral(np.linspace(0, 1, 18))
    colors_rgb = colors[:, :3]  
    np.random.shuffle(colors_rgb)

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='3d'))

    def update(frame):
        ax.clear()
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        
        for idx, label in enumerate(range(1, np.int(resized_img.max()) + 1)):
            points = np.argwhere(resized_img == label)
            ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=240,c=[colors_rgb[idx]])
        
        ax.view_init(elev=30, azim=360/n_view*frame)

    ani = animation.FuncAnimation(fig, update, frames=n_view, interval)
    ani.save('segmentation_animation.gif', writer='imagemagick', fps=9)

    plt.show()


seg_result = "PA1001_merged_result.nii.gz"
get_aha17_segment_gif(seg_result)
