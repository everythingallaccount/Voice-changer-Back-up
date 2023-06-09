from enum import Enum
import os
import sys
import tempfile
from typing import Literal, TypeAlias


ModelType: TypeAlias = Literal[
    "MMVCv15",
    "MMVCv13",
    "so-vits-svc-40v2",
    "so-vits-svc-40",
    "so-vits-svc-40_c",
    "DDSP-SVC",
    "RVC",
]

ERROR_NO_ONNX_SESSION = "ERROR_NO_ONNX_SESSION"


tmpdir = tempfile.TemporaryDirectory()
# print("generate tmpdir:::",tmpdir)
SSL_KEY_DIR = os.path.join(tmpdir.name, "keys") if hasattr(sys, "_MEIPASS") else "keys"
MODEL_DIR = os.path.join(tmpdir.name, "logs") if hasattr(sys, "_MEIPASS") else "logs"
UPLOAD_DIR = (
    os.path.join(tmpdir.name, "upload_dir")
    if hasattr(sys, "_MEIPASS")
    else "upload_dir"
)
NATIVE_CLIENT_FILE_WIN = (
    os.path.join(sys._MEIPASS, "voice-changer-native-client.exe")  # type: ignore
    if hasattr(sys, "_MEIPASS")
    else "voice-changer-native-client"
)
NATIVE_CLIENT_FILE_MAC = (
    os.path.join(
        sys._MEIPASS,  # type: ignore
        "voice-changer-native-client.app",
        "Contents",
        "MacOS",
        "voice-changer-native-client",
    )
    if hasattr(sys, "_MEIPASS")
    else "voice-changer-native-client"
)

HUBERT_ONNX_MODEL_PATH = (
    os.path.join(sys._MEIPASS, "model_hubert/hubert_simple.onnx")  # type: ignore
    if hasattr(sys, "_MEIPASS")
    else "model_hubert/hubert_simple.onnx"
)


TMP_DIR = (
    os.path.join(tmpdir.name, "tmp_dir") if hasattr(sys, "_MEIPASS") else "tmp_dir"
)
os.makedirs(TMP_DIR, exist_ok=True)


def getFrontendPath():

    frontend_path = (
        os.path.join(sys._MEIPASS, "dist")
        if hasattr(sys, "_MEIPASS")
        else "../client/demo/dist"
    )
    print("We turn it.",frontend_path)

    return frontend_path


# "hubert_base",  "contentvec",  "distilhubert"
class EnumEmbedderTypes(Enum):
    hubert = "hubert_base"
    contentvec = "contentvec"
    hubert_jp = "hubert-base-japanese"


class EnumInferenceTypes(Enum):
    pyTorchRVC = "pyTorchRVC"
    pyTorchRVCNono = "pyTorchRVCNono"
    pyTorchRVCv2 = "pyTorchRVCv2"
    pyTorchRVCv2Nono = "pyTorchRVCv2Nono"
    pyTorchWebUI = "pyTorchWebUI"
    pyTorchWebUINono = "pyTorchWebUINono"
    onnxRVC = "onnxRVC"
    onnxRVCNono = "onnxRVCNono"


class EnumPitchExtractorTypes(Enum):
    harvest = "harvest"
    dio = "dio"
    crepe = "crepe"


class EnumFrameworkTypes(Enum):
    pyTorch = "pyTorch"
    onnx = "onnx"


class ServerAudioDeviceTypes(Enum):
    audioinput = "audioinput"
    audiooutput = "audiooutput"


SAMPLES_JSONS = [
    # "https://huggingface.co/wok000/vcclient_model/raw/main/samples_0001.json",
    # "https://huggingface.co/wok000/vcclient_model/raw/main/samples_0002.json",
    "https://huggingface.co/wok000/vcclient_model/raw/main/samples_0003_t.json",
    "https://huggingface.co/wok000/vcclient_model/raw/main/samples_0003_o.json",
    # "https://huggingface.co/wok000/vcclient_model/raw/main/test/test_official_v1_v2.json",
    # "https://huggingface.co/wok000/vcclient_model/raw/main/test/test_ddpn_v1_v2.json",
]

SAMPLE_MODEL_IDS = [
    ("TokinaShigure_o", True),
    ("KikotoMahiro_o", False),
    ("Amitaro_o", False),
    ("Tsukuyomi-chan_o", False),
    # オフィシャルモデルテスト
    # ("test-official-v1-f0-48k-l9-hubert_t", True),
    # ("test-official-v1-nof0-48k-l9-hubert_t", False),
    # ("test-official-v2-f0-40k-l12-hubert_t", False),
    # ("test-official-v2-nof0-40k-l12-hubert_t", False),
    # ("test-official-v1-f0-48k-l9-hubert_o", True),
    # ("test-official-v1-nof0-48k-l9-hubert_o", False),
    # ("test-official-v2-f0-40k-l12-hubert_o", False),
    # ("test-official-v2-nof0-40k-l12-hubert_o", False),
    # DDPNモデルテスト(torch)
    # ("test-ddpn-v1-f0-48k-l9-hubert_t", False),
    # ("test-ddpn-v1-nof0-48k-l9-hubert_t", False),
    # ("test-ddpn-v2-f0-40k-l12-hubert_t", False),
    # ("test-ddpn-v2-nof0-40k-l12-hubert_t", False),
    # ("test-ddpn-v2-f0-40k-l12-hubert_jp_t", False),
    # ("test-ddpn-v2-nof0-40k-l12-hubert_jp_t", False),
    # DDPNモデルテスト(onnx)
    # ("test-ddpn-v1-f0-48k-l9-hubert_o", False),
    # ("test-ddpn-v1-nof0-48k-l9-hubert_o", False),
    # ("test-ddpn-v2-f0-40k-l12-hubert_o", False),
    # ("test-ddpn-v2-nof0-40k-l12-hubert_o", False),
    # ("test-ddpn-v2-f0-40k-l12-hubert_jp_o", False),
    # ("test-ddpn-v2-nof0-40k-l12-hubert_jp_o", False),
]


RVC_MODEL_DIRNAME = "rvc"
RVC_MAX_SLOT_NUM = 10
