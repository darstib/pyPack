import cv2
import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# from io import BytesIO


def imgs_concat(*images, gsize=None, show_sub=False):
    """
    Concatenates multiple images into a grid.

    Parameters:
    - *images: Any number of image objects (numpy.ndarray, PIL.Image.Image, matplotlib.figure.Figure).
    - gsize (tuple): A tuple (x, y) representing the number of columns and rows, default is None; if used, should `gsize=(x, y)`
    - show_sub (bool): Whether to display individual images. Default is False.

    Returns:
    - concatenated_image (PIL.Image.Image): The concatenated PNG image.
    """

    if gsize is None:
        default_cols = 4
        num_images = len(images)
        columns = num_images if (num_images <= default_cols) else default_cols
        rows = (num_images + columns - 1) // columns
        gsize = (columns, rows)
    x, y = gsize
    total_cells = x * y

    processed_images = []
    for img in images:
        if isinstance(img, plt.Figure):
            img = fig_to_img(img)
            if not show_sub:
                plt.close(img)
        elif isinstance(img, plt.Axes):
            fig = img.get_figure()
            img = fig_to_img(fig)
            if not show_sub:
                plt.close(fig)
        elif isinstance(img, Image.Image):
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        elif isinstance(img, np.ndarray):
            pass
        else:  # sns.axisgrid.JointGrid, sns.axisgrid.FacetGrid
            try:
                img = fig_to_img(img.fig)
                if not show_sub:
                    plt.close(img.fig)
            except:
                raise TypeError(f"Unsupported image type: {type(img)}")
        processed_images.append(img)

    if len(processed_images) < total_cells:
        img_height, img_width = processed_images[0].shape[:2]
        black_image = np.zeros_like(
            processed_images[0]
        )  # use black image as placeholder
        processed_images += [black_image] * (total_cells - len(processed_images))
    else:
        processed_images = processed_images[:total_cells]

    img_height, img_width = processed_images[0].shape[:2]
    resized_images = [
        cv2.resize(img, (img_width, img_height)) for img in processed_images
    ]

    rows = []
    for row in range(y):
        row_images = resized_images[row * x : (row + 1) * x]
        row_concat = np.hstack(row_images)
        rows.append(row_concat)

    concatenated_ndarray = np.vstack(rows)
    concatenated_rgb = cv2.cvtColor(concatenated_ndarray, cv2.COLOR_BGR2RGB)
    concatenated_image = Image.fromarray(concatenated_rgb)
    return concatenated_image


def fig_to_img(fig):
    """
    Converts a Matplotlib figure to an OpenCV image.

    Parameters:
    - fig (matplotlib.figure.Figure): The Matplotlib figure to convert.

    Returns:
    - img (numpy.ndarray): The image in BGR format suitable for OpenCV.
    """
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img = Image.open(buf).convert("RGB")
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    buf.close()
    return img


def fig_to_img(fig):
    """
    Converts a Matplotlib figure to an OpenCV image.

    Parameters:
    - fig (matplotlib.figure.Figure): The Matplotlib figure to convert.

    Returns:
    - img (numpy.ndarray): The image in BGR format suitable for OpenCV.
    """
    canvas = FigureCanvas(fig)
    canvas.draw()
    width, height = fig.get_size_inches() * fig.get_dpi()
    image = np.frombuffer(canvas.tostring_rgb(), dtype="uint8").reshape(
        int(height), int(width), 3
    )
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image
