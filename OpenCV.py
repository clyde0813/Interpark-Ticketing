import cv2
import numpy as np

# Load image, grayscale, adaptive threshold
image = cv2.imread('./captcha.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,85,1)

# Morph open
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

# Remove noise by filtering using contour area
cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    if area < 30:
        cv2.drawContours(opening, [c], -1, (0,0,0), -1)
kernel2 = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
opening = cv2.filter2D(opening,-1,kernel2)

# Invert image for result
result = 255 - opening

cv2.imshow('image', image)
cv2.imshow('2', thresh)
cv2.imshow('1', opening)
cv2.imshow('result', result)
cv2.waitKey()