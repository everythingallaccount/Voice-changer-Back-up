import React, { useMemo, useState, useEffect } from "react"
import { useAppState } from "../../../001_provider/001_AppStateProvider"
import { useGuiState } from "../001_GuiStateProvider"

export type StartButtonRowProps = {
}


export const StartButtonRow = (_props: StartButtonRowProps) => {
    const appState = useAppState()
    const guiState = useGuiState()
    const [startWithAudioContextCreate, setStartWithAudioContextCreate] = useState<boolean>(false)

    useEffect(() => {
        if (!startWithAudioContextCreate) {
            return
        }
        guiState.setIsConverting(true)
        appState.clientSetting.start()
    }, [startWithAudioContextCreate])


    const startButtonRow = useMemo(() => {
        const onStartClicked = async () => {


            if (appState.serverSetting.serverSetting.enableServerAudio == 0) {


                if (!appState.initializedRef.current) {
                    while (true) {
                        // console.log("wait 500ms")
                        await new Promise<void>((resolve) => {
                            setTimeout(resolve, 500)
                        })
                        // console.log("initiliazed", appState.initializedRef.current)
                        if (appState.initializedRef.current) {
                            break
                        }
                    }
                    setStartWithAudioContextCreate(true)
                } else {
                    guiState.setIsConverting(true)
                    await appState.clientSetting.start()
                }
            } else {


                appState.serverSetting.updateServerSettings({ ...appState.serverSetting.serverSetting, serverAudioStated: 1 })



                guiState.setIsConverting(true)
            }
        }
        const onStopClicked = async () => {
            if (appState.serverSetting.serverSetting.enableServerAudio == 0) {
                guiState.setIsConverting(false)
                await appState.clientSetting.stop()
            } else {
                guiState.setIsConverting(false)
                console.log("Stop clicked", appState.serverSetting.serverSetting)
                appState.serverSetting.updateServerSettings({ ...appState.serverSetting.serverSetting, serverAudioStated: 0 })
            }
        }
        const startClassName = guiState.isConverting ? "body-button-active" : "body-button-stanby"
        const stopClassName = guiState.isConverting ? "body-button-stanby" : "body-button-active"

        return (
            <div className="body-row split-3-2-2-3 left-padding-1  guided">
                <div className="body-item-title left-padding-1">Start</div>
                <div className="body-button-container">
                    <div onClick={onStartClicked} className={startClassName}>start</div>
                    <div onClick={onStopClicked} className={stopClassName}>stop</div>
                </div>
                <div>
                </div>
                <div className="body-input-container">
                </div>
            </div>
        )
    }, [guiState.isConverting, appState.clientSetting.start, appState.clientSetting.stop, appState.serverSetting.serverSetting, appState.serverSetting.updateServerSettings])

    return startButtonRow
}