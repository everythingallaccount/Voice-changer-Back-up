def printMessage(message, level=0):
    pf = platform.system()
    if pf == "Windows":
        if level == 0:
            print(f"{message}")
        elif level == 1:
            print(f"    {message}")
        elif level == 2:
            print(f"    {message}")
        else:
            print(f"    {message}")
    else:
        if level == 0:
            print(f"\033[17m{message}\033[0m")
        elif level == 1:
            print(f"\033[34m    {message}\033[0m")
        elif level == 2:
            print(f"\033[32m    {message}\033[0m")
        else:
            print(f"\033[47m    {message}\033[0m")
from concurrent.futures import ThreadPoolExecutor
import sys

from distutils.util import strtobool
from datetime import datetime
import socket
import platform
import os
import argparse
from Downloader import download, download_no_tqdm
from voice_changer.RVC.SampleDownloader import (
    checkRvcModelExist,
    downloadInitialSampleModels,
)

from voice_changer.utils.VoiceChangerParams import VoiceChangerParams

import uvicorn
from mods.ssl import create_self_signed_cert
from voice_changer.VoiceChangerManager import VoiceChangerManager
from sio.MMVC_SocketIOApp import MMVC_SocketIOApp
from restapi.MMVC_Rest import MMVC_Rest
from const import (
    NATIVE_CLIENT_FILE_MAC,
    NATIVE_CLIENT_FILE_WIN,
    SSL_KEY_DIR,
    getRVCSampleJsonAndModelIds,
)
import subprocess
import multiprocessing as mp
from misc.log_control import setup_loggers

setup_loggers()
printMessage(f"Start of application.......", level=2)

def setupArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--logLevel",
        type=str,
        default="critical",
        help="Log level info|critical. (default: critical)",
    )
    parser.add_argument("-p", type=int, default=18888, help="port")
    parser.add_argument("--https", type=strtobool, default=False, help="use https")
    parser.add_argument(
        "--httpsKey", type=str, default="ssl.key", help="path for the key of https"
    )
    parser.add_argument(
        "--httpsCert", type=str, default="ssl.cert", help="path for the cert of https"
    )
    parser.add_argument(
        "--httpsSelfSigned",
        type=strtobool,
        default=True,
        help="generate self-signed certificate",
    )

    parser.add_argument("--model_dir", type=str, help="path to model files")
    parser.add_argument(
        "--rvc_sample_mode", type=str, default="production", help="rvc_sample_mode"
    )

    parser.add_argument(
        "--content_vec_500", type=str, help="path to content_vec_500 model(pytorch)"
    )
    parser.add_argument(
        "--content_vec_500_onnx", type=str, help="path to content_vec_500 model(onnx)"
    )
    parser.add_argument(
        "--content_vec_500_onnx_on",
        type=strtobool,
        default=False,
        help="use or not onnx for  content_vec_500",
    )
    parser.add_argument(
        "--hubert_base", type=str, help="path to hubert_base model(pytorch)"
    )
    parser.add_argument(
        "--hubert_base_jp", type=str, help="path to hubert_base_jp model(pytorch)"
    )
    parser.add_argument(
        "--hubert_soft", type=str, help="path to hubert_soft model(pytorch)"
    )
    parser.add_argument(
        "--nsf_hifigan", type=str, help="path to nsf_hifigan model(pytorch)"
    )

    return parser




def downloadWeight():
    # content_vec_500 = (args.content_vec_500,)
    # content_vec_500_onnx = (args.content_vec_500_onnx,)
    # content_vec_500_onnx_on = (args.content_vec_500_onnx_on,)
    hubert_base = args.hubert_base
    hubert_base_jp = args.hubert_base_jp
    hubert_soft = args.hubert_soft
    nsf_hifigan = args.nsf_hifigan

    # file exists check (currently only for rvc)
    downloadParams = []
    if os.path.exists(hubert_base) is False:
        downloadParams.append(
            {
                "url": "https://huggingface.co/ddPn08/rvc-webui-models/resolve/main/embeddings/hubert_base.pt",
                "saveTo": hubert_base,
                "position": 0,
            }
        )
    if os.path.exists(hubert_base_jp) is False:
        downloadParams.append(
            {
                "url": "https://huggingface.co/rinna/japanese-hubert-base/resolve/main/fairseq/model.pt",
                "saveTo": hubert_base_jp,
                "position": 1,
            }
        )
    if os.path.exists(hubert_soft) is False:
        downloadParams.append(
            {
                "url": "https://huggingface.co/wok000/weights/resolve/main/ddsp-svc30/embedder/hubert-soft-0d54a1f4.pt",
                "saveTo": hubert_soft,
                "position": 2,
            }
        )
    if os.path.exists(nsf_hifigan) is False:
        downloadParams.append(
            {
                "url": "https://huggingface.co/wok000/weights/resolve/main/ddsp-svc30/nsf_hifigan_20221211/model.bin",
                "saveTo": nsf_hifigan,
                "position": 3,
            }
        )
    nsf_hifigan_config = os.path.join(os.path.dirname(nsf_hifigan), "config.json")

    if os.path.exists(nsf_hifigan_config) is False:
        downloadParams.append(
            {
                "url": "https://huggingface.co/wok000/weights/raw/main/ddsp-svc30/nsf_hifigan_20221211/config.json",
                "saveTo": nsf_hifigan_config,
                "position": 4,
            }
        )

    with ThreadPoolExecutor() as pool:
        pool.map(download, downloadParams)

    if (
        os.path.exists(hubert_base) is False
        or os.path.exists(hubert_base_jp) is False
        or os.path.exists(hubert_soft) is False
        or os.path.exists(nsf_hifigan) is False
        or os.path.exists(nsf_hifigan_config) is False
    ):
        printMessage("RVC用のモデルファイルのダウンロードに失敗しました。", level=2)
        printMessage("failed to download weight for rvc", level=2)

printMessage(f"Prepare to set up setupArgParser", level=2)

parser = setupArgParser()
args, unknown = parser.parse_known_args()

printMessage(f"Booting PHASE ::::::::::::::::::::{__name__}", level=2)

PORT = args.p

# args.p=18889
# PORT = 18889

def localServer(logLevel: str = "critical"):
    printMessage(f"Path checking.gggggggg {os.path.basename(__file__)[:-3]}:app_socketio", level=2)

    uvicorn.run(
        f"{os.path.basename(__file__)[:-3]}:app_socketio",
        host="0.0.0.0",
        port=int(PORT),
        reload=False if hasattr(sys, "_MEIPASS") else True,
        log_level=logLevel,
    )


if __name__ == "MMVCServerSIO":
    printMessage(f"Start of application.......MMVCServerSIO", level=2)
    mp.freeze_support()
    voiceChangerParams = VoiceChangerParams(
        model_dir=args.model_dir,
        content_vec_500=args.content_vec_500,
        content_vec_500_onnx=args.content_vec_500_onnx,
        content_vec_500_onnx_on=args.content_vec_500_onnx_on,
        hubert_base=args.hubert_base,
        hubert_base_jp=args.hubert_base_jp,
        hubert_soft=args.hubert_soft,
        nsf_hifigan=args.nsf_hifigan,
        rvc_sample_mode=args.rvc_sample_mode,
    )

    if (
        os.path.exists(voiceChangerParams.hubert_base) is False
        or os.path.exists(voiceChangerParams.hubert_base_jp) is False
    ):
        printMessage("RVC用のモデルファイルのダウンロードに失敗しました。", level=2)
        printMessage("failed to download weight for rvc", level=2)
    else:
        printMessage(f"Download weight success.........", level=2)

    voiceChangerManager = VoiceChangerManager.get_instance(voiceChangerParams)
    app_fastapi = MMVC_Rest.get_instance(voiceChangerManager, voiceChangerParams)
    app_socketio = MMVC_SocketIOApp.get_instance(app_fastapi, voiceChangerManager)
    printMessage(f"app_socketio Finish Initialize........", level=2)

if __name__ == "__mp_main__":
    printMessage("Starting server processssssssssssssssss. サーバプロセスを起動しています。", level=2)

if __name__ == "__main__":
    printMessage("This is __main__...................................", level=2)

    mp.freeze_support()

    printMessage("Voice Changerを起動しています。", level=2)

    # ダウンロード
    downloadWeight()
    os.makedirs(args.model_dir, exist_ok=True)

    try:
        sampleJsons = []
        sampleJsonUrls, sampleModels = getRVCSampleJsonAndModelIds(args.rvc_sample_mode)
        for url in sampleJsonUrls:
            filename = os.path.basename(url)
            download_no_tqdm({"url": url, "saveTo": filename, "position": 0})
            sampleJsons.append(filename)
        if checkRvcModelExist(args.model_dir) is False:
            downloadInitialSampleModels(sampleJsons, sampleModels, args.model_dir)
        print("[Voice Changer] loading Sample is successful.")
    except Exception as e:
        print("[Voice Changer] loading sample failed", e)

    PORT = args.p

    if os.getenv("EX_PORT"):
        EX_PORT = os.environ["EX_PORT"]
        printMessage(f"External_Portttttttt:{EX_PORT} Internal_Port:{PORT}", level=1)
    else:
        printMessage(f"Internal_Portttttttt:{PORT}", level=1)

    if os.getenv("EX_IP"):
        EX_IP = os.environ["EX_IP"]
        printMessage(f"External_IPPPPPPPPPPP:{EX_IP}", level=1)

    # HTTPS key/cert作成
    if args.https and args.httpsSelfSigned == 1:
        # HTTPS(おれおれ証明書生成)
        os.makedirs(SSL_KEY_DIR, exist_ok=True)
        key_base_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        keyname = f"{key_base_name}.key"
        certname = f"{key_base_name}.cert"
        create_self_signed_cert(
            certname,
            keyname,
            certargs={
                "Country": "JP",
                "State": "Tokyo",
                "City": "Chuo-ku",
                "Organization": "F",
                "Org. Unit": "F",
            },
            cert_dir=SSL_KEY_DIR,
        )
        key_path = os.path.join(SSL_KEY_DIR, keyname)
        cert_path = os.path.join(SSL_KEY_DIR, certname)
        printMessage(
            f"protocol: HTTPS(self-signed), key:{key_path}, cert:{cert_path}", level=1
        )

    elif args.https and args.httpsSelfSigned == 0:
        # HTTPS
        key_path = args.httpsKey
        cert_path = args.httpsCert
        printMessage(f"protocol: HTTPS, key:{key_path}, cert:{cert_path}", level=1)
    else:
        # HTTP
        printMessage("protocol: HTTP", level=1)
    printMessage("-- ---- -- ", level=1)

    # アドレス表示
    printMessage("ブラウザで次のURLを開いてください.", level=2)
    if args.https == 1:
        printMessage("https://<IP>:<PORT>/", level=1)
    else:
        printMessage("http://<IP>:<PORT>/", level=1)

    printMessage("多くの場合は次のいずれかのURLにアクセスすると起動します。", level=2)


    if "EX_PORT" in locals() and "EX_IP" in locals():  # シェルスクリプト経由起動(docker)
        printMessage(f"socket Is delayed to be connected and initialized......................", level=1)

        if args.https == 1:
            printMessage(f"https://localhost:{EX_PORT}/", level=1)
            for ip in EX_IP.strip().split(" "):
                printMessage(f"https://{ip}:{EX_PORT}/", level=1)
        else:
            printMessage(f"http://localhost:{EX_PORT}/", level=1)
    else:  # 直接python起動
        printMessage(f"socket is directly connected in initialized.....................", level=1)

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        hostname = s.getsockname()[0]
        if args.https == 1:
            printMessage(f"https://localhost:{PORT}/", level=1)
            printMessage(f"https://{hostname}:{PORT}/", level=1)
        else:
            printMessage(f"http://localhost:{PORT}/", level=1)

    # サーバ起動
    if args.https:
        print("HTTPS is ..................")

        # HTTPS サーバ起動
        uvicorn.run(
            f"{os.path.basename(__file__)[:-3]}:app_socketio",
            host="0.0.0.0",
            port=int(PORT),
            reload=False if hasattr(sys, "_MEIPASS") else True,
            ssl_keyfile=key_path,
            ssl_certfile=cert_path,
            log_level=args.logLevel,
        )
    else:
        print("HTTPS is not..................")

        p = mp.Process(name="p", target=localServer, args=(args.logLevel,))
        print("Prepare to start the localServer process.")

        p.start()
        print("localServer process............Should be start.")

        try:
            if sys.platform.startswith("win"):
                print("eeeeeeeeeeeeeeeeeeeeeeeeeeee2",NATIVE_CLIENT_FILE_WIN)

                process = subprocess.Popen(
                    [NATIVE_CLIENT_FILE_WIN, "-u", f"http://localhost:{PORT}/"]
                )
                print("eeeeeeeeeeeeeeeeeeeeeeeeeeee3")
                return_code = process.wait()
                print("client closed.")
                p.terminate()
            elif sys.platform.startswith("darwin"):
                process = subprocess.Popen(
                    [NATIVE_CLIENT_FILE_MAC, "-u", f"http://localhost:{PORT}/"]
                )
                return_code = process.wait()
                print("client closed.")
                p.terminate()

        except Exception as e:
            print("Exception are phased.   Seems that the front end client is not open successfully?")
            print(e)
