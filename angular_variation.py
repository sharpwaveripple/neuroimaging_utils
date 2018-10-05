import sys
import numpy as np
import nibabel as nib

#test
def find_adjacent(voxel):
    adj_voxels = np.empty([26, 3])
    xplus = x + 1
    xminus = x - 1
    yplus = y + 1
    yminus = y - 1
    zplus = z + 1
    zminus = z - 1
    adj_voxels[0] = data[xminus, yplus, zplus, :]
    adj_voxels[1] = data[xminus, y, zplus, :]
    adj_voxels[2] = data[xminus, yminus, zplus, :]
    adj_voxels[3] = data[x, yplus, zplus, :]
    adj_voxels[4] = data[x, y, zplus, :]
    adj_voxels[5] = data[x, yminus, zplus, :]
    adj_voxels[6] = data[xplus, yplus, zplus, :]
    adj_voxels[7] = data[xplus, y, zplus, :]
    adj_voxels[8] = data[xplus, yminus, zplus, :]
    adj_voxels[9] = data[xminus, yplus, z, :]
    adj_voxels[10] = data[xminus, y, z, :]
    adj_voxels[11] = data[xminus, yminus, z, :]
    adj_voxels[12] = data[x, yplus, z, :]
    adj_voxels[13] = data[x, yminus, z, :]
    adj_voxels[14] = data[xplus, yplus, z, :]
    adj_voxels[15] = data[xplus, y, z, :]
    adj_voxels[16] = data[xplus, yminus, z, :]
    adj_voxels[17] = data[xminus, yplus, zminus, :]
    adj_voxels[18] = data[xminus, y, zminus, :]
    adj_voxels[19] = data[xminus, yminus, zminus, :]
    adj_voxels[20] = data[x, yplus, zminus, :]
    adj_voxels[21] = data[x, y, zminus, :]
    adj_voxels[22] = data[x, yminus, zminus, :]
    adj_voxels[23] = data[xplus, yplus, zminus, :]
    adj_voxels[24] = data[xplus, y, zminus, :]
    adj_voxels[25] = data[xplus, yminus, zminus, :]
    return(adj_voxels)

def make_texture_image(data, dimensions):
    texture_image = np.empty(dimensions[0:3])
    for z in range(0, dimensions[2]-1):
        voxel_coor = np.nonzero(data[:, :, z, 0])
        for voxel in range(0, len(voxel_coor[0])):
            x = voxel_coor[0][voxel]
            y = voxel_coor[1][voxel]
            reference_voxel = data[x, y, z, :]
            adj_voxels = find_adjacent(reference_voxel)
            dot_products = np.arccos(np.sum(reference_voxel * adj_voxels, axis=1))
            angular_variation = np.sum(np.degrees(dot_products))
            texture_image[x, y, z] = angular_variation
    texture_image = texture_image / 26
    return texture_image

	
input = sys.argv[1]  # a principle eigenvector image
output = sys.argv[2]
img = nib.load(input)
img_hdr = img.header
eigenimage = img.get_data()
eigenimage = np.abs(eigenimage)
dims = eigenimage.shape

texture_img = make_texture_image(eigenimage, dims)
nifti_image = nib.Nifti1Image(texture_img,
                              affine=img_hdr.get_sform(coded=False))
nifti_image.to_filename(output)

