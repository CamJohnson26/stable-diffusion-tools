from cmd import Cmd

from dotenv import load_dotenv

from generate_image import generate_image
from prompt_helpers import generate_object_close_up, generate_outside_wide_shot

load_dotenv()

# token = os.environ.get("")


class CLIApp(Cmd):
    """A simple CLI app."""
    prompt = '>>> '

    def do_generate(self, args):
        """Generate an image."""
        description = args
        generate_image(description)

    def do_object(self, args):
        """Generate an image of an object."""
        description = args
        generate_object_close_up(description)

    def do_outside(self, args):
        """Generate an image outside."""
        description = args
        generate_outside_wide_shot(description)

    def do_exit(self, args):
        """Exit the app."""
        raise SystemExit()


if __name__ == '__main__':
    CLIApp().cmdloop("Enter a command (greet, exit):")
