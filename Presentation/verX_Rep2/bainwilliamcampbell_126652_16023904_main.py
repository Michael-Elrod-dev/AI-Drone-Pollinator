from GreenHouseModel import greenHouseModel
import cv2

model = greenHouseModel(fileName = "./models/textBasedModel.txt")
cv2.imshow("planters", model.getPlanterModel())
# cv2.imshow("flowers", model.getFlowerModel())

cv2.waitKey()