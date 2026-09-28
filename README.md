# DJI Action 5 → Mindstorms Machine Learning camera

Use the DJI Osmo Action 5 on the robot as a **wireless camera** for the LEGO
Mindstorms app's Machine Learning (image classification).

```
DJI Action 5 --WiFi (RTMP, via Mimo app)--> MediaMTX on laptop
     --> stream_to_vcam.py --> "OBS Virtual Camera" --> Mindstorms app
                                                            |
                                                   Bluetooth to the hub
```

## What's in this folder

| File | What it does |
|---|---|
| `1_Install_First_Time.bat` | One-time setup: installs Python, the Python packages, MediaMTX, and OBS Studio if missing |
| `2_Start_Camera.bat` | Starts everything. Shows the RTMP address to type into Mimo |
| `3_Stop_Camera.bat` | Stops everything |
| `stream_to_vcam.py` | Reads the DJI stream and sends it to OBS Virtual Camera |
| `mediamtx\` | [MediaMTX](https://github.com/bluenviron/mediamtx) video server that receives the DJI stream. Downloaded by `1_Install_First_Time.bat`; not stored in this repo |
| `requirements.txt` | Python packages used by the script |

The OBS Studio **app does not need to be open**. Only its "OBS Virtual Camera"
driver is used. Keep OBS closed while using this.

---

## Requirements

- Windows 10/11 laptop with WiFi
- DJI Osmo Action 5 (or any camera/app that can livestream to an RTMP address) and the DJI Mimo app
- LEGO Mindstorms app with the Machine Learning extension

## First time on a laptop (once)

1. Download this repo (green **Code** button → **Download ZIP**) and unzip it.
2. Double-click **`1_Install_First_Time.bat`** and wait until it says *Setup finished*.
3. The first time `2_Start_Camera.bat` runs, Windows Firewall asks about
   **mediamtx.exe**. Tick **both Private and Public** and click **Allow**, or
   the camera can't reach the laptop.

---

## Every time: step by step

### 1. Same WiFi
Connect the **laptop** and the **DJI Action 5** to the **same WiFi network**.
A 5 GHz home router is best. School or guest WiFi often blocks devices from
talking to each other; if that happens, use your own router or a phone hotspot.

### 2. Start the laptop side
Double-click **`2_Start_Camera.bat`**. A window opens showing something like:

```
  1. In DJI Mimo: LIVESTREAM > RTMP, enter this address:
        rtmp://192.168.1.11:1935/live/action5
```

Use the address **shown in your window**. The number changes when you change
WiFi networks. Leave the window open.

### 3. Start streaming from the camera (Mimo app on the phone)
1. Open **DJI Mimo** and connect to the Action 5.
2. Swipe to **LIVESTREAM** and choose **RTMP**.
3. Make sure the **camera** joins the same WiFi as the laptop.
4. Paste the `rtmp://...` address from step 2.
5. Set **720p** and the **lowest bitrate** for the least lag.
6. Start the livestream.

In the laptop window you should now see **`Stream connected`**.

### 4. (Optional) Check the picture
Open **http://127.0.0.1:8889/live/action5** in Chrome or Edge.

### 5. Use it in Mindstorms
1. Open the Mindstorms app → your project → **Machine Learning**.
2. Tap the **⚙ camera settings** icon on the camera preview.
3. **Camera Input** → **OBS Virtual Camera**.
4. The DJI picture appears. Capture image samples and train your model as usual.

If you still see the OBS logo, pick another camera and then OBS Virtual Camera
again, or restart the Mindstorms app.

### 6. When finished
Stop the livestream in Mimo, then double-click **`3_Stop_Camera.bat`**.

---

## Tips

- **Lag** is about 0.5–1 s over WiFi. Program the robot to move slowly or in
  short steps, and wait about 1 second after moving before trusting a
  detection.
- **Train with the real setup**: same camera position on the robot, same
  lighting, same 720p setting you'll use in the demo.
- Keep the router close to the robot; WiFi drops cause freezes.

## Troubleshooting

| Problem | Fix |
|---|---|
| Laptop window keeps saying *No stream* | Mimo isn't streaming, or the address is wrong. Check the camera and laptop are on the **same WiFi** and the address matches the one in the window. |
| Mimo says it can't connect | Firewall: allow `mediamtx.exe` (Windows Security → Firewall → Allow an app). Or the WiFi blocks device-to-device traffic: use your own router or a hotspot. |
| *Could not start OBS Virtual Camera* | OBS Studio is open with its virtual camera on. Close OBS and run `2_Start_Camera.bat` again. |
| Mindstorms shows the OBS logo | The script isn't running, or no stream yet. Check the laptop window says *Stream connected*, then reselect the camera. |
| Very laggy | 720p, lowest bitrate, 5 GHz WiFi, router close to the robot. |
| `python` not found | Run `1_Install_First_Time.bat` again. |
