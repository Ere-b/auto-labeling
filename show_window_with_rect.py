import cv2

def show_window_with_rect(image_with_rect, image_path, x, y, w, h):
  """
  객체가 감지된 이미지를 보여주는 Function

  Args:
      image_with_rect (str): 객체 검출 결과물
      image_path (str): 이미지 경로
      x (int): value of x
      y (int): value of y
      w (int): width of rectangle
      h (int): height of rectangle
  """
  cv2.rectangle(image_with_rect, (x, y), (x + w, y + h), (0, 0, 255), 1)
  cv2.imshow(image_path, image_with_rect)
  cv2.namedWindow(image_path, cv2.WINDOW_NORMAL)
  cv2.resizeWindow(image_path, 640, 480)
  cv2.moveWindow(image_path, 500,0)
  cv2.waitKey(0)
  cv2.destroyAllWindows()