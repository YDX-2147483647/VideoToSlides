import os
import cv2
import img2pdf
import glob
import shutil
import multiprocessing

def extract_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception(f'unable to open file {video_path}')

    temp_path = os.path.join(os.path.dirname(video_path), os.path.basename(video_path).replace('.mp4', "_PDF_TEMP"))
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
    os.makedirs(temp_path, exist_ok=True)

    fgbg = cv2.createBackgroundSubtractorMOG2(
        history=4, varThreshold=16, detectShadows=False)

    cnt = 0
    (W, H) = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)/20),
              int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/20))
    orig = None
    frame_cnt = 0
    while True:
        ret = cap.grab()
        if ret is not True:
            break

        frame_cnt += 1
        if frame_cnt % 3 != 0:
            continue

        ret, frame = cap.retrieve()
        if ret is not True:
            break

        frame_resized = cv2.resize(frame, (W, H))

        p_diff = (cv2.countNonZero(fgbg.apply(
            frame_resized)) / float(W * H)) * 100

        if p_diff < 0.2:
            orig = frame
        elif p_diff > 2 and orig is not None:
            cnt += 1
            cv2.imencode('.png', orig)[1].tofile(os.path.join(temp_path, f"{cnt:03}.png"))
            orig = None

    if orig is not None:
        cnt += 1
        cv2.imencode('.png', orig)[1].tofile(os.path.join(temp_path, f"{cnt:03}.png"))
        orig = None

    cap.release()

    with open(video_path.replace(".mp4", ".pdf"), "wb") as f:
        f.write(img2pdf.convert(sorted(glob.glob(f"{temp_path}/*.png"))))
    shutil.rmtree(temp_path)

    os.remove(video_path)
    print(f'[SUCCESS] File: {video_path}')

    return

if __name__ == "__main__":
    folder_path = "./videos"
    video_list = glob.glob(f"{folder_path}/*vga*.mp4")

    with multiprocessing.Pool(8) as pool:
        pool.map(extract_video, video_list)

    # for video_path in video_list:
    #     extract_video(video_path)
