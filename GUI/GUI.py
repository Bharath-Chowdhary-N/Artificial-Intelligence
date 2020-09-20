import tkinter as tk
from tkinter import filedialog

def func_button1():
    print('button is pressed')
    file_path = filedialog.askopenfilename()
    
root = tk.Tk() #create a GUI main window and place everything within root.mainloop()
# Rename the title of the window
root.title("Image Classifier GUI - @YUGItech")



#canvas to place button_1

canvas=tk.Canvas(root,height=20,width=80)
canvas.pack()

#Background image
background_image=tk.PhotoImage(file='background_image.png')
background_label=tk.Label(root,image=background_image)
background_label.place(relwidth=1,relheight=1)

# Frame
#frame = tk.Frame(root,bg='#80c1ff')
#frame.place(relx=0.1,rely=0.1,relwidth=0.5,relheight=0.5)


# Label
label = tk.Label(root,text='AI Image Classifier',font=("Arial Bold",25),bg='#fafafa').pack()
root.geometry('1050x600')
root.wm_attributes('-transparentcolor',background_label['bg'])

# button_1
button_1 = tk.Button(root, text="Import Images (from folder)",bg='gray',fg='black',command=func_button1)
#button_1.grid_location(0.1,0.5)
#button_1.pack(side='bottom',fill='x',expand=True)
#button_1.grid(row=0,column=1)
button_1.place(relx=0.25,rely=0.5,relwidth=0.5,relheight=0.1)


#
root.configure(background='#064b4f')
root.mainloop()
