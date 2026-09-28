"""
Send the DJI stream from MediaMTX into "OBS Virtual Camera", so the Mindstorms
app (Machine Learning > Camera Input) can pick it. The OBS app itself does not
need to be open; only its virtual camera driver (installed with OBS) is used.

    DJI Action 5 --RTMP--> MediaMTX --RTSP--> this script --> OBS Virtual Camera --> Mindstorms

Usage (MediaMTX running, DJI streaming to rtmp://<PC-IP>:1935/live/action5):
    python stream_to_vcam.py
    python stream_to_vcam.py --url rtsp://127.0.0.1:8554/live/action5 --preview

Close the OBS app (or at least stop its own virtual camera) first; only one
program can drive the OBS virtual camera at a time.
"""

import argparse
import os
import socket
import threading
import time

# Low-latency RTSP over TCP (must be set before OpenCV opens the stream).
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp|fflags;nobuffer|flags;low_delay|max_delay;0"
# Hide FFmpeg's "DESCRIBE failed: 404" noise while waiting for the DJI; our own log says the same.
os.environ["OPENCV_FFMPEG_LOGLEVEL"] = "-8"

import cv2  # noqa: E402
import numpy as np  # noqa: E402
import pyvirtualcam  # noqa: E402


def log(msg):
    print(f"{time.strftime('%H:%M:%S')} {msg}", flush=True)


def local_ip():
    """IP of the adapter that reaches the LAN (no packet is actually sent)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "<this PC's IP - run ipconfig>"
    finally:
        s.close()


def print_banner():
    ip = local_ip()
    line = "=" * 64
    print(line)
    print("  1. In DJI Mimo: LIVESTREAM > RTMP, enter this address:")
    print(f"        rtmp://{ip}:1935/live/action5")
    print("  2. Browser preview (optional):  http://127.0.0.1:8889/live/action5")
    print("  3. Mindstorms: Machine Learning > Camera Input > OBS Virtual Camera")
    print(line)
    print("  Keep this window open. Close it to stop the camera.")
    print(line, flush=True)


def placeholder(width, height, text):
    img = np.full((height, width, 3), 32, np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    (tw, th), _ = cv2.getTextSize(text, font, 1.0, 2)
    cv2.putText(img, text, ((width - tw) // 2, (height + th) // 2), font, 1.0, (200, 200, 200), 2, cv2.LINE_AA)
    return img


def letterbox(frame, width, height):
    h, w = frame.shape[:2]
    if (w, h) == (width, height):
        return frame
    scale = min(width / w, height / h)
    nw, nh = int(w * scale), int(h * scale)
    out = np.zeros((height, width, 3), np.uint8)
    x, y = (width - nw) // 2, (height - nh) // 2
    out[y:y + nh, x:x + nw] = cv2.resize(frame, (nw, nh), interpolation=cv2.INTER_AREA)
    return out


class LatestFrame:
    """Reads the stream on its own thread and keeps only the newest frame, so lag never builds up."""

    def __init__(self, url):
        self.url = url
        self.lock = threading.Lock()
        self.frame = None
        self.stamp = 0.0
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        while True:
            log(f"Opening {self.url}")
            cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
            if cap.isOpened():
                log("Stream connected")
            while cap.isOpened():
                ok, frame = cap.read()
                if not ok:
                    break
                with self.lock:
                    self.frame, self.stamp = frame, time.monotonic()
            cap.release()
            log("No stream (is the DJI streaming to MediaMTX?). Retrying in 2 s...")
            time.sleep(2)

    def get(self, max_age=2.0):
        with self.lock:
            if self.frame is None or time.monotonic() - self.stamp > max_age:
                return None
            return self.frame


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default="rtsp://127.0.0.1:8554/live/action5", help="RTSP stream to read")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--preview", action="store_true", help="also show a preview window")
    args = ap.parse_args()

    print_banner()
    source = LatestFrame(args.url)
    waiting = placeholder(args.width, args.height, "Waiting for DJI stream...")

    try:
        cam = pyvirtualcam.Camera(args.width, args.height, args.fps, fmt=pyvirtualcam.PixelFormat.BGR, backend="obs")
    except Exception as e:
        log(f"Could not start OBS Virtual Camera: {e}")
        log("Close the OBS app (or stop its virtual camera) and try again.")
        return

    with cam:
        log(f"Sending to '{cam.device}' at {args.width}x{args.height} @ {args.fps} fps. Ctrl+C to stop.")
        try:
            while True:
                frame = source.get()
                out = letterbox(frame, args.width, args.height) if frame is not None else waiting
                cam.send(out)
                if args.preview:
                    cv2.imshow("DJI -> OBS Virtual Camera", out)
                    if cv2.waitKey(1) == 27:  # Esc
                        break
                cam.sleep_until_next_frame()
        except KeyboardInterrupt:
            pass
    log("Stopped.")


if __name__ == "__main__":
    main()
