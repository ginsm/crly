"""Usage:
  crly [--help | --version] [options]

Options:
  -s, --show <name>        Select a show
  -e, --episode <number>   Select an episode (default: oldest ep)
  -q, --quality <quality>  Set the video quality (default: "best")
  -p, --play               Play the selected episode
  -a, --autoplay           Autoplay episodes (default: false)
  -n, --next               Select the next episode
  -i, --info               Print information about the show
  -t, --track              Begin tracking a show
  -u, --updates            Check tracked shows for updates
  -d, --debug              Print debug information
  -h, --help               Print this help screen
  -v, --version            Print the current version"""

import sys
import atexit

from docopt import docopt

from .modules.utility import Utility

# Set root path variable (used in Store)
Utility.set_env('root_path', Utility.get_path(__file__))

from .modules.store import Store
from .modules.error import Error
from .modules.handler import Handler


def main():
  # Initialize state
  Store.init_state(
      default_state={
          'show': None,
          'quality': "best",
          'autoplay': False,
          'playing': False,
          'tracked': [],
      })

  # Toggle playing at exit (pid locked)
  atexit.register(Handler.playing)

  # Handle any edge cases
  Error.check.required_native_packages(['streamlink'])
  Error.check.no_arguments_issue_help(sys.argv, __doc__)

  # Initialize docopt
  options = docopt(__doc__, help=True, version='crly v0.2.0')

  # The order in which option handlers should execute
  option_priority = [
      '--debug', '--show', '--episode', '--quality', '--next', '--track',
      '--updates', '--info', '--autoplay', '--play'
  ]

  # Option handler delegation
  for opt in option_priority:
    value = options[opt]
    if value:
      # Normalize method name and retrieve method
      method_name = opt.removeprefix('--').replace('-', '_')
      method = Handler.get(method_name)

      if method:
        method(value, options)


if __name__ == '__main__':
  main()