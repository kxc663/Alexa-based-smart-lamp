//
//  LampiView.swift
//  Lampi
//

import SwiftUI

struct LampiView: View {
    @ObservedObject var lampi = Lampi()

    var body: some View {
        VStack {
            Rectangle()
                .fill(lampi.color)
                .edgesIgnoringSafeArea(.top)

            Group {
                GradientSlider(value: $lampi.hue,
                               handleColor: lampi.baseHueColor,
                               trackColors: Color.rainbow())

                GradientSlider(value: $lampi.saturation,
                               handleColor: Color(hue: lampi.hue,
                                                  saturation: lampi.saturation,
                                                  brightness: 1.0),
                               trackColors: [.white, lampi.baseHueColor])

                GradientSlider(value: $lampi.brightness,
                               handleColor: Color(white: lampi.brightness),
                               handleImage: Image(systemName: "sun.max"),
                               trackColors: [.black, .white])
                    .foregroundColor(Color(white: 1.0 - lampi.brightness))
            }.padding()

            Button(action: {
                lampi.isOn.toggle()
            }) {
                HStack {
                    Spacer()
                    Image(systemName: "power")
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                    Spacer()
                }.padding()
            }
            .frame(height: 100)
            .background(Color.black.edgesIgnoringSafeArea(.bottom))
            .foregroundColor(lampi.isOn ? lampi.color : .gray)
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        LampiView()
    }
}
