from PIL import Image, ImageTk, ImageSequence

fire_frames = []
water_frames = []
forest_frames = []
tiger_frames = []
lion_frames = []

def load_animation_frames():
    global fire_frames, water_frames, forest_frames, tiger_frames, lion_frames

    fire_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/fire.gif"))]
    water_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/water.gif"))]
    forest_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/forest.gif"))]
    tiger_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/tiger.gif"))]
    lion_frames = [ImageTk.PhotoImage(img.resize((40, 40), Image.ANTIALIAS)) for img in ImageSequence.Iterator(Image.open("resources/images/lion.gif"))]

def update_button_image(button, frames, index=0):
    button.config(image=frames[index])
    animation_id = button.after(100, update_button_image, button, frames, (index + 1) % len(frames))
    button.animation_id = animation_id
