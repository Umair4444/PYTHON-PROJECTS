import gradio as gr

def greet(name, intensity,bolo):
    return "Hello, " + name + "!" * intensity + bolo
# interface
# demo = gr.Interface(
#     fn=greet,
#     inputs=["text", gr.Slider(value=2, minimum=1, maximum=10, step=1),'text'],
#     outputs=[gr.Textbox(label="greeting", lines=2)],
# )

#  blocks
# with gr.Blocks() as demo:
#     with gr.Row():
#         with gr.Column(scale=1):
#             text1 = gr.Textbox()
#             text2 = gr.Textbox()
#         with gr.Column(scale=4):
#             btn1 = gr.Button("Button 1")
#             btn2 = gr.Button("Button 2")

# tab
# with gr.Blocks() as demo:
#     with gr.Tab("Lion"):
#         gr.Image("lion.jpg")
#         gr.Button("New Lion")
#     with gr.Tab("Tiger"):
#         gr.Image("tiger.jpg")
#         gr.Button("New Tiger")

# group
with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Mental Health Checker")

    with gr.Group():
        gr.Markdown("### 👤 User Information")
        name = gr.Textbox(label="Name")
        age = gr.Slider(label="Age", minimum=10, maximum=100, step=1, value=25)

    with gr.Group():
        gr.Markdown("### 📋 Questionnaire")
        mood = gr.Radio(["Happy", "Sad", "Anxious", "Angry"], label="How are you feeling today?")
        sleep = gr.Slider(label="Hours of sleep", minimum=0, maximum=12, step=1, value=7)

    output = gr.Textbox(label="AI Response")
    submit_btn = gr.Button("🧾 Submit")

    def analyze(name, age, mood, sleep):
        return f"{name}, age {age}, you feel {mood.lower()} and slept {sleep} hours. Take care!"

    submit_btn.click(analyze, [name, age, mood, sleep], output)

demo.launch()

