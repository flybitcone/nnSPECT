import os

import SimpleITK as sitk
import numpy as np
import pickle


def center_of_mass_sitk(image):
    # Get the image properties
    spacing = image.GetSpacing()
    origin = image.GetOrigin()
    size = image.GetSize()
    # Calculate the coordinates of each pixel in the image
    xx, yy, zz = np.meshgrid(
        np.arange(size[0]),
        np.arange(size[1]),
        np.arange(size[2]),
        indexing='ij'
    )
    # Apply the spacing and origin to the pixel coordinates
    xx = xx * spacing[0] + origin[0]
    yy = yy * spacing[1] + origin[1]
    zz = zz * spacing[2] + origin[2]
    # Get the image intensity values
    values = sitk.GetArrayViewFromImage(image)
    values = values.transpose((2,1,0))
    # Calculate the center of mass
    center_of_mass = np.array([np.sum(xx * values) / np.sum(values),
                               np.sum(yy * values) / np.sum(values),
                               np.sum(zz * values) / np.sum(values)])
    return center_of_mass

class ImageRead:
    def __init__(self, path=""):
        self.path = path
        self.stage = 0

    def read_image(self):
        if self.path.endswith(".dcm"):
            self.path = os.path.dirname(self.path)
            reader = sitk.ImageSeriesReader()
            dicom_names = reader.GetGDCMSeriesFileNames(self.path)
            reader.SetFileNames(dicom_names)
            self.image = reader.Execute()
        else:
            self.image = sitk.ReadImage(self.path)
        self.image_show = sitk.GetArrayFromImage(self.image)
        self.voxel_size = self.image.GetSpacing()
        self.origin = self.image.GetOrigin()
        self.matrix_size = self.image.GetSize()

    def set_type(self, type):
        self.type = type

    def read_seg(self, path, type):
        self.stage = 1
        self.seg = ImageRead(path, type)
        self.seg.read_image()
        self.seg.image = sitk.Cast(self.seg.image, sitk.sitkUInt8)
        self.seg.image.SetOrigin(self.origin)
        self.seg.image.SetSpacing(self.voxel_size)
        if type != "tumor":
            self.organ[type] = self.seg
        else:
            self.organ["tumor"].append(self.seg)

    def flip(self, index=0):
        if index == '1':
            self.image_show = self.image_show[:,:,::-1]
        elif index == '3':
            self.image_show = self.image_show[:, ::-1, :]
        else:
            self.image_show = self.image_show[::-1, :, :]
        self.image = sitk.GetImageFromArray(self.image_show)
        self.image.SetSpacing(self.voxel_size)
        self.image.SetOrigin(self.origin)


    def resample_to(self, image2):
        self.image = sitk.Resample(self.image, image2)
        self.image_show = sitk.GetArrayFromImage(self.image)
        self.voxl_size = self.image.GetSpacing()
        self.origin = self.image.GetOrigin()
        if self.organ["liver"] !="":
            self.organ["liver"].image = sitk.Resample(self.organ["liver"].image, image2)
        if self.organ["lung"] !="":
            self.organ["lung"].image = sitk.Resample(self.organ["lung"].image, image2)
        if self.organ["tumor"] !="":
            for i in range(len(self.organ["tumor"])):
                self.organ["tumor"][i].image = sitk.Resample(self.organ["tumor"][i].image, image2)
        return self.image

    def resample_com_to(self, image2):
        center1 = center_of_mass_sitk(self.image)
        center2 = center_of_mass_sitk(image2)

        translation = [center2[i] - center1[i] for i in range(3)]
        self.image = sitk.Resample(self.image, image2)
        transform = sitk.TranslationTransform(3, translation)
        self.image = sitk.Resample(self.image, image2, transform)
        if self.organ["liver"] !="":
            self.organ["liver"].image = sitk.Resample(self.organ["liver"].image, image2, transform)
        if self.organ["lung"] !="":
            self.organ["lung"].image = sitk.Resample(self.organ["lung"].image, image2, transform)
        if self.organ["tumor"] !="":
            for i in range(len(self.organ["tumor"])):
                self.organ["tumor"][i].image = sitk.Resample(self.organ["tumor"][i].image, image2, transform)
        self.image_show = sitk.GetArrayFromImage(self.image)
        self.voxl_size = self.image.GetSpacing()
        self.origin = self.image.GetOrigin()
        return self.image

    def resample_with_move(self, direction, type, image):
        origin = self.image.GetOrigin()
        spacing = self.image.GetSpacing()
        new_origin = [origin[0], origin[1], origin[2]]
        if type == 0:
            new_origin[direction] += spacing[direction]
        else:
            new_origin[direction] -= spacing[direction]
        self.image.SetOrigin(new_origin)
        return self.resample_to(image)

    def save(self, path):
        with open(path, 'wb') as outp:  # Overwrites any existing file.
            pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)

    def load(self, path):
        filehandler = open(path, 'w')
        pickle.dump(self, filehandler)