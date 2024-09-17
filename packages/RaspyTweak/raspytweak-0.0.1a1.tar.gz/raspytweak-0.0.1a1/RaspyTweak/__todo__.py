import sys
if sys.platform in ("win32", "win64", "amd64", "darwin", "sunos5", "aix", "hp-ux", "os2", "riscos", "vms"):
    OSInvalid("\033[31mThis software requires a RaspberryPI device and a supported operating system!\033[0m\n>> Refer to the readme for more information") # type: ignore
try:
    with open('/etc/os-release') as f:
        os_info = f.read()
    if ('Raspbian', 'Raspberry Pi', 'Raspberry OS') in os_info:
        from .gpio import *
    else:
        OSInvalid("\033[31mThis software requires a RaspberryPI device and a supported operating system!\033[0m\n>> Refer to the readme for more information") # type: ignore
except FileNotFoundError:
    OSInvalid("\033[31mThis software requires a RaspberryPI device and a supported operating system!\033[0m\n>> Refer to the readme for more information") # type: ignore
except Exception:
    pass
del sys
