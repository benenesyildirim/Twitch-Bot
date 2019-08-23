import argparse
import sys
from twitchbot import TwitchBot

parser = argparse.ArgumentParser(description="Simple Twitch Bot")
parser.add_argument('-c', '--command', nargs='+', required=False,
                    help="You can add new command & response in database")
parser.add_argument('-r', '--run', nargs='+', required=False, help="Run script")
args = vars(parser.parse_args())
command_argv = sys.argv[1]
if command_argv == '-c' or command_argv == '--command':
    TwitchBot.add_command(*args['command'])
elif command_argv == '-r' or command_argv == '--run':
    t_bot = TwitchBot(sys.argv[2], sys.argv[3], sys.argv[4])
    while True:
        viewer_user, t_command = t_bot.get_message()
        c_response = t_bot.check_command(t_command)
        t_bot.send_message(viewer_user, c_response)
