from notifypy import Notify
import mss
import json
import time
import logging
from PIL import Image
import traceback
import transformers
from vllm import LLM, SamplingParams
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
import typer
from typing_extensions import Annotated
from pathlib import Path


# Typer CLI
app = typer.Typer(
    rich_markup_mode="rich",
)
state = {"verbose": False, "super_verbose": False}


# Model config
MODEL_PATH = "OpenGVLab/InternVL2-2B"
TORCH_DTYPE = "bfloat16"

TEMP = 0.2
MAX_CONTEXT_LEN = 4096
MAX_TOKENS = 128
QUESTION = """
Task: Analyze the given computer screenshot to determine if it shows evidence of focused, productive activity or potentially distracting activity, then provide an appropriate titled response.

Instructions:
1. Examine the screenshot carefully.
2. Look for indicators of focused, productive activities such as:
   - Code editors or IDEs in use
   - Document editing software with substantial text visible
   - Spreadsheet applications with data or formulas
   - Research papers or educational materials being read
   - Professional design or modeling software in use
   - Terminal/command prompt windows with active commands
3. Identify potentially distracting activities, including:
   - Social media websites
   - Video streaming platforms
   - Unrelated news websites or apps
   - Online shopping sites
   - Music or video players
   - Messaging apps
   - Games or gaming platforms
4. Consider the context: a coding-related YouTube video might be considered focused activity for a programmer.

Response Format:
Return a single JSON object with the following fields:
- is_distracted (boolean): value (true if the screenshot primarily shows evidence of distraction, false if it shows focused activity)
- title (string): 1-liner snarky title to catch the user's attention (only if is_distracted is true, otherwise an empty string)
- message (string): 1-liner snarky message to encourage the user to refocus (only if is_distracted is true, otherwise an empty string)

Example responses:
{"is_distracted": false, "title": "", "message": ""}
{"is_distracted": true, "title": "Uh-oh!", "message": "Looks like someone's getting a little distracted..."}

Important:
- Only write a title and message if is_distracted is true.
- Provide only one JSON object as your complete response.
- Ensure the JSON is valid and properly formatted.
- Do not include any explanations or additional text outside the JSON object.
- Use true/false for the boolean value, not 1/0.
"""

# Notifypy
NOTIFICATION_INTERVAL = 8  # seconds
notification = Notify(
    default_application_name="Modeldemo",
    default_notification_urgency="critical",
    default_notification_icon=str(Path(__file__).parent / "icon.png"),
    default_notification_audio=str(Path(__file__).parent / "sound.wav"),
)


# Helper fns
def capture_screenshot() -> Image:
    with mss.mss() as sct:
        # Capture the entire screen
        monitor = sct.monitors[0]
        sct_img = sct.grab(monitor)
        return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")


def load_internvl() -> tuple[LLM, str, list[int]]:
    llm = LLM(
        model=MODEL_PATH,
        tokenizer=MODEL_PATH,
        tokenizer_mode="auto",
        trust_remote_code=True,
        dtype=TORCH_DTYPE,
        max_num_seqs=1,
        max_model_len=MAX_CONTEXT_LEN,
    )

    tokenizer = llm.get_tokenizer()
    messages = [{"role": "user", "content": f"<image>\n{QUESTION}"}]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    # Stop tokens for InternVL
    # models variants may have different stop tokens
    # please refer to the model card for the correct "stop words":
    # https://huggingface.co/OpenGVLab/InternVL2-2B#service
    stop_tokens = ["<|endoftext|>", "<|im_start|>", "<|im_end|>", "<|end|>"]
    stop_token_ids = [tokenizer.convert_tokens_to_ids(i) for i in stop_tokens]
    return llm, prompt, stop_token_ids


# Typer CLI
def run() -> None:
    if state["verbose"]:
        print("Press Ctrl+C to stop at any time.")
        with Progress(
            SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True
        ) as progress:
            progress.add_task("Downloading model...", total=None)
            llm, prompt, stop_token_ids = load_internvl()
        print("Model downloaded!")
    else:
        llm, prompt, stop_token_ids = load_internvl()

    sampling_params = SamplingParams(temperature=TEMP, max_tokens=MAX_TOKENS, stop_token_ids=stop_token_ids)
    while True:
        img = capture_screenshot()
        inputs = {
            "prompt": prompt,
            "multi_modal_data": {"image": img},
        }
        outputs = llm.generate(inputs, sampling_params=sampling_params)
        pred = outputs[0].outputs[0].text
        if state["super_verbose"]:
            print(f"Prediction: {pred}")

        try:
            format_pred = pred.split("```json")[1].split("```")[0].strip()
            format_pred = json.loads(format_pred)
            is_distracted, title, message = format_pred["is_distracted"], format_pred["title"], format_pred["message"]
            is_distracted = bool(is_distracted)
        except Exception as e:
            if state["verbose"]:
                print(f"Failed to parse prediction: {e}")
            continue

        if is_distracted:
            if state["verbose"]:
                print(f"[bold red] {title}\n{message} [/bold red]")
            notification.title = title
            notification.message = message
            notification.send(block=False)
            time.sleep(NOTIFICATION_INTERVAL)


@app.command(
    help="Stay [bold red]focused.[/bold red]",
    epilog="Made by [bold blue]Andrew Hinh.[/bold blue] :mechanical_arm::person_climbing:",
    context_settings={"allow_extra_args": False, "ignore_unknown_options": True},
)
def main(verbose: Annotated[int, typer.Option("--verbose", "-v", count=True)] = 0) -> None:
    try:
        state["verbose"] = verbose > 0
        state["super_verbose"] = verbose > 1
        vllm_logger = logging.getLogger("vllm")
        if state["super_verbose"]:
            transformers.logging.set_verbosity_debug()
            vllm_logger.setLevel(logging.DEBUG)
        elif state["verbose"]:
            transformers.logging.set_verbosity_warning()
            vllm_logger.setLevel(logging.WARNING)
        else:
            transformers.logging.set_verbosity_error()
            vllm_logger.setLevel(logging.ERROR)
        run()
    except KeyboardInterrupt:
        if state["verbose"]:
            print("\n\nExiting...")
    except Exception as e:
        if state["verbose"]:
            print(f"Failed with error: {e}")
            print(traceback.format_exc())
            print("\n\nExiting...")
