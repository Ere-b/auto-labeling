import os
import sys
import cv2
import glob
import numpy as np
from weapons import Weapon
from show_window_with_rect import show_window_with_rect

def auto_labeling(image, image_path, class_index, index, total_count, input_path, output_path):
  """
  이미지 파일의 레이블 정보가 담긴 .txt 파일을 생성하는 Function
  
  Output Format: <class_index> <x_center_relative> <y_center_relative> <width_relative> <height_relative>
  
  Args:
    image () 
    image_path (str): 객체를 탐지할 이미지의 파일 경로
    class_index (int): labelImg에서 설정할 class_index
    index (int): 현재 이미지 파일의 index
    total_count (int): 전체 이미지 파일의 개수
    input_path (str): 레이블링할 데이터 경로
    output_path (str): 레이블링 정보 파일 저장 경로
  """
  # 전 처리
  # _, binary_image = cv2.threshold(image, 225, 255, cv2.THRESH_BINARY_INV)
  _, binary_image = cv2.threshold(image, 225, 255, cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)

  # 모폴로지 연산에 사용할 커널 정의
  kernel = np.ones((3, 3), np.uint8)
  binary_image= cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
  
  # 객체의 외곽선 검출
  contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # 외곽선을 이용하여 객체의 경계 상자 좌표 계산
  x, y, w, h = cv2.boundingRect(contours[0])

  # 경계 상자를 사각형으로 그리기
  image_with_rect = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
  
  # 결과물 확인
  # show_window_with_rect(image_with_rect, image_path, x, y, w, h)

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
  print(txt_filename)
  txt_filename = txt_filename.replace(input_path, output_path)
  print(txt_filename)
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
    
def auto_labeling_batch(input_path, output_path):
  """
  Directory내의 모든 이미지 파일을 입력받아 auto_labeling()으로 파일 경로를 전달해주는 Function

  Args:
    input_path (str): directory path
    output_path (str): output path
  """
  # 디렉토리 내의 모든 이미지 파일 경로를 리스트로 저장
  image_files = glob.glob(os.path.join(input_path, "*.jpg"))

  # 전체 이미지 파일의 개수
  total_count = len(image_files)
  print(total_count)
  
  if total_count == 0:
    print("파일이 존재하지 않습니다.")
    sys.exit()
  
  # 디렉토리 내의 모든 이미지 파일에 대해 auto_labeling() 호출
  for index ,image_path in enumerate(image_files, start=1):
    image = cv2.imread(image_path)
    if image is not None and 'Weapon china knife' in image_path:
      auto_labeling(image, image_path, Weapon.c_knife.value, index, total_count, input_path, output_path)
    elif 'Weapon knife' in image_path or 'Weapon military knife' in image_path:
      auto_labeling(image, image_path, Weapon.knife.value, index, total_count, input_path, output_path)
    elif 'Pistol' in image_path or 'Revolver' in image_path:
      auto_labeling(image, image_path, Weapon.pistol.value, index, total_count, input_path, output_path)
    elif 'MP5' in image_path:
      auto_labeling(image, image_path, Weapon.gun.value, index, total_count, input_path, output_path)
    elif 'UZI' in image_path:
      auto_labeling(image, image_path, Weapon.uzi.value, index, total_count, input_path, output_path)
    else:
      print(f"Failed to read the image file: {image_path}")

# main()
while True:
  try:
    input_path = input("이미지 경로 (0 to quit): ")
    if input_path == '0':
      sys.exit()
    elif os.path.isdir(input_path) and os.path.exists(input_path):
      output_path = input("저장 경로: ")
      auto_labeling_batch(input_path, output_path)
    else:
      print("유효하지 않은 경로입니다. 다시 입력해주세요.")
  except ValueError:
    print("잘못된 입력입니다. 다시 입력해주세요.")
