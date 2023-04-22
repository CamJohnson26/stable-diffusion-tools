from cmd import Cmd

from dotenv import load_dotenv

from background_job import initiate_background_tasks
from prompt_helpers import generate_object_close_up, generate_outside_wide_shot
# from prompt_helpers import generate_object_close_up, generate_outside_wide_shot
from rabbitmq import publish_message

load_dotenv()

# token = os.environ.get("")


class CLIApp(Cmd):
    """A simple CLI app."""
    prompt = '>>> '

    def do_consume(self, args):
        """Start consuming messages."""
        initiate_background_tasks()

    def do_generate(self, args):
        """Generate an image."""
        description = args
        publish_message(description, 'image_generate')

    def do_object(self, args):
        """Generate an image of an object."""
        description = generate_object_close_up(args)
        publish_message(description, 'image_generate')


    def do_outside(self, args):
        """Generate an image outside."""
        description = generate_outside_wide_shot(args)
        publish_message(description, 'image_generate')

    def do_exit(self, args):
        """Exit the app."""
        raise SystemExit()


if __name__ == '__main__':
    CLIApp().cmdloop("Enter a command (greet, exit):")
