import cx_Freeze

executables = [cx_Freeze.Executable("maze.py")]

cx_Freeze.setup(
    name="Mazer",
    options={"build_exe": {"packages": ["pygame", "time"],
                           "include_files": ["2.mp3", "./ext/fonts/msyh.ttf", "./images/back button.png",
                                             "./images/easy.png", "./images/hard.png", "./images/medium.png"]}},
    executables=executables

)
