from zeroset import cv0
import cv2

# img = cv0.from_url("https://ae01.alicdn.com/kf/H6717450a87eb42ec9733cc27d1c52d5aa.jpg")

# img = cv0.write_fit_text(2000, 500, "안녕하세요", 10, 10, (0, 0, 0), (255, 255, 255))
img = cv0.from_blank(500, 500, (24, 231, 124))
cv0.imshow("img", img)
cv0.waitKey()
