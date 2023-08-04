import os
import sys
import cv2
import glob
from weapons import Weapon

def auto_labeling(image_path, class_index, index, total_count):
  """
  이미지 파일의 레이블 정보가 담긴 .txt 파일을 생성하는 Function
  
  Output Format: <class_index> <x_center_relative> <y_center_relative> <width_relative> <height_relative>
  
  Args:
    image_path (str): 객체를 탐지할 이미지의 파일 경로
    class_index (int): labelImg에서 설정할 class_index
    index (int): 현재 이미지 파일의 index
    total_count (int): 전체 이미지 파일의 개수
  """
  # 이미지 파일 읽기
  image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
  
  # 전 처리
  threshold_value = 215 
  image[image >= threshold_value] = 255
  _, binary_image = cv2.threshold(image, 220, 255, cv2.THRESH_BINARY_INV)
  # _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
  
  # 객체의 외곽선 검출
  contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # 외곽선을 이용하여 객체의 경계 상자 좌표 계싼
  x, y, w, h = cv2.boundingRect(contours[0])

  # 경계 상자를 사각형으로 그리기
  image_with_rect = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

  # 그린 rectangle의 중심 좌표값과 폭, 높이 계산
  x_center = x + w // 2
  y_center = y + h // 2
  width = w
  height = h

  # 좌표값과 폭, 높이를 이미지의 가로/세로 크기에 상대적인 비율로 변환
  image_width, image_height = image.shape[1], image.shape[0]
  x_center_relative = round(x_center / image_width, 6)
  y_center_relative = round(y_center / image_height, 6)
  width_relative = round(width / image_width, 6)
  height_relative = round(height / image_height, 6)
  
  # .txt 파일로 저장
  txt_filename = image_path.replace(".jpg", ".txt")
  txt_filename = txt_filename.replace("64_half_test", "64_half_test_label")
  try:
    with open(txt_filename, "w") as f:
        f.write(
            f"{class_index} {x_center_relative} {y_center_relative} {width_relative} {height_relative}"
        )
    print(f"레이블 정보를 생성 class index: {class_index} 진행률: {(index/total_count)*100:.1f}%")
  except FileNotFoundError as e:
    print("파일을 찾을 수 없습니다:", e)
  except PermissionError as e:
    print("파일에 쓸 권한이 없습니다:", e)
  except OSError as e:
    print("파일 작업 중 오류가 발생했습니다:", e)
    
def auto_labeling_batch(directory_path, class_index):
  """
  Directory내의 모든 이미지 파일을 입력받아 auto_labeling()으로 파일 경로를 전달해주는 Function

  Args:
    directory_path (_type_): directory path
    class_index (_type_): class_index
  """
  # 디렉토리 내의 모든 이미지 파일 경로를 리스트로 저장
  image_files = glob.glob(os.path.join(directory_path, "*.jpg"))
  # 전체 이미지 파일의 개수
  total_count= len(image_files)
  
  # 디렉토리 내의 모든 이미지 파일에 대해 auto_labeling() 호출
  for index ,image_path in enumerate(image_files, start=1):
    image = cv2.imread(image_path)
    if image is not None:
      auto_labeling(image_path, class_index, index,total_count)
    else:
      print(f"Failed to read the image file: {image_path}")

# 예제 이미지에 대한 레이블 정보를 생성
directory_path = "./64_half_test"
while True:
  try:
    class_index = int(input("Select class index(0. c_knife 1. knife 2. pistol 3. gun 4. unknown 5 uzi 6. empty) 99 to quit: "))
    if class_index == Weapon.c_knife.value:
      auto_labeling_batch(directory_path, Weapon.c_knife.value)
    elif class_index == Weapon.knife.value:
      auto_labeling_batch(directory_path, Weapon.knife.value)
    elif class_index == Weapon.pistol.value:
      auto_labeling_batch(directory_path, Weapon.pistol.value)
    elif class_index == Weapon.gun.value:
      auto_labeling_batch(directory_path, Weapon.gun.value)
    elif class_index == Weapon.unknown.value:
      auto_labeling_batch(directory_path, Weapon.unknown.value)
    elif class_index == Weapon.uzi.value:
      auto_labeling_batch(directory_path, Weapon.uzi.value)
    elif class_index == Weapon.empty.value:
      auto_labeling_batch(directory_path, Weapon.empty.value)
    elif class_index == 99:
      sys.exit()
    else:
      print("잘못된 입력입니다. 다시 입력해주세요.")
  except ValueError:
    print("잘못된 입력입니다. 다시 입력해주세요.")
