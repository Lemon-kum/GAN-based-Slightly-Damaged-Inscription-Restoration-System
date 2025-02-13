# -*- codeing = utf-8 -*-
# @Time : 2024/2/27 20:53
# @Author : dujinjie
# @File : test.py
# @Software : PyCharm

import cv2
import numpy as np

image = cv2.imread('static/test2.png')
#颜色取反
inverted_image = 255 - image
#灰度化
gray_image = cv2.cvtColor(inverted_image, cv2.COLOR_BGR2GRAY)
#二值化
binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)[1]

#中值滤波
rec_img = cv2.medianBlur(binary_image,3)
#块匹配和三维滤波
bm3d_denoised = cv2.fastNlMeansDenoisingColored(image,None,30,10,7,21)
#非局部均值滤波
image_float = np.array(binary_image, dtype=np.float32)
denoised_image = cv2.fastNlMeansDenoising(binary_image, None, 30, 7, 21)
denoised_image_uint8 = np.clip(denoised_image, 0, 255).astype(np.uint8)
#局部均值滤波(效果差，字迹模糊)
kernel_size = 7  # 滤波器的大小，必须是奇数
blurred_image = cv2.blur(image, (kernel_size, kernel_size))


#低通滤波
# 对图像进行傅里叶变换
dft = cv2.dft(np.float32(rec_img), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)
# 创建低通滤波器
rows, cols = rec_img.shape
crow, ccol = rows // 2, cols // 2  # 中心点
mask = np.zeros((rows, cols, 2), np.uint8)
r = 10  # 滤波器的半径
center = [crow, ccol]
x, y = np.ogrid[:rows, :cols]
mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= r * r
mask[mask_area] = 1
# 应用低通滤波器
dft_shift_filtered = dft_shift * mask
# 执行逆傅里叶变换
idft_shift_filtered = np.fft.ifftshift(dft_shift_filtered)
image_filtered = cv2.idft(idft_shift_filtered)
image_filtered = cv2.magnitude(image_filtered[:, :, 0], image_filtered[:, :, 1])

#高通滤波
# 对图像进行傅里叶变换
dft = cv2.dft(np.float32(denoised_image), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)
# 创建高通滤波器
rows, cols = denoised_image.shape
crow, ccol = rows // 2, cols // 2  # 中心点
mask = np.ones((rows, cols, 2), np.uint8)
r = 10  # 滤波器的半径
mask[crow - r:crow + r + 1, ccol - r:ccol + r + 1] = 0  # 将中心低频区域置为0
# 应用高通滤波器
dft_shift_filtered = dft_shift * mask
# 执行逆傅里叶变换
idft_shift_filtered = np.fft.ifftshift(dft_shift_filtered)
image_filtered = cv2.idft(idft_shift_filtered)
image_filtered = cv2.magnitude(image_filtered[:, :, 0], image_filtered[:, :, 1])
# 为了增强高通滤波后的效果，通常会对图像进行归一化处理
norm_factor = np.max(image_filtered)
image_filtered = image_filtered / norm_factor

#平滑
# 使用平均滤波器进行平滑处理
# cv2.blur() 函数接收图像和一个核大小（宽和高必须是正奇数）
blurred_image = cv2.blur(rec_img, (5, 5))

# 使用高斯滤波器进行平滑处理
# cv2.GaussianBlur() 函数也接收图像和一个核大小，还可以指定X和Y方向的标准差
gaussian_blurred_image = cv2.GaussianBlur(rec_img, (5, 5), 0)

#锐化
# 定义一个6x6的锐化滤波器
sharpen_kernel = np.array([
    [-1, -1, -1],
    [-1, 9, -1],
    [-1, -1, -1],
])
# 使用filter2D函数应用滤波器
sharpened_image = cv2.filter2D(rec_img, -1, sharpen_kernel)

#显示图片
#cv2.imshow('Image',image)
cv2.imshow('Binary Image',binary_image)
#cv2.imshow('Rec Image',rec_img)
#cv2.imshow('Bm3d Image',bm3d_denoised)
#cv2.imshow('Denoised Image',denoised_image_uint8)
#cv2.imshow('Blurrd Image',blurred_image)
#cv2.imshow('Low-Pass Filtered Image', image_filtered)
#cv2.imshow('High-Pass Filtered Image', image_filtered)
#cv2.imshow('Blurred Image', blurred_image)
#cv2.imshow('Gaussian Blurred Image', gaussian_blurred_image)
#cv2.imshow('Sharpened Image', sharpened_image)

# 等待用户按键，然后关闭所有窗口
cv2.waitKey(0)
cv2.destroyAllWindows()

#保存图片
cv2.imwrite('0006.jpg',binary_image)