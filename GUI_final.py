import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import cv2
import os
import Recognition
import Capture_Images
from Jsoncreating import *
from tkinter import messagebox
from predictmodel import *
import win32api
def center_window(window, width, height):
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

window = tk.Tk()
window.title("Hệ thống nhận dạng khuôn mặt")
window.iconbitmap("models_weights_logo\logo.ico")
center_window(window, 1500, 800)
window.resizable(False, False)

background_label = tk.Label(window)
background_image = Image.open("Img_gui\GUI.png")
window_width, window_height = 1600, 800
background_image = background_image.resize((window_width, window_height))
background_image = ImageTk.PhotoImage(background_image)
background_label.configure(image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
LABEL = tk.Label(window, text = "Hệ thống điểm danh",bg="#FFCC99", fg="blue",
                       width=25, height=2, font=('times', 30, 'italic bold ') )
LABEL.place(x = 450 , y= 50 )

def Recognize():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Camera', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('c'):
            predict()
            cv2.imwrite('captured_image.jpg', frame)
            caption = Recognition.check('captured_image.jpg')                                               
            os.remove('captured_image.jpg')
            noti.configure(text= caption)
            break
    cap.release()
    cv2.destroyAllWindows()

def Register():
    window2 = tk.Toplevel()  # Tạo một cửa sổ con
    window2.title("Face_Recognizer")
    window2.iconbitmap("models_weights_logo\logo.ico")
    center_window(window2, 1500, 800)
    window2.resizable(False, False)

        # Xóa tất cả các widget trong cửa sổ con
    for widget in window2.winfo_children():
        widget.destroy()

    background_label1 = tk.Label(window2)
    background_image1 = Image.open("Img_gui\\GUI.png")
    background_image1 = background_image1.resize((1600, 800))
    background_image1 = ImageTk.PhotoImage(background_image1)
    background_label1.configure(image=background_image1)
    background_label1.place(x=0, y=0, relwidth=1, relheight=1)
    
    def clear():
        txt.delete(0, 'end')
        res = ""
        message.configure(text=res)

    def clear2():
        txt2.delete(0, 'end')
        res = ""
        message.configure(text=res)

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def TakeImages():
        Id = txt.get()
        name = txt2.get()

        if is_number(Id) and any(char.isalpha() for char in name) and name.strip() != "":
            Capture_Images.takeImages(Id, name)
            res = "Images Saved " + name
            row = [Id, name]
            message.configure(text=res)
        else:
            if not is_number(Id):
                res = "Chưa nhập MSSV bạn ơi"
            elif not any(char.isalpha() for char in name):
                res = "Nhập nốt Họ tên đi bạn ơi"
            else:
                res = "Nhập tên không trống"

            message.configure(text=res)

    def Embedding():
        try:
            jsonVectorized("images")  # Gọi hàm jsonVectorized với đường dẫn "images"
            messagebox.showinfo("Thông báo", "Ảnh đã được lưu rùi ạ")
            predict()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

    clearButton = tk.Button(window2, text="Xóa", command=clear, fg="red", bg="#FFCC33", width=20, height=2, activebackground="Red",
                            font=('times', 15, ' bold '))
    clearButton.place(x=800, y=200)

    clearButton2 = tk.Button(window2, text="Xóa", command=clear2, fg="red", bg="#FFCC33", width=20, height=2, activebackground="Red",
                            font=('times', 15, ' bold '))
    clearButton2.place(x=800, y=300)

    TakeImage = tk.Button(window2, text='Bước 1: Chụp ảnh', command=TakeImages, fg='red', bg='#FFCC00', width=20, height=2,
                         activebackground='Red', font=('times', 15, 'bold'))
    TakeImage.place(x=500, y=500)

    Embedding = tk.Button(window2, text='Bước 2: Lưu ảnh', command=Embedding, fg='red', bg='#FFCC00', width=20, height=2,
                          activebackground='Red', font=('times', 15, 'bold'))
    Embedding.place(x=800, y=500)
    
    message = tk.Label(window2, text="Đăng ký người mới", bg="#FFCC99", fg="blue", width =25, height =2
                       
                        , font=('times', 30, 'italic bold '))
    message.place(x=400, y=20)
    

    lbl = tk.Label(window2, text="Nhập MSSV", width=20, height=2, fg="red", bg="#FFCC66", font=('times', 15, ' bold '))
    lbl.place(x=200, y=215)
    txt = tk.Entry(window2, width=20, bg="#FFFFCC", fg="red", font=('times', 15, ' bold '))
    txt.place(x=500, y=215)

    lbl2 = tk.Label(window2, text="Nhập tên", width=20, fg="red", bg="#FFCC66", height=2, font=('times', 15, ' bold '))
    lbl2.place(x=200, y=300)
    txt2 = tk.Entry(window2, width=20, bg="#FFFFCC", fg="red", font=('times', 15, ' bold'))
    txt2.place(x=500, y=315)

    lbl3 = tk.Label(window2, text="Thông báo : ", width=20, fg="red", bg="#FFCC66", height=2, font=('times', 15, ' bold underline '))
    lbl3.place(x=200, y=400)
    message = tk.Label(window2, text="", bg="#FFCC66", fg="red", width=30, height=2, activebackground="yellow",
                       font=('times', 15, ' bold '))
    message.place(x=500, y=400)

    window2.mainloop()
    
noti = tk.Label(window, text="" ,bg="#FFCC66"  ,fg="red"  ,width=30  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold ')) 
noti.place(x=840, y=600)
    
image1 = Image.open("Img_gui\\register.jpg")
image1 = image1.resize((250, 250))  
photo1 = ImageTk.PhotoImage(image1)
button1 = Button(window, text = "Đăng kí", image=photo1, command=Register)
button1.place(x=300, y=300)

image2 = Image.open("Img_gui\\recognition.jpg")
image2 = image2.resize((250, 250))  
photo2 = ImageTk.PhotoImage(image2)
button2 = Button(window, text = "Nhận diện", command = Recognize , image=photo2)
button2.place(x=900, y=300)



window.mainloop()

