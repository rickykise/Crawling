import pymysql,time,datetime
import cv2
import numpy as np
import requests
import urllib.request
from matplotlib import pyplot as plt
from PIL import Image
from io import BytesIO

def url_to_image(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    # im_rgb = cv2.cvtColor(im_cv, cv2.COLOR_BGR2RGB)
    image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)


    return image

def readImg(filepath):
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    # cv2.namedWindow("root", cv2.WINDOW_NORMAL) # window 생성
    # cv2.imshow("root", img) # window에 이미지 띄우기
    # cv2.waitKey(5000) # 5초 기다림. 아무키나 입력되면 대기 종료
    # cv2.destroyAllWindows() # window 제거
    return img

def diffImg(img1, img2) :
    # Initiate SIFT detector
    orb = cv2.ORB_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # Match descriptors.
    matches = bf.match(des1,des2)
    # Sort them in the order of their distance.

    matches = sorted(matches, key = lambda x:x.distance)
    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])

    # Draw first 10 matches.
    knn_image = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
    # knn_image = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches[:2], None, flags=2)
    check_text = len(good)
    print(check_text)
    plt.imshow(knn_image)
    plt.show()

    return check_text

def startCrawling():
    # url1 = 'http://61.82.113.196:8181/poster/poster.jpg'
    # url2 = 'http://kanbo8.com/Uploads/vod/2019-09-05/5d712ae4278d4.jpg'

    url1 = 'http://61.82.113.196:8181/poster/poster.jpg'
    url2 = 'http://61.82.113.196:8181/poster/poster.jpg'
    # url2 = 'http://cn2.3days.cc/1571710321475390.jpeg'
    img1 = url_to_image(url1)
    img2 = url_to_image(url2)

    # 이미지 객체 가져옴
    # filepath1 = r"C:\Users\user\Desktop\crawling_glo\image\images3.jpg"
    # filepath2 = r"C:\Users\user\Desktop\crawling_glo\image\images4.jpg"
    # img1 = readImg(filepath1)
    # img2 = readImg(filepath2)

    # 2개의 이미지 비교
    img_check = diffImg(img1, img2)


if __name__=='__main__':
    start_time = time.time()

    print("test 크롤링 시작")
    startCrawling()
    print("test 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
