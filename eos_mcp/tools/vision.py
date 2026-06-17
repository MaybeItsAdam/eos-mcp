from ..app import mcp


@mcp.tool()
def capture_visualizer(window_title: str = "Augment3d"):
    """Captures the 3D visualizer window so the lighting state can be verified.

    Locates the visualizer window, brings it to the foreground to force the GPU to
    render the current lighting state, pauses briefly for the frame to draw, then takes
    a screenshot and returns it as a PNG image. On Windows the capture is cropped to the
    window; on macOS it falls back to the full primary monitor. Returns an error string
    (never raises) if anything fails, so the OSC listener thread is never endangered.

    Args:
        window_title: The name of the visualizer window (defaults to "Augment3d").
    """
    import sys
    import time

    try:
        import mss
        import mss.tools
        from fastmcp.utilities.types import Image
    except Exception as e:  # noqa: BLE001 - degrade gracefully if a dep is missing
        return f"Error: vision dependencies unavailable ({e}). Install with: pip install mss"

    # --- Step 1: Bring the window to the foreground (OS dependent) ---
    window_box = None

    # WINDOWS IMPLEMENTATION
    if sys.platform.startswith("win"):
        try:
            import pygetwindow as gw

            windows = gw.getWindowsWithTitle(window_title)
            if not windows:
                return f"Error: Window containing '{window_title}' not found."
            win = windows[0]
            if win.isMinimized:
                win.restore()
            win.activate()
            window_box = {
                "top": win.top,
                "left": win.left,
                "width": win.width,
                "height": win.height,
            }
        except Exception as e:  # noqa: BLE001
            print(f"Windows window focus failed: {e}")

    # macOS IMPLEMENTATION
    elif sys.platform == "darwin":
        try:
            import os

            # Bring the matching application to the front via AppleScript. We cannot
            # reliably read the window rectangle here, so window_box stays None and we
            # fall back to capturing the full primary monitor below.
            safe_title = window_title.replace('"', "").replace("'", "")
            script = (
                'tell application "System Events" to set frontmost of first process '
                f'whose name contains "{safe_title}" to true'
            )
            os.system(f"osascript -e '{script}'")
            time.sleep(0.2)
        except Exception as e:  # noqa: BLE001
            print(f"macOS window focus failed: {e}")

    # --- Step 2: Pause for hardware-accelerated rendering ---
    # 3D engines need a split second to draw frames once brought to the front.
    time.sleep(0.3)

    # --- Step 3: Capture the frame via MSS ---
    try:
        with mss.mss() as sct:
            # Use the targeted window box if we got one, otherwise the primary monitor.
            monitor = window_box if window_box else sct.monitors[1]
            sct_img = sct.grab(monitor)
            png_bytes = mss.tools.to_png(sct_img.rgb, sct_img.size)
            return Image(data=png_bytes, format="png")
    except Exception as e:  # noqa: BLE001
        return f"Screenshot capture failed: {e}"


@mcp.tool()
def capture_camera(source: str = "0"):
    """Captures a single frame from a live camera feed (USB webcam or RTSP IP stream).

    Returns the frame as a JPEG image, or an error string (never raises) if the source
    cannot be opened or no frame is available, so the OSC listener thread is never
    endangered.

    Args:
        source: "0" or "1" for local USB webcams, or an "rtsp://..." URL for IP cameras.
    """
    try:
        import cv2
        from fastmcp.utilities.types import Image
    except Exception as e:  # noqa: BLE001 - degrade gracefully if a dep is missing
        return f"Error: camera dependencies unavailable ({e}). Install with: pip install opencv-python"

    # A digit string is a local camera index; anything else (e.g. an RTSP URL) is a path.
    cam_source = int(source) if source.isdigit() else source

    cap = cv2.VideoCapture(cam_source)
    try:
        if not cap.isOpened():
            return f"Error: Could not open camera source '{source}'."

        ret, frame = cap.read()
        if not ret:
            return "Error: Failed to retrieve a frame from the active camera source."

        # Compress to a JPEG buffer at 80% quality to keep transmission fast.
        ok, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        if not ok:
            return "Error: Failed to encode the captured frame as JPEG."
        return Image(data=buffer.tobytes(), format="jpeg")
    except Exception as e:  # noqa: BLE001
        return f"Camera capture failed: {e}"
    finally:
        cap.release()  # Always free the hardware lock.
