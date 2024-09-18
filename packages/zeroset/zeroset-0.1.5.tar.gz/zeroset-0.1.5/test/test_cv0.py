from zeroset import cv0
import cv2
from zeroset import py0
from zeroset import viz0

s = py0.list_chunk(viz0.zeroset_colors, 100)

for e in s:
    print(len(e))

# img1 = cv0.from_url("https://ae01.alicdn.com/kf/H6717450a87eb42ec9733cc27d1c52d5aa.jpg")
#
# img2 = cv0.from_blank(500, 500, (24, 231, 124))
#
# img3 = viz0.write_fit_text(width=1000, height=400, text="안녕 디지몬", lr_pad=10, tb_pad=10)

# print(cv0.similarity.psnr(img1, img2))
#
# print(cv0.hash.average_hash(img1))
#
# cv0.exit()

# img = cv0.hconcat(img1, img2)

# cv0.imshow("img", img3)
# cv0.waitKey()
