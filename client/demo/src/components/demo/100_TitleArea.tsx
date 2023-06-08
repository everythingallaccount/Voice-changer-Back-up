import React, { useMemo } from "react"
import { generateComponent } from "./002_ComponentGenerator"
import { useAppRoot } from "../../001_provider/001_AppRootProvider"

export const TitleArea = () => {
    const { appGuiSettingState } = useAppRoot()
    const componentSettings = appGuiSettingState.appGuiSetting.front.title
    console.log("TitleAreaaaaaaaaaaaa", componentSettings)
    const titleArea = useMemo(() => {
        const components = componentSettings.map((x, index) => {
            const c = generateComponent(x.name, x.options)
            return <div key={`${x.name}_${index}`}>{c}</div>
        })
        return (
            <>
                {/*<div>b3</div>*/}
                {components}

                {/*The component is the real time voice changer client.*/}
                {/*<div>bbbbbbbbb4</div>*/}
            </>
        )
    }, [])

    return titleArea
}