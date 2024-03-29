from api import API

import sounddevice as sd
import soundfile as sf
from abc import ABC, abstractmethod

import os


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

    def __call__(self, *args):
        global kwargs, rate
        _, audio = self.api.regenerate_response(**kwargs)
        sd.play(audio, rate)
        sd.wait()


class SaveCommand(Command):
    def __init__(self):
        super().__init__(
            "save",
            "Save the audio response to a file",
            "save",
        )
        current_directory = os.getcwd()
        output_folder = os.path.join(current_directory, "output_audio_response")
        os.makedirs(output_folder, exist_ok=True)
        self.output_path = os.path.join(output_folder, "audio_response.wav")

    def __call__(self, *args):
        global audio, rate
        if audio is None:
            print("No audio to save")
            return
        sf.write(self.output_path, audio, rate)


class PlayCommand(Command):
    def __init__(self):
        super().__init__("play", "Play the audio response", "play")

    def __call__(self, *args):
        global audio, rate
        if audio is None:
            print("No audio to play")
            return
        sd.play(audio, rate)
        sd.wait()


kwargs = {
    "speaker": "kaguya",
    "language": "日本語",
    "speed": 0.7,
    "noise_scale": 0.667,
    "noise_scale_w": 0.6,
}

api = API()
rate = api.rate
audio = None

# Map commands to functions
commands = {
    "quit": QuitCommand(),
    "help": HelpCommand(),
    "set": SetCommand(),
    "reset": ResetCommand(kwargs),
    "kwargs": KwargsCommand(),
    "regenerate": RegenerateCommand(api),
    "save": SaveCommand(),
    "play": PlayCommand(),
}


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
