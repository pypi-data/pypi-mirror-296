from zeroset import cv0
import cv2

files = cv0.glob("")

for file in files:
    img = cv0.imread(file)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv0.imwrite(file, img)
    # cv0.imshow(img).waitKey()
