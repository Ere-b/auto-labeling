import cv2

def show_window_with_rect(image_with_rect, image_path, x, y, w, h):
  """
  객체가 감지된 이미지를 보여주는 Function

  Args:
      image_path (str): _description_
      x (int): _description_
      y (int): _description_
      w (int): _description_
      h (int): _description_
  """
  cv2.rectangle(image_with_rect, (x, y), (x + w, y + h), (0, 0, 255), 1)
  cv2.imshow(image_path, image_with_rect)
  cv2.namedWindow(image_path, cv2.WINDOW_NORMAL)
  cv2.resizeWindow(image_path, 640, 480)
  cv2.waitKey(0)
  cv2.destroyAllWindows()