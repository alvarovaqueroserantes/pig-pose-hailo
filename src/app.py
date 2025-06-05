import argparse, cv2, time, sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from hailo_runner import HailoRunner
from postprocess import decode, draw

# ──────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Realtime pose with Hailo8L")
    ap.add_argument("--hef", type=Path, default=Path("../models/pig_pose_hailo.hef"),
                    help="Ruta al .hef")
    ap.add_argument("--src", default="0",
                    help="Video file (.mov) o ID de cámara (0)")
    ap.add_argument("--width", type=int, default=1280,
                    help="Ventana ancho")
    args = ap.parse_args()

    runner = HailoRunner(args.hef)

    cap = cv2.VideoCapture(int(args.src) if args.src.isdigit() else args.src)
    if not cap.isOpened():
        print("No se pudo abrir la cámara / video"); return

    t0, fps = time.time(), 0
    while True:
        ok, frame = cap.read()
        if not ok: break

        outs = runner.infer(frame)
        detections = decode(outs)
        draw(frame, detections)

        # FPS
        fps = fps*0.9 + 0.1 / (time.time() - t0)
        t0 = time.time()
        cv2.putText(frame, f"{fps:0.1f} FPS", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

        frame_rs = cv2.resize(frame, (args.width,
                                      int(frame.shape[0]*args.width/frame.shape[1])))
        cv2.imshow("Hailo Pose", frame_rs)
        if cv2.waitKey(1) & 0xFF == 27:   # ESC
            break

    cap.release(); cv2.destroyAllWindows(); runner.close()

# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
