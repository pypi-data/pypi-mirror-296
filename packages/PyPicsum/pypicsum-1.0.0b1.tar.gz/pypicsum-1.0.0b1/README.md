# PyPicsum

## Info

PyPicsum is a simple python library for using placeholder images, it is made using [Picsum](https://github.com/robertopreste/pypicsum)

## Useage

Useage is very simple, you need to have a basic tkinter app like:

```
import tkiner as tk

root = tk.Tk()
root.title('Simple Title')

root.mainloop()
```

Then you need to add a simple label:

```
import tkiner as tk

root = tk.Tk()
root.title('Simple Title')

label = tk.Label(master=root)
label.pack()

root.mainloop()
```

And finally you need to specifcy the image size, this can be done in 2 ways: For a Square:

```
pypicsum(image_x=500, label=label)
```

In that example, it will be a 500x500 image, and the label is called 'label'
To add it to you code ad it after the labe.pack but before the root.mainloop()

```
import tkiner as tk

root = tk.Tk()
root.title('Simple Title')

label = tk.Label(master=root)
label.pack()

pypicsum(image_x=500, label=label)

root.mainloop()
```

To make it a rectangle you can add an image_y value:

```pypicsum(image_x=500, image_y=200 label=label)```

so it would be a 500x200 image

