from nilearn import image

# 读取niigz文件
input_niigz = 'input_file.nii.gz'
img = image.load_img(input_niigz)

# 计算新的空间分辨率
new_affine = img.affine.copy()
new_affine[2, 2] *= 1/3  # 将z轴spacing变成原来的1/3

# 执行重采样
resampled_img = image.resample_img(img, target_affine=new_affine, interpolation='continuous')

# 保存重采样后的文件
output_niigz = 'output_resampled_file.nii.gz'
resampled_img.to_filename(output_niigz)

