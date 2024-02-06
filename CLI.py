from api import API

import sounddevice as sd

import torch
import gc

from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, name, description, usage):
        self.name = name
        self.description = description
        self.usage = usage

    @abstractmethod
    def __call__(self, *args):
        pass

    def __str__(self):
        return (
            "- "
            + self.name
            + ":  "
            + self.description
            + "\n  "
            + "Usage: "
            + self.usage
        )


class QuitCommand(Command):
    def __init__(self):
        super().__init__("quit", "Exit the program", "quit")

    def __call__(self, *args):
        global running
        running = False
        print("Exiting...")


class HelpCommand(Command):
    def __init__(self):
        super().__init__("help", "Show available commands", "help")

    def __call__(self, *args):
        print("Available commands:")
        for command in commands.values():
            print(command)


class SetCommand(Command):
    def __init__(self):
        super().__init__(
            "set",
            "Set a key-value pair in kwargs",
            "set -<type> <key> <value>, where <type> is -s, -f, or -i",
        )

    def __call__(self, *args):
        global kwargs
        if len(args) != 3:
            print("Invalid number of arguments")
            return
        type_ = args[0]
        key = args[1]
        value = args[2]
        if type_ == "-s":
            kwargs[key] = str(value)
        elif type_ == "-f":
            kwargs[key] = float(value)
        elif type_ == "-i":
            kwargs[key] = int(value)
        else:
            print("Invalid type")
            return
        print("Current kwargs:", kwargs)


class ResetCommand(Command):
    def __init__(self, kwargs):
        super().__init__("reset", "Reset kwargs to original values", "reset")
        self.original_kwargs = kwargs.copy()

    def __call__(self, *args):
        global kwargs
        kwargs = self.original_kwargs.copy()
        print("Reset to original kwargs:", kwargs)


class KwargsCommand(Command):
    def __init__(self):
        super().__init__("kwargs", "Print the current kwargs", "kwargs")

    def __call__(self, *args):
        global kwargs
        print(kwargs)

class RegenerateCommand(Command):
    def __init__(self, api_instance):
        super().__init__("regenerate", "Regenerate audio response", "regenerate")
        self.api = api_instance
        self.response = None  # 初始化 response
        self.audio = None  # 初始化 audio

    def __call__(self):
        if self.api is None:
            print("Error: API instance is None")
            return

        try:
            print("test1")
            self.response, self.audio = self.api.regenerate_response(**kwargs)
            if self.response is None or self.audio is None:
                print("Error: API response or audio is None")
                return
            sd.play(self.audio, rate)
            sd.wait()
        except Exception as e:
            print("Error:", e)


kwargs = {
    "speaker": "kaguya",
    "language": "日本語",
    "speed": 0.7,
    "noise_scale": 0.667,
    "noise_scale_w": 0.6,
}

api = API()

# Map commands to functions
commands = {
    "quit": QuitCommand(),
    "help": HelpCommand(),
    "set": SetCommand(),
    "reset": ResetCommand(kwargs),
    "kwargs": KwargsCommand(),
    "regenerate": RegenerateCommand(api),
}


rate = api.rate

print("type 'help' for help")

running = True
# Main loop
while running:
    prompt = input(">> ")
    prompt = prompt.strip()
    parts = prompt.split(" ")
    command = parts[0]
    args = [arg for arg in parts[1:] if arg != ""]

    if command in commands.keys():
        # Call the command function with arguments
        commands[command](*args)
    else:
        _, audio = api(prompt, **kwargs)
        # play
        sd.play(audio, rate)
        sd.wait()

        # clear memory
        torch.cuda.empty_cache()
        gc.collect()
