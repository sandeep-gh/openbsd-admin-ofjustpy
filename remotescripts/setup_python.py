
def setup():
    if os.path.exists("/home/shared/pyvenv/bin/activate"):
        exec_cmd([
            "python3.11", "-m", "venv", "/home/shared/pyvenv"
        ]
                 )

        exec_cmd([
            "source",  "/home/shared/pyvenv/bin/activate", ";", "pip3", "install", "wget"
]

                 )

        # install these as well 
        pip_modules = ["jinja2",
                       "aenum",
                       "itsdangerous",
                       "hjson",
                       "httpx",
                       "psutil",
                       "starlette",
                       "uvicorn",
                       "websockets",
                       "aiofiles",
                       "twine",
                       "wheel",
                       "aenum",
                       "jsbeautifier",
                       "dpath",
                       ]
