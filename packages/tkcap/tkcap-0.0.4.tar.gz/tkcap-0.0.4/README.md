```
   __      __
  /  |    /  |
 _$$ |_   $$ |   __   _______   ______    ______
/ $$   |  $$ |  /  | /       | /      \  /      \
$$$$$$/   $$ |_/$$/ /$$$$$$$/  $$$$$$  |/$$$$$$  |
  $$ | __ $$   $$<  $$ |       /    $$ |$$ |  $$ |
  $$ |/  |$$$$$$  \ $$ \_____ /$$$$$$$ |$$ |__$$ |
  $$  $$/ $$ | $$  |$$       |$$    $$ |$$    $$/
   $$$$/  $$/   $$/  $$$$$$$/  $$$$$$$/ $$$$$$$/
                                        $$ |
                                        $$ |
                                        $$/
```

Welcome to my Github page! I am happy to present to you my personal project, tkcap. This is a Python script that lets you take screenshots of a Tkinter window.

Tkinter is a popular GUI toolkit for Python, and it's often used to develop desktop applications. Sometimes, you may need to take a screenshot of a Tkinter window for documentation or debugging purposes. This is where tkcap comes in handy. With just a few lines of code, you can capture a screenshot of your Tkinter window and save it as an image file.

tkcap is easy to use, and the script is designed to be lightweight and efficient. You simply import the **tkcap** module, create an instance of the **CAP** class, and call the `capture` method to take a screenshot. The captured screenshot can be saved in various image formats, including PNG, JPEG, and BMP.

I have thoroughly tested tkcap on different operating systems and with different versions of Python, and I am confident that it will work seamlessly for you. If you encounter any issues or have suggestions for improvement, please don't hesitate to open an issue on Github or reach out to me directly.

I hope that tkcap can be a useful tool for your Tkinter projects, and I look forward to hearing your feedback. Happy coding!

Ghanteyyy http://github.com/ghanteyyy
MIT License

# Requirements and Tested Platforms

- Python:

  > - 3.x

- Windows:
  > - Windows 10 & 11

# Installation

tkcap is available on PyPI. You can install it through pip:

`pip install tkcap`

# Usage

```python

  import tkcap

  cap = tkcap.CAP(master)  # 'master' is a tkinter window instance, passed to create a capture object
  cap.capture(FileName)    # Captures a screenshot of the tkinter window and saves it as provided FileName

  # To retrieve the x, y coordinates, width, and height of the tkinter window
  region = cap.get_region()

  # Bind a key (in this case, 'Control + g') to trigger a screenshot capture when pressed
  # Each time 'Control + g' is pressed, the screenshot will be saved as provided FileName
  master.bind('<Control-g>', lambda: cap.capture(FileName))
```
