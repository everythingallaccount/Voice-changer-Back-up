## VC Client

[Japanese](/README_ja.md)

## What's New!

- v.1.5.3.4d

  - some bugfix
    - All: nof0 onnx model doesn't work for float processing

- v.1.5.3.4c

  - some bugfix
    - M1 Mac: mps cannot support float64
    - All: nof0 onnx model doesn't work

- v.1.5.3.4b

  - some bugfix
  - some performance improvements

- v.1.5.3.4

  - Update framework pyTorch v1.x -> v.2.x
  - Update framework ONNX v1.13.x -> v.15.x
  - remove support of so-vits-svc 4.0v2
  - experimental support onnx-directml
  -

# What is VC Client

1. This is a client software for performing real-time voice conversion using various Voice Conversion (VC) AI. The supported AI for voice conversion are as follows.

- [MMVC](https://github.com/isletennos/MMVC_Trainer)
- [so-vits-svc](https://github.com/svc-develop-team/so-vits-svc)
- [RVC(Retrieval-based-Voice-Conversion)](https://github.com/liujing04/Retrieval-based-Voice-Conversion-WebUI)
- [DDSP-SVC](https://github.com/yxlllc/DDSP-SVC)

2. Distribute the load by running Voice Changer on a different PC
   The real-time voice changer of this application works on a server-client configuration. By running the MMVC server on a separate PC, you can run it while minimizing the impact on other resource-intensive processes such as gaming commentary.

![image](https://user-images.githubusercontent.com/48346627/206640768-53f6052d-0a96-403b-a06c-6714a0b7471d.png)

3. Cross-platform compatibility
   Supports Windows, Mac (including Apple Silicon M1), Linux, and Google Colaboratory.

# usage

This is an app for performing voice changes with MMVC and so-vits-svc.

It can be used in two main ways, in order of difficulty:

- Using a pre-built binary
- Setting up an environment with Docker or Anaconda and using it

## (1) Usage with pre-built binaries

You can download and run executable binaries.
We offer Windows and Mac versions.

- For Windows user, after unzipping the downloaded zip file, please run the `start_http.bat` file corresponding to your VC.

- For Mac version, after unzipping the downloaded file, double-click the `startHttp.command` file corresponding to your VC. If a message indicating that the developer cannot be verified is displayed, please press the control key and click to run it again (or right-click to run it).

- If you are connecting remotely, please use the `.command` file (Mac) or `.bat` file (Windows) with https instead of http.

- The encoder of DDPS-SVC only supports hubert-soft.

- Please refer to [here](tutorials/tutorial_rvc_en_latest.md) for the description of each item of GUI to be used in RVC.

- Download (When you cannot download from google drive, try [hugging_face](https://huggingface.co/wok000/vcclient000/tree/main))

| Version    | OS  | Framework                                 | link                                                                                           | support VC                                                                    | size   |
| ---------- | --- | ----------------------------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------ |
| v.1.5.3.4d | mac | ONNX(cpu), PyTorch(cpu,mps)               | [normal](https://drive.google.com/uc?id=1xZPn9UiqBgPHANQAzFF5O2sqahqFOuoB&export=download) \*1 | MMVC v.1.5.x, MMVC v.1.3.x, so-vits-svc 4.0, RVC                              | 785MB  |
|            | win | ONNX(cpu,cuda), PyTorch(cpu,cuda)         | [normal](https://drive.google.com/uc?id=1oks9Aq_cFKNk95VOvXwhEKE8GHX0RUW9&export=download) \*1 | MMVC v.1.5.x, MMVC v.1.3.x, so-vits-svc 4.0, RVC, DDSP-SVC                    | 3243MB |
|            | win | ONNX(cpu,DirectML), PyTorch(cpu,cuda) \*2 | [normal](https://drive.google.com/uc?id=1jJ6P9rBuSj5u_SSWAbwGAaT31cM4rRcf&export=download) \*1 | MMVC v.1.5.x, MMVC v.1.3.x, so-vits-svc 4.0, RVC, DDSP-SVC                    | 3121MB |
| v.1.5.3.3b | mac | ONNX(cpu), PyTorch(cpu,mps)               | [normal](https://drive.google.com/uc?id=14_STxl6lYwhTahcgMGfsjnwpoHmN0svf&export=download) \*1 | MMVC v.1.5.x, MMVC v.1.3.x, so-vits-svc 4.0, RVC                              | 797MB  |
|            | win | ONNX(cpu,cuda), PyTorch(cpu,cuda)         | [normal](https://drive.google.com/uc?id=1VpMSF5lE3VrUeb_TusWQi22_Hx8JoPhC&export=download) \*1 | MMVC v.1.5.x, MMVC v.1.3.x, so-vits-svc 4.0, so-vits-svc 4.0v2, RVC, DDSP-SVC | 2872MB |

(\*1) You can alson download from [hugging_face](https://huggingface.co/wok000/vcclient000/tree/main)
(\*2) The developer does not have an AMD graphics card, so it has not been tested. This package only includes onnxruntime-directml.
(\*3) If unpacking or starting is slow, there is a possibility that virus checking is running on your antivirus software. Please try running it with the file or folder excluded from the target. (At your own risk)

## (2) Usage after setting up the environment such as Docker or Anaconda

Clone this repository and use it. Setting up WSL2 is essential for Windows. Additionally, setting up virtual environments such as Docker or Anaconda on WSL2 is also required. On Mac, setting up Python virtual environments such as Anaconda is necessary. Although preparation is required, this method works the fastest in many environments. **<font color="red"> Even without a GPU, it may work well enough with a reasonably new CPU </font>(refer to the section on real-time performance below)**.

[Explanation video on installing WSL2 and Docker](https://youtu.be/POo_Cg0eFMU)

[Explanation video on installing WSL2 and Anaconda](https://youtu.be/fba9Zhsukqw)

To run docker, see [start docker](docker_vcclient/README_en.md).

To run on Anaconda venv, see [server developer's guide](README_dev_en.md)

# Real-time performance

Conversion is almost instantaneous when using GPU.

https://twitter.com/DannadoriYellow/status/1613483372579545088?s=20&t=7CLD79h1F3dfKiTb7M8RUQ

Even with CPU, recent ones can perform conversions at a reasonable speed.

https://twitter.com/DannadoriYellow/status/1613553862773997569?s=20&t=7CLD79h1F3dfKiTb7M8RUQ

With an old CPU (i7-4770), it takes about 1000 msec for conversion.

# Software Signing

This software is not signed by the developer. A warning message will appear, but you can run the software by clicking the icon while holding down the control key. This is due to Apple's security policy. Running the software is at your own risk.

![image](https://user-images.githubusercontent.com/48346627/212567711-c4a8d599-e24c-4fa3-8145-a5df7211f023.png)

https://user-images.githubusercontent.com/48346627/212569645-e30b7f4e-079d-4504-8cf8-7816c5f40b00.mp4

# Acknowledgments

- [Tachizunda-mon materials](https://seiga.nicovideo.jp/seiga/im10792934)
- [Irasutoya](https://www.irasutoya.com/)
- [Tsukuyomi-chan](https://tyc.rei-yumesaki.net)

> This software uses the voice data of the free material character "Tsukuyomi-chan," which is provided for free by CV. Yumesaki Rei.
>
> - Tsukuyomi-chan Corpus (CV. Yumesaki Rei)
>
> https://tyc.rei-yumesaki.net/material/corpus/
>
> Copyright. Rei Yumesaki

- [Amitaro's Onsozai kobo](https://amitaro.net/)
- [Replica doll](https://kikyohiroto1227.wixsite.com/kikoto-utau)

# Terms of Use

In accordance with the Tsukuyomi-chan Corpus Terms of Use for the Tsukuyomi-chan Real-time Voice Changer, the use of the converted voice for the following purposes is prohibited.

- Criticizing or attacking individuals (the definition of "criticizing or attacking" is based on the Tsukuyomi-chan character license).

- Advocating for or opposing specific political positions, religions, or ideologies.

- Publicly displaying strongly stimulating expressions without proper zoning.

- Publicly disclosing secondary use (use as materials) for others.
  (Distributing or selling as a work for viewing is not a problem.)

Regarding the Real-time Voice Changer Amitaro, we prohibit the following uses in accordance with the terms of use of the Amitaro's koe-sozai kobo.[detail](https://amitaro.net/voice/faq/#index_id6)

Regarding the Real-time Voice Changer Kikoto Mahiro, we prohibit the following uses in accordance with the terms of use of Replica doll.[detail](https://kikyohiroto1227.wixsite.com/kikoto-utau/ter%EF%BD%8Ds-of-service)

# Disclaimer

We are not liable for any direct, indirect, consequential, incidental, or special damages arising out of or in any way connected with the use or inability to use this software.
