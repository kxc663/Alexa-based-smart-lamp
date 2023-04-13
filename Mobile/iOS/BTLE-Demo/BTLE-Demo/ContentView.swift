//
//  ContentView.swift
//  BTLE-Demo
//
//  Created by Chris Nurre on 1/4/21.
//

import SwiftUI

struct ContentView: View {
    @ObservedObject var btleObj = BTLEObject()

    var body: some View {
        VStack {
            Slider(value:$btleObj.state.number)
            Text("Number: \(btleObj.state.number)")
        }.padding()
        .disabled(!btleObj.state.isConnected)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
