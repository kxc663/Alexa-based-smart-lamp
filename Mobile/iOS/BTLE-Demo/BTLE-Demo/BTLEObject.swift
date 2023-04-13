//
//  BTLEObject.swift
//  BTLE-Demo
//

import Foundation
import CoreBluetooth

class BTLEObject: NSObject, ObservableObject {
    @Published var state: State = State() {
        didSet {
            if !updatePending && !skipNextWrite && state != oldValue,
               let numberCharacteristic = numberCharacteristic {

                updatePending = true
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) { [weak self] in
                    guard let self = self else { return }

                    var intToWrite = UInt8(self.state.number * 255.0)
                    let dataToWrite = Data(bytes: &intToWrite, count: 1)
                    self.devicePeripheral?.writeValue(dataToWrite, for: numberCharacteristic, type: .withResponse)

                    self.updatePending = false
                }
            }

            skipNextWrite = false
        }
    }

    private var bluetoothManager: CBCentralManager!
    private var devicePeripheral: CBPeripheral?
    private var numberCharacteristic: CBCharacteristic?
    private var updatePending: Bool = false
    private var skipNextWrite: Bool = false

    override init() {
        super.init()
        bluetoothManager = CBCentralManager(delegate: self,
                                            queue: nil)
    }
}

extension BTLEObject: CBCentralManagerDelegate {
    #warning("Update DEVICE_NAME")
    private static let DEVICE_NAME = "YOUR BLUETOOTH DEVICE NAME"
    private static let OUR_SERVICE_UUID = "7a4bbfe6-999f-4717-b63a-066e06971f59"

    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        if central.state == .poweredOn {
            let services = [CBUUID(string:BTLEObject.OUR_SERVICE_UUID)]
            bluetoothManager.scanForPeripherals(withServices: services)
        }
    }

    func centralManager(_ central: CBCentralManager,
                        didDiscover peripheral: CBPeripheral,
                        advertisementData: [String : Any],
                        rssi RSSI: NSNumber) {
        if peripheral.name == BTLEObject.DEVICE_NAME {
            print("Found \(BTLEObject.DEVICE_NAME)")

            devicePeripheral = peripheral

            bluetoothManager.stopScan()
            bluetoothManager.connect(peripheral)
        }
    }

    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
        print("Connected to peripheral: \(peripheral)")
        state.isConnected = true

        peripheral.delegate = self
        peripheral.discoverServices([CBUUID(string:BTLEObject.OUR_SERVICE_UUID)])
    }

    func centralManager(_ central: CBCentralManager, didDisconnectPeripheral peripheral: CBPeripheral, error: Error?) {
        print("Disconnected from peripheral: \(peripheral)")
        state.isConnected = false
    }
}

extension BTLEObject: CBPeripheralDelegate {
    static let SOME_NUMBER_UUID = "7a4b0001-999f-4717-b63a-066e06971f59"

    func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {
        guard let services = peripheral.services else { return }

        for service in services {
            print("Discovered device service")
            peripheral.discoverCharacteristics(nil, for: service)
        }
    }

    func peripheral(_ peripheral: CBPeripheral, didDiscoverCharacteristicsFor service: CBService, error: Error?) {
        guard let characteristics = service.characteristics else { return }

        for characteristic in characteristics {
            if characteristic.uuid == CBUUID(string: BTLEObject.SOME_NUMBER_UUID) {
                print("Found characteristic with UUID: \(BTLEObject.SOME_NUMBER_UUID)")

                numberCharacteristic = characteristic
                devicePeripheral?.readValue(for: characteristic)
                devicePeripheral?.setNotifyValue(true, for: characteristic)
            }
        }
    }

    func peripheral(_ peripheral: CBPeripheral, didUpdateValueFor characteristic: CBCharacteristic, error: Error?) {
        print("Value updated for characteristic with UUID: \(characteristic.uuid)")
        if characteristic == numberCharacteristic,
           let numberData = numberCharacteristic?.value {

            let newNumber = Double(numberData[0]) / 255.0

            skipNextWrite = true
            state.number = newNumber
        }
    }
}

extension BTLEObject {
    struct State: Equatable {
        var number: Double = 0.0
        var isConnected: Bool = false
    }
}
