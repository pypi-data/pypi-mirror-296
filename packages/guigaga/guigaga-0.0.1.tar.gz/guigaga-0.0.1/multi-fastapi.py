from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import gradio as gr

app = FastAPI()

HELLO_ROUTE = "/hello"
GOODBYE_ROUTE = "/goodbye"
iframe_dimensions = "height=300px width=1000px"

index_html = f'''
<h1>Put header here</h1>

<h3>
You can mount multiple gradio apps on a single FastAPI object for a multi-page app.
However if you mount a gradio app downstream of another gradio app, the downstream
apps will be stuck loading. 
</h3>

<h3>
So in particular if you mount a gradio app at the index route "/", then all your 
other mounted gradio apps will be stuck loading. But don't worry, you can still embed
your downstream gradio apps into the index route using iframes like I do here. In fact,
you probably want to do this anyway since its your index page, which you want to detail 
more fully with a jinja template. 
For a full example, you can see my <a href=https://yfu.one/>generative avatar webapp</a>
</h3>

<div>
<iframe src={HELLO_ROUTE} {iframe_dimensions}></iframe>
</div>

<div>
<iframe src={GOODBYE_ROUTE} {iframe_dimensions}></iframe>
</div>

'''

@app.get("/", response_class=HTMLResponse)
def index():
    return index_html


hello_app = gr.Interface(lambda x: "Hello, " + x + "!", "textbox", "textbox")
goodbye_app = gr.Interface(lambda x: "Goodbye, " + x + "!", "textbox", "textbox")


app = gr.mount_gradio_app(app, hello_app, path=HELLO_ROUTE)
app = gr.mount_gradio_app(app, goodbye_app, path=GOODBYE_ROUTE)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)