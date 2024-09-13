import gradio as gr
import sys

class Logger:
    def __init__(self):
        self.terminal = sys.stdout
        self.log = []

    def write(self, message):
        self.terminal.write(message)
        self.log.append(message)
        
    def flush(self):
        self.terminal.flush()

    def isatty(self):
        return False

    def get_logs(self):
        return ''.join(self.log)

logger = Logger()
sys.stdout = logger

def test(x):
    print("This is a test")
    print(f"Your function is running with input {x}...")
    return x

def read_logs():
    return logger.get_logs()

with gr.Blocks() as demo:
    with gr.Row():
        input = gr.Textbox()
        output = gr.Textbox()
    btn = gr.Button("Run")
    btn.click(test, input, output)
    
    logs = gr.Textbox()
    demo.load(read_logs, None, logs, every=1)
    
demo.queue().launch()