"""
Wrapper ligero sobre PyHailoRT.
Carga el HEF y expone un método infer(img) → [tensor…].
"""

from pathlib import Path
import numpy as np
import hailort


class HailoRunner:
    def __init__(self, hef_path: Path):
        self.hef_path = hef_path

        # abrir dispositivo y configurar
        self.device = hailort.Device()
        with hailort.Hef(str(hef_path)) as hef:
            self.network_group = self.device.create_network_group(hef)

        # **asumimos un único canal de entrada y 3 de salida**
        in_infos = self.network_group.get_input_infos()
        out_infos = self.network_group.get_output_infos()

        self.input_name = next(iter(in_infos)).name
        self.output_names = [info.name for info in out_infos]

        # abrir streams
        self.input_vstream = self.network_group.create_input_vstream(self.input_name, queue_size=4)
        self.output_vstreams = [
            self.network_group.create_output_vstream(name, queue_size=4)
            for name in self.output_names
        ]

        self.height, self.width, _ = in_infos[0].shape  # p.e. (640, 640, 3)

    # ──────────────────────────────────────────────────────────────
    def infer(self, frame_bgr: np.ndarray) -> list[np.ndarray]:
        """
        · Recibe frame BGR uint8 de tamaño arbitrario.
        · Lo ajusta a la resolución que espera el HEF.
        · Devuelve la lista de tensores crudos.
        """
        import cv2

        img = cv2.resize(frame_bgr, (self.width, self.height), interpolation=cv2.INTER_LINEAR)
        img = img.astype(np.uint8)

        # flat → bytes
        self.input_vstream.send(img.tobytes())

        tensors = [np.frombuffer(o.recv(), dtype=np.uint8)
                   .reshape(o.info.shape) for o in self.output_vstreams]
        return tensors

    # ──────────────────────────────────────────────────────────────
    def close(self):
        for o in self.output_vstreams:
            o.close()
        self.input_vstream.close()
        self.network_group.release()
        self.device.release()
