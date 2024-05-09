# Used ChatGPT To make this code object oriented. 
# Original Model taken from https://python-sounddevice.readthedocs.io/en/0.4.6/examples.html#plot-microphone-signal-s-in-real-time:~:text=Output%20Pass%2DThrough-,Plot%20Microphone%20Signal(s)%20in%20Real%2DTime,-Real%2DTime%20Text
import argparse
import queue
import sys
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

class AudioStream:
    def __init__(self, args):
        self.args = args
        self.queue = queue.Queue()
        # Ensure the mapping for channels starts from 0 since array indices start at 0
        self.mapping = [c - 1 for c in self.args.channels]
        self.stream = sd.InputStream(
            device=self.args.device, channels=max(self.args.channels),
            samplerate=self.args.samplerate, callback=self.audio_callback)

    def audio_callback(self, indata, frames, time, status):
        """Callback function for each audio block."""
        if status:
            print(status, file=sys.stderr)
        # Apply mapping correctly; use the entire slice if the mapping is empty
        try:
            if self.mapping:
                self.queue.put(indata[::self.args.downsample, self.mapping])
            else:
                self.queue.put(indata[::self.args.downsample])
        except Exception as e:
            print(f"Error during audio callback processing: {e}")


    def start(self):
        with self.stream:
            plt.show()

class AudioVisualizer:
    average_rms = 100

    def __init__(self, queue, args):
        self.queue = queue  # AudioVisualizer now has access to the queue
        self.args = args
        # self.average_rms = 0
        self.length = int(args.window * args.samplerate / (1000 * args.downsample))
        self.plotdata = np.zeros((self.length, len(args.channels)))
        self.fig, self.ax = plt.subplots()
        self.lines = self.ax.plot(self.plotdata)
        self.setup_plot()
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=args.interval, save_count=200, blit=False)  # Set save_count and turn off blit

    def setup_plot(self):
        if len(self.args.channels) > 1:
            self.ax.legend([f'channel {c}' for c in self.args.channels], loc='lower left', ncol=len(self.args.channels))
        self.ax.axis((0, len(self.plotdata), -1, 1))
        self.ax.set_yticks([0])
        self.ax.yaxis.grid(True)
        self.ax.tick_params(bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)
        self.fig.tight_layout(pad=0)

    def update_plot(self, frame):
        rms_values = []
        while True:
            try:
                data = self.queue.get_nowait()
            except queue.Empty:
                break
            if data.size > 0:
                rms = np.sqrt(np.mean(data**2))
                rms_values.append(rms)
        if rms_values:
            average_rms = np.mean(rms_values)
            print(f"{average_rms}")  # Output the RMS value to stdout
        return self.lines
    
    def get_average_rms(self):
        return AudioVisualizer.average_rms

class CLIHandler:
    def __init__(self):
        self.parser = self.create_parser()
        self.args = self.parse_args()

    def create_parser(self):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-l', '--list-devices', action='store_true', help='show list of audio devices and exit')
        return parser

    def parse_args(self):
        args, remaining = self.parser.parse_known_args()
        if args.list_devices:
            print(sd.query_devices())
            self.parser.exit(0)
        self.parser = argparse.ArgumentParser(
            description='Plot the live microphone signal(s) with matplotlib.',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[self.parser])
        self.add_arguments()
        return self.parser.parse_args(remaining)

    def add_arguments(self):
        self.parser.add_argument('channels', type=int, default=[1], nargs='*', metavar='CHANNEL', help='input channels to plot (default: the first)')
        self.parser.add_argument('-d', '--device', type=self.int_or_str, help='input device (numeric ID or substring)')
        self.parser.add_argument('-w', '--window', type=float, default=200, metavar='DURATION', help='visible time slot (default: %(default)s ms)')
        self.parser.add_argument('-i', '--interval', type=float, default=30, help='minimum time between plot updates (default: %(default)s ms)')
        self.parser.add_argument('-b', '--blocksize', type=int, help='block size (in samples)')
        self.parser.add_argument('-r', '--samplerate', type=float, help='sampling rate of audio device')
        self.parser.add_argument('-n', '--downsample', type=int, default=10, metavar='N', help='display every Nth sample (default: %(default)s)')

    @staticmethod
    def int_or_str(text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

if __name__ == '__main__':
    cli_handler = CLIHandler()
    if any(c < 1 for c in cli_handler.args.channels):
        cli_handler.parser.error('argument CHANNEL: must be >= 1')
    mapping = [c - 1 for c in cli_handler.args.channels]  # Channel numbers start with 1

    if cli_handler.args.samplerate is None:
        device_info = sd.query_devices(cli_handler.args.device, 'input')
        cli_handler.args.samplerate = device_info['default_samplerate']

    audio_stream = AudioStream(cli_handler.args)
    visualizer = AudioVisualizer(audio_stream.queue, cli_handler.args)
    audio_stream.start()
