from dataclasses import dataclass, field
import json

from const import ModelType


@dataclass
class RVCModelSample:
    id: str = ""
    lang: str = ""
    tag: list[str] = field(default_factory=lambda: [])
    name: str = ""
    modelUrl: str = ""
    indexUrl: str = ""
    termsOfUseUrl: str = ""
    credit: str = ""
    description: str = ""

    sampleRate: int = 48000
    modelType: str = ""
    f0: bool = True


def getModelSamples(jsonFiles: list[str], modelType: ModelType):
    from MMVCServerSIO import logger
    try:
        samples: list[RVCModelSample] = []
        for file in jsonFiles:
            with open(file, "r", encoding="utf-8") as f:
                jsonDict = json.load(f)

            modelList = jsonDict[modelType]
            if modelType == "RVC":
                for s in modelList:
                    logger.info(f"getModelSamples: {s}")
                    modelSample = RVCModelSample(**s)
                    samples.append(modelSample)

            else:
                raise RuntimeError(f"Unknown model type {modelType}")
        return samples

    except Exception as e:
        logger.error(f"getModelSamples error: {e}")
        print("[Voice Changer] loading sample info error:", e)
        return None
