//
//  LampiBrowserView.swift
//  Lampi
//

import SwiftUI

struct LampiBrowserView: View {
    @ObservedObject var lampiManager = LampiManager()

    var body: some View {
        if lampiManager.isScanning {
            BLEScannerView()
        } else {
            NavigationView {
                List(lampiManager.foundLampis, id: \.name) { lampi in
                    NavigationLink(destination: LampiView(lamp: lampi)) {
                        LampiRow(lampi: lampi)
                    }
                }
                .navigationTitle("Nearby Lampis")
                .toolbar {
                    ToolbarItem(placement: .primaryAction) {
                        Button(action: {
                            lampiManager.scanForLampis()
                        }) {
                            Image(systemName: "arrow.clockwise")
                        }
                    }
                }
            }
        }
    }
}

struct LampiBrowserView_Previews: PreviewProvider {
    static var previews: some View {
        LampiBrowserView()

        LampiRow(lampi: Lampi(name: "Test Lampi"))
            .previewLayout(.sizeThatFits)
    }
}

private struct LampiRow: View {
    @ObservedObject var lampi: Lampi

    var body: some View {
        HStack {
            ZStack {
                RoundedRectangle(cornerRadius: 3)
                    .fill(lampi.state.color)
                    .shadow(radius: 2.0)
                    .frame(width: 50, height: 50)
                    .padding()

                let imageName = lampi.state.isOn ? "lightbulb" : "lightbulb.slash"
                Image(systemName: imageName)
                    .imageScale(.large)
                    .foregroundColor(.white)
                    .shadow(radius: 2.0)
            }

            Text("\(lampi.name)")

            Spacer()
        }
    }
}

private struct BLEScannerView: View {
    @State private var showOuterWave = false
    @State private var showMiddleWave = false
    @State private var showInnerWave = false

    var body: some View {
        VStack {
            Spacer()
            ZStack {
                Circle() // Outer Wave
                    .stroke()
                    .frame(width: 120, height: 120)
                    .foregroundColor(.blue)
                    .scaleEffect(showOuterWave ? 3 : 1)
                    .opacity(showOuterWave ? 0.0 : 1)
                    .animation(Animation.easeInOut(duration: 1)
                                .delay(1)
                                .repeatForever(autoreverses: false)
                                .delay(2))
                    .onAppear() {
                        showOuterWave.toggle()
                    }

                Circle() // Middle Wave
                    .stroke()
                    .frame(width: 120, height: 120)
                    .foregroundColor(.blue)
                    .scaleEffect(showMiddleWave ? 2.75 : 1)
                    .opacity(showMiddleWave ? 0.0 : 1)
                    .animation(Animation.easeInOut(duration: 1)
                                .delay(1)
                                .repeatForever(autoreverses: false)
                                .delay(2.2))
                    .onAppear() {
                        showMiddleWave.toggle()
                    }

                Circle() // Inner Wave
                    .stroke()
                    .frame(width: 120, height: 120)
                    .foregroundColor(.blue)
                    .scaleEffect(showInnerWave ? 2.5 : 1)
                    .opacity(showInnerWave ? 0.0 : 1)
                    .animation(Animation.easeInOut(duration: 1)
                                .delay(1)
                                .repeatForever(autoreverses: false)
                                .delay(2.4))
                    .onAppear() {
                        showInnerWave.toggle()
                    }

                Circle()
                    .frame(width: 120, height: 120)
                    .foregroundColor(.blue)
                    .overlay(
                        Image(systemName: "dot.radiowaves.left.and.right")
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                            .padding()
                            .foregroundColor(.white)
                    )
            }
            Spacer()
            Text("Scanning for Lampis")
                .foregroundColor(.white)
                .padding()
                .background(RoundedRectangle(cornerRadius: .infinity)
                                .fill(Color(white: 0.25, opacity: 0.5)))
                .padding()
        }
    }
}
