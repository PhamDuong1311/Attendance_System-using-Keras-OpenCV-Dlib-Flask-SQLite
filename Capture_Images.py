import os
import cv2
from tkinter import messagebox

def takeImages(Id, name):
    folder_path = 'images'
    person_name = os.path.splitext(name)[0]
    person_Id = os.path.splitext(Id)[0]
    person_folder = os.path.join(folder_path, f"{person_name}_{person_Id}")
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)
        print(f"Thư mục cho '{person_name}_{person_Id}' đã được tạo!")

    cam = cv2.VideoCapture(0)
    sampleNum = 0
    captured_images = []

    while True:
        ret, img = cam.read()

        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 1
        font_color = (255, 0, 0)
        font_thickness = 2
        message = "Press c to capture 10 images"
        cv2.putText(img, message, (10, 30), font, font_scale, font_color, font_thickness)

        cv2.imshow('frame', img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            sampleNum = sampleNum + 1
            person_folder = os.path.join(folder_path, f"{person_name}_{person_Id}")

            image_path = person_folder + os.sep + f"{person_name}_{person_Id}_{sampleNum}.jpg"
            cv2.imwrite(image_path, img)
            captured_images.append(image_path)

            print(f"Đã chụp ảnh số {sampleNum}")

        if key == ord('q') or sampleNum >= 10:
            break

    cam.release()
    cv2.destroyAllWindows()

    show_images(captured_images)

def show_images(images):
    current_image_index = 0

    while True:
        img = cv2.imread(images[current_image_index])
        cv2.imshow('Images Captured', img)
        key = cv2.waitKey(0)

        if key == ord('q'):
            break
        elif key == ord('t') and current_image_index < len(images) - 1:
            current_image_index += 1
        elif key == ord('l') and current_image_index > 0:
            current_image_index -= 1

    cv2.destroyAllWindows()

    choice = messagebox.askquestion("Chụp lại?", "Bạn có muốn chụp lại không?")
    if choice == 'yes':
        for image_path in images:
            os.remove(image_path)

