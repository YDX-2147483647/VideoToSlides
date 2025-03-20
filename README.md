# VideoToSlides

**Inspired by [video2pdfslides](https://github.com/kaushikj/video2pdfslides).**

Compared with video2pdfsildes, not only has VideoToSlides a more accurate output, but can work it out faster.

```shell
$ uv run VideoToSlides.py path/to/video.mp4
frame_cnt = 483, cnt = 1
frame_cnt = 570, cnt = 2
…
frame_cnt = 266022, cnt = 168
Working... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸ 100% 0:00:01
Convert to PDF using img2pdf now? (You may want to manually remove redundant pages in “path/to/video_PDF_TEMP” first, or skip this step and convert with your external tools.) [Y/n]
[SUCCESS] File: path/to/video.mp4
```
