import cv2,os
import numpy as np
from matplotlib import pyplot as plt

envpath = '/home/beango/.local/lib/python3.9/site-packages/cv2/qt/plugins/platforms'
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = envpath

img = cv2.imread('1.jpg', 0)
img2 = img.copy()
template = cv2.imread('3.png', 0)
w, h = template.shape[::-1]
# 所有的匹配方法
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
for meth in methods:
    img = img2.copy()
    method = eval(meth)  # 去掉字符串的引号
    # 匹配
    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # 使用不同的比较方法，对结果的解释不同
    # 如果方法是 TM_SQDIFF or TM_SQDIFF_NORMED, 取最小值
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
 
    cv2.rectangle(img, top_left, bottom_right, 255, 2)
 
    plt.subplot(121), plt.imshow(res, cmap='gray'),
    plt.title('Matching Result'), plt.axis('off')
    plt.subplot(122), plt.imshow(img, cmap='gray'),
    plt.title('Detected Point'), plt.axis('off')
    plt.suptitle(meth)
 
    plt.show()
    