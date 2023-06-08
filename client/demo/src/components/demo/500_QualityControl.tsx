import React, { useMemo } from "react"
import { useAppRoot } from "../../001_provider/001_AppRootProvider"
import { AnimationTypes, HeaderButton, HeaderButtonProps } from "../101_HeaderButton"
import { useGuiState } from "./001_GuiStateProvider"
import { generateComponent } from "./002_ComponentGenerator"

export const QualityControl = () => {
    const guiState = useGuiState()
    const { appGuiSettingState } = useAppRoot()
    const componentSettings = appGuiSettingState.appGuiSetting.front.qualityControl

    const accodionButton = useMemo(() => {
        const accodionButtonProps: HeaderButtonProps = {
            stateControlCheckbox: guiState.stateControls.openQualityControlCheckbox,
            tooltip: "Open/Close",
            onIcon: ["fas", "caret-up"],
            offIcon: ["fas", "caret-up"],
            animation: AnimationTypes.spinner,
            tooltipClass: "tooltip-right",
        };
        return <HeaderButton {...accodionButtonProps}></HeaderButton>;
    }, []);

    const deviceSetting = useMemo(() => {
        const components = componentSettings.map((x, index) => {
            const c = generateComponent(x.name, x.options)
            return <div key={`${x.name}_${index}`}>{c}</div>
        })
        return (
            <>
                {guiState.stateControls.openQualityControlCheckbox.trigger}
                <div className="partition">
                    <div className="partition-header">
                        <span className="caret">
                            {accodionButton}
                        </span>
                        <span className="title" onClick={() => { guiState.stateControls.openQualityControlCheckbox.updateState(!guiState.stateControls.openQualityControlCheckbox.checked()) }}>
                            {/*Quality Control*/}
                            质量控制
                        </span>
                        <span></span>
                    </div>

                    <div className="partition-content">
                        {components}
                        {/* <NoiseControlRow />
                        <GainControlRow />
                        <F0DetectorRow />
                        <div className="body-row divider"></div>
                        <AnalyzerRow />
                        <SamplingRow />
                        <SamplingPlayRow /> */}
                    </div>
                </div>
            </>
        )
    }, [])

    return deviceSetting
}