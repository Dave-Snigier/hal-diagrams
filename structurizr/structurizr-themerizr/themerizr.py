"""
Creates a Structurizr theme.json file from a directory of SVG images.
"""
import json
import os
import io
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import click
import cairosvg
from PIL import Image
# from pprint import pprint


def convert_svg_to_png(
    svg_filepath: str, png_filepath: str, max_height: int, max_width: int
) -> None:
    """
    Converts an SVG file to a PNG file with specified maximum dimension.
    The output image will maintain its aspect ratio.
    """
    converted_png = cairosvg.svg2png(url=svg_filepath)
    im = Image.open(io.BytesIO(converted_png))  # type: ignore
    print("hello")
    original_width, original_height = im.size

    # Calculate the scale to maintain aspect ratio
    # scale_w = min(max_width / original_width, 1)
    scale_w = max_width / original_width
    scale_h = max_height / original_height
    scale = min(scale_w, scale_h)

    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    # Convert using cairosvg
    cairosvg.svg2png(
        url=svg_filepath,
        write_to=png_filepath,
        output_width=new_width,
        output_height=new_height,
    )


# def convert_svg_to_png(
#     svg_filepath: str, png_filepath: str, height: int, width: int
# ) -> None:
#     """
#     Converts an SVG file to a PNG file with specified dimensions.
#     ...
#     """
#     cairosvg.svg2png(
#         url=svg_filepath,
#         write_to=png_filepath,
#         output_height=height,
#         output_width=width,
#     )


def process_png_files(source: str, target: str, files: List[str]) -> List[str]:
    """
    copies PNG files from source to target directory and returns a list of filenames.
    """
    processed_files = []

    for png_file in files:
        source_filepath = os.path.join(source, png_file)
        target_filepath = os.path.join(target, png_file)
        os.system(f"cp {source_filepath} {target_filepath}")
        processed_files.append(png_file)

    return processed_files


def create_theme_json(target: str, prefix: str, image_files: List[str]) -> None:
    """
    Creates a theme.json file in the Structurizr theme format with the provided image files.

    :param target: The target directory where theme.json will be written.
    :param prefix: The prefix for the tags in theme.json.
    :param image_files: The list of image filenames that have been converted.
    """
    theme_data = {
        "name": "Custom Structurizr Theme",
        "description": "A custom theme for Structurizr",
        "elements": [],
    }

    for image_file in image_files:
        theme_data["elements"].append(
            {
                "tag": f"{prefix}/{image_file.replace('_', ' ').rsplit('.', 1)[0]}",
                "icon": os.path.join(image_file),
            }
        )

    with open(os.path.join(target, "theme.json"), "w", encoding="utf-8") as theme_file:
        json.dump(theme_data, theme_file, indent=2)


def convert_images_concurrently(
    source: str, target: str, height: int, width: int, files: List[str]
) -> List[str]:
    """
    Converts a list of SVG files to PNG format concurrently using a ThreadPoolExecutor.

    :param source: The source directory containing SVG images.
    :param target: The destination directory for converted PNG images.
    :param height: The height to which the SVG images will be resized.
    :param width: The width to which the SVG images will be resized.
    :param files: The list of SVG filenames to convert.
    :return: A list of converted PNG filenames.
    """
    converted_files = []

    with ThreadPoolExecutor() as executor:
        future_to_png = {
            executor.submit(
                convert_svg_to_png,
                os.path.join(source, svg_file),
                os.path.join(target, svg_file.replace(".svg", ".png")),
                height,
                width,
            ): svg_file.replace(".svg", ".png")
            for svg_file in files
        }

        for future in as_completed(future_to_png):
            res = future_to_png[future]
            if future.exception() is not None:
                click.echo(
                    f"File {res} encountered an error during conversion: {future.exception()}"
                )
            else:
                converted_files.append(res)
                click.echo(f"File {res} converted successfully.")

    return converted_files


@click.command()
@click.argument("source", type=click.Path(exists=True, file_okay=False))
@click.argument("target", type=click.Path())
@click.option(
    "--height", default=64, type=int, help="Maximum height of the PNG images."
)
@click.option("--width", default=256, type=int, help="Maximum width of the PNG images.")
@click.option("--prefix", help="Prefix for the tags in theme.json.", required=True)
def convert(source: str, target: str, height: int, width: int, prefix: str) -> None:
    """
    Converts all SVG images in the source directory to PNG format
    with the specified size constraints and
    writes a theme.json file for a Structurizr theme.
    ...
    """
    if not os.path.exists(target):
        os.makedirs(target)

    svg_files = [f for f in os.listdir(source) if f.endswith(".svg")]
    png_files = [f for f in os.listdir(source) if f.endswith(".png")]

    png_processed_files = process_png_files(source, target, png_files)

    converted_files = convert_images_concurrently(
        source, target, height, width, svg_files
    )

    all_files = png_processed_files + converted_files

    create_theme_json(target, prefix, all_files)

    click.echo(
        f"Conversion complete. PNG files and theme.json are saved in '{target}'."
    )


if __name__ == "__main__":
    convert()  # pylint: disable=no-value-for-parameter
