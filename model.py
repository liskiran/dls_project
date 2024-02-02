import torch
import subprocess
import os
from IPython.display import display, Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


async def predict(
    model_path: str = "best.pt",
    images_path: str = "/temp_folder/telegram_photos/",
):
    os.makedirs(images_path, exist_ok=True)
    run_model_cmd = f"yolo task=detect mode=predict model={model_path} conf=0.1 source=/temp_folder/telegram_photos/ save=True".split(
        " "
    )
    subprocess.run(run_model_cmd)
