import os
from pathlib import Path

import ffmpeg


def convert_jpg_to_mp4(
    image_folder: str, output_video_path: str, fps: int = 30
) -> None:
    """Convert a folder of images to an MP4 video.

    Example
    -------
    >>> video_path = 'video.mp4'
    >>> output_folder = 'video_jpg'
    >>> convert_mp4_to_jpg(video_path, output_folder)
    """
    input_pattern = os.path.join(image_folder, "%05d.jpg")
    (
        ffmpeg.input(input_pattern, framerate=fps)
        .output(
            str(output_video_path), vcodec="mpeg4", pix_fmt="yuv420p", loglevel="error"
        )
        .run(overwrite_output=True)
    )


def convert_mp4_to_jpg(video_path: str, output_folder: str, quality: int = 2) -> None:
    """Convert an MP4 video to a folder of JPG images.

    Example
    -------
    >>> video_path = 'video.mp4'
    >>> output_folder = 'video_jpg'
    >>> convert_mp4_to_jpg(video_path, output_folder)
    """
    os.makedirs(output_folder, exist_ok=True)
    output_pattern = os.path.join(output_folder, "%05d.jpg")

    assert (
        2 <= quality <= 31
    ), "Quality must be between 2 and 31 (inclusive), lower is better."
    ffmpeg.input(video_path).output(output_pattern, **{"q:v": quality}).run()


def rename_files_in_folder(
    folder_path: str | Path, zero_padding_length: int = 5
) -> None:
    """Rename files in a folder by padding the numeric part of the filename with zeros."""
    import re

    for filename in os.listdir(folder_path):
        # Use regular expression to find numeric part in the filename
        match = re.search(r"(\d+)", filename)
        if match:
            # Extract numeric part and pad with zeros
            numeric_part = match.group(0)
            padded_numeric_part = numeric_part.zfill(zero_padding_length)

            # Replace numeric part in filename with padded version
            new_filename = re.sub(r"\d+", padded_numeric_part, filename).strip()

            try:
                # Rename the file
                os.rename(
                    os.path.join(folder_path, filename),
                    os.path.join(folder_path, new_filename),
                )
                print(f"Renamed {filename} to {new_filename}")
            except Exception as e:
                print(f"Error renaming {filename}: {e}")


def sam2_output_export(
    video_segments, frame_names: list[str | Path], output_dir: str | Path = "output"
) -> None:
    """Export SAM2 output to masks and visualization images.

    Example
    -------
    >>> video_predictor = build_sam2_video_predictor(CONFIG, CHECKPOINT, device=DEVICE, apply_postprocessing=False)
    >>> frame_names = list(IMAGES_DIR.glob('*.jpg'))
    >>> frame_names.sort(key=lambda p: int(p.stem))
    >>> video_segments = {}  # video_segments contains the per-frame segmentation results
    >>> for out_frame_idx, out_obj_ids, out_mask_logits in video_predictor.propagate_in_video(inference_state):
    >>>     video_segments[out_frame_idx] = {
    >>>         out_obj_id: (out_mask_logits[i] > 0.0).cpu().numpy()
    >>>         for i, out_obj_id in enumerate(out_obj_ids)
    >>>     }
    >>> sam2_output_export(video_segments, frame_names, IMAGES_DIR / 'sam2_output')
    """
    import numpy as np
    from PIL import Image
    from tqdm import tqdm

    out_dir = Path(output_dir)
    masks_dir = out_dir / "masks"
    vis_dir = out_dir / "visualization"

    masks_dir.mkdir(parents=True, exist_ok=True)
    vis_dir.mkdir(parents=True, exist_ok=True)

    for out_frame_idx in tqdm(range(0, len(frame_names)), desc="Exporting SAM2 output"):
        for out_obj_id, out_mask in video_segments[out_frame_idx].items():
            # Save mask
            mask = out_mask.squeeze()
            mask_img = Image.fromarray(
                (mask * 255).astype(np.uint8)
            )  # Convert mask to 0-255 range
            mask_img.save(masks_dir / f"{out_frame_idx:05d}.png")

            # Save overlay
            mask_rgba = np.zeros((*mask.shape, 4), dtype=np.uint8)
            mask_rgba[..., 0] = 255  # Red
            mask_rgba[..., 3] = (mask > 0.5) * 102  # Alpha channel with transparency
            mask_img = Image.fromarray(mask_rgba, "RGBA")
            frame_img_rgba = Image.open(frame_names[out_frame_idx]).convert("RGBA")
            overlay_img = Image.alpha_composite(frame_img_rgba, mask_img)
            overlay_img.convert("RGB").save(vis_dir / f"{out_frame_idx:05d}.jpg")
