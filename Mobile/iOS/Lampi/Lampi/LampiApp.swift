//
//  LampiApp.swift
//  Lampi
//

import SwiftUI
import Mixpanel

@main
struct LampiApp: App {
    #warning("Update DEVICE_NAME")
    let DEVICE_NAME = "LAMPI XXXXXXX"
    let USE_BROWSER = false

    #warning("Update MIXPANEL_TOKEN")
    let MIXPANEL_TOKEN = "INSERT MIXPANEL TOKEN HERE"

    init() {
        Mixpanel.initialize(token: MIXPANEL_TOKEN)
        Mixpanel.mainInstance().registerSuperProperties(["interface": "iOS"])
    }

    var body: some Scene {
        WindowGroup {
            if USE_BROWSER {
                LampiBrowserView()
            } else {
                LampiView(lamp: Lampi(name: DEVICE_NAME))
            }
        }
    }
}

extension MixpanelInstance {
    func trackUIEvent(_ event: String?, properties: Properties = [:]) {
        var eventProperties = properties
        eventProperties["event_type"] = "ui"

        track(event: event, properties: eventProperties)
    }
}
