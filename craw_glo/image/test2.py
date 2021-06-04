import pymysql,time,datetime
import cv2
import numpy as np
import requests
import urllib.request
from matplotlib import pyplot as plt
from PIL import Image
from io import BytesIO
from test import *

def url_to_image(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    # im_rgb = cv2.cvtColor(im_cv, cv2.COLOR_BGR2RGB)
    image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)

    return image

def imgCheck():
    url1 = 'https://www.ksubtv.co/wp-content/themes/ksubtv/scripts/timthumb.php?src=https://www.ksubtv.co/wp-content/uploads/2018/09/bcvbvbnbvnvbnvbn.png&w=400&h=600&zc=1'
    u = urllib.parse.quote('나의 나라.jpg')
    url2 = 'http://61.82.113.196:8181/poster/'+u
    img1 = url_to_image(url1)
    img2 = url_to_image(url2)

    # filepath1 = r"C:\Users\user\Desktop\crawling_glo\image\img\del4.jpg"
    # filepath2 = r"C:\Users\YW\Desktop\crawling_glo\image\img\test.jpg"
    # img1 = readImg(filepath1)
    # img2 = readImg(filepath2)

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    # Need to draw only good matches, so create a mask
    matchesMask = [[0,0] for i in range(len(matches))]

    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.3*n.distance:
            matchesMask[i]=[1,0]

    check_text = matchesMask.count([1,0])
    print(check_text)

    draw_params = dict(matchColor = (0,255,0),singlePointColor = (255,0,0),matchesMask = matchesMask,flags = 2)
    knn_image = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
    plt.imshow(knn_image)
    plt.show()

    # return check_text


if __name__=='__main__':
    start_time = time.time()

    print("test 크롤링 시작")
    imgCheck()
    print("test 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
