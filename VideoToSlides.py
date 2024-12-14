import os
import shutil
from itertools import count
from pathlib import Path
from sys import argv

import cv2
from rich.progress import track


def extract_video(video_path: Path):
    cap = cv2.VideoCapture(video_path)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if not cap.isOpened():
        raise Exception(f"unable to open file {video_path}")

    temp_path = video_path.parent / f"{video_path.stem}_PDF_TEMP"
    os.makedirs(temp_path, exist_ok=True)

    fgbg = cv2.createBackgroundSubtractorMOG2(
        history=4, varThreshold=16, detectShadows=False
    )

    (W, H) = (
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 20),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 20),
    )
    orig = None
    frame_cnt = 0
    cnt = 0
    # frame_cnt = 102000, cnt = 52
    for _ in track(count(), total=num_frames):
        # https://vuamitom.github.io/2019/12/13/fast-iterate-through-video-frames.html#:~:text=Opencv%20grab%20and%20retrieve%20function%20can%20be
        ret = cap.grab()
        if ret is not True:
            break

        frame_cnt += 1
        if frame_cnt % 3 != 0:
            continue

        ret, frame = cap.retrieve()
        if ret is not True:
            break
        # if frame_cnt <= 102000:
        #     if frame_cnt == 102000:
        #       cnt = 53
        #     continue

        frame_resized = cv2.resize(frame, (W, H))

        p_diff = (cv2.countNonZero(fgbg.apply(frame_resized)) / float(W * H)) * 100

        if p_diff < 0.2:
            orig = frame
        elif p_diff > 2.4 and orig is not None:
            cnt += 1
            print(f"{frame_cnt = }, {cnt = }")
            cv2.imencode(".png", orig)[1].tofile(
                os.path.join(temp_path, f"{cnt:03}.png")
            )
            orig = None

    if orig is not None:
        cnt += 1
        cv2.imencode(".png", orig)[1].tofile(os.path.join(temp_path, f"{cnt:03}.png"))
        orig = None

    cap.release()

    if (
        input(
            f"Convert to PDF using img2pdf now? (You may want to manually remove redundant pages in “{temp_path}” first, or skip this step and convert with your external tools.) [Y/n]"
        ).lower()
        == "y"
    ):
        import img2pdf

        with open(video_path.with_suffix(".pdf"), "wb") as f:
            f.write(img2pdf.convert(sorted(temp_path.glob("*.png"))))

        if input(f"Remove frames “{temp_path}”? [y/N]").lower() == "y":
            shutil.rmtree(temp_path)
    print(f"[SUCCESS] File: {video_path}")

    return


if __name__ == "__main__":
    video = Path(argv[1])
    assert video.exists()

    extract_video(video)
