from RealtimeSTT import AudioToTextRecorder
from modules.typer_agent import TyperAgent
from modules.utils import create_session_logger_id, setup_logging
import logging
import typer
from typing import List
import os

app = typer.Typer()


@app.command()
def ping():
    print("pong")


@app.command()
def deep(
    typer_file: str = typer.Option(
        ..., "--typer-file", "-f", help="Path to typer commands file"
    ),
    scratchpad: List[str] = typer.Option(
        ..., "--scratchpad", "-s", help="List of scratchpad files"
    ),
):
    """Run STT interface that processes speech into typer commands"""
    assistant, typer_file, scratchpad = TyperAgent.build_assistant(
        typer_file, scratchpad
    )

    print("🎤 Speak now... (press Ctrl+C to exit)")

    """
    Play with these configuration settings.

    recorder_config = {
        'spinner': False,
        'model': 'large-v3',
        #'realtime_model_type': 'medium.en',
        'realtime_model_type': 'tiny.en',
        'language': 'en',
        'silero_sensitivity': 0.4,
        'webrtc_sensitivity': 3,
        'post_speech_silence_duration': unknown_sentence_detection_pause,
        'min_length_of_recording': 1.1,
        'min_gap_between_recordings': 0,
        'enable_realtime_transcription': True,
        'realtime_processing_pause': 0.05,
        'on_realtime_transcription_update': text_detected,
        'silero_deactivity_detection': True,
        'early_transcription_on_silence': 0,
        'beam_size': 5,
        'beam_size_realtime': 1,
        'batch_size': 4,
        'realtime_batch_size': 4,
        'no_log_file': True,
        'initial_prompt_realtime': (
            "End incomplete sentences with ellipses.\n"
            "Examples:\n"
            "Complete: The sky is blue.\n"
            "Incomplete: When the sky...\n"
            "Complete: She walked home.\n"
            "Incomplete: Because he...\n"
        )
    }
    
    """
    recorder = AudioToTextRecorder(
        # wake_words="deep"
        spinner=False,
        enable_realtime_transcription=False,
        # realtime_processing_pause=0.3,
        # post_speech_silence_duration=0.3,
        # model="large-v3",
        model="tiny.en",
        realtime_model_type="tiny.en",
        # realtime_model_type="large-v3",
        language="en",
        print_transcription_time=True,
    )

    def process_text(text):
        print(f"\n🎤 Heard: {text}")
        try:
            if "deep" not in text.lower():
                print("🤖 Not deep - ignoring")
                return
            output = assistant.process_text(text, typer_file, scratchpad)
            print(f"🤖 Response:\n{output}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    while True:
        recorder.text(process_text)


if __name__ == "__main__":
    app()