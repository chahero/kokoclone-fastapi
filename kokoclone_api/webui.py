from pathlib import Path

import gradio as gr

from .routes import SUPPORTED_LANGUAGES
from .service import get_clone_service


def create_gradio_app() -> gr.Blocks:
    def clone_voice(text, lang, ref_audio_path):
        if not text or not text.strip():
            raise gr.Error("Please enter some text.")
        if not ref_audio_path:
            raise gr.Error("Please upload or record a reference audio file.")

        output_path = str(Path("gradio_output.wav").resolve())
        get_clone_service().clone_text(
            text=text,
            lang=lang,
            reference_audio=ref_audio_path,
            output_path=output_path,
        )
        return output_path

    def convert_voice(source_audio_path, ref_audio_path):
        if not source_audio_path:
            raise gr.Error("Please upload or record a source audio file.")
        if not ref_audio_path:
            raise gr.Error("Please upload or record a reference audio file.")

        output_path = str(Path("gradio_convert_output.wav").resolve())
        get_clone_service().convert_audio(
            source_audio=source_audio_path,
            reference_audio=ref_audio_path,
            output_path=output_path,
        )
        return output_path

    with gr.Blocks() as demo:
        gr.Markdown(
            """
            <div style="text-align: center;">
                <h1>KokoClone</h1>
                <p>Generate multilingual speech and clone any target voice.</p>
            </div>
            """
        )

        with gr.Tabs():
            with gr.Tab("Text to Clone"):
                with gr.Row():
                    with gr.Column(scale=1):
                        text_input = gr.Textbox(
                            label="Text to Synthesize",
                            lines=4,
                            placeholder="Enter the text you want spoken...",
                        )
                        lang_input = gr.Dropdown(
                            label="Language",
                            choices=SUPPORTED_LANGUAGES,
                            value="en",
                        )
                        ref_audio_input = gr.Audio(
                            label="Reference Voice",
                            type="filepath",
                        )
                        submit_btn = gr.Button("Generate Clone", variant="primary")
                    with gr.Column(scale=1):
                        output_audio = gr.Audio(
                            label="Generated Cloned Audio",
                            interactive=False,
                        )

                submit_btn.click(
                    fn=clone_voice,
                    inputs=[text_input, lang_input, ref_audio_input],
                    outputs=output_audio,
                )

            with gr.Tab("Audio to Clone"):
                with gr.Row():
                    with gr.Column(scale=1):
                        source_audio_input = gr.Audio(
                            label="Source Audio",
                            type="filepath",
                        )
                        ref_audio_convert_input = gr.Audio(
                            label="Reference Voice",
                            type="filepath",
                        )
                        convert_btn = gr.Button("Convert Voice", variant="primary")
                    with gr.Column(scale=1):
                        convert_output_audio = gr.Audio(
                            label="Converted Audio",
                            interactive=False,
                        )

                convert_btn.click(
                    fn=convert_voice,
                    inputs=[source_audio_input, ref_audio_convert_input],
                    outputs=convert_output_audio,
                )

    return demo

