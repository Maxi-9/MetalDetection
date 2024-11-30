//
//  ConnectionController.swift
//  MagConnect
//
//  Created by Max Schwickert on 12/31/23.
//

import Foundation
import Network



enum SendTypes: String, Decodable {
        case command = "command"
        case marker = "marker"
}

enum ReciveTypes: String, Decodable {
    case FPS = "fps"
    case Error = "error"
    case Log = "log"
    case Requested = "requested"
    case Success = "success"
    case Closing = "closing"
}

enum Commands: String, Decodable {
    case startDataCollect = "startDataCollect"
    case stopDataCollect = "stopDataCollect"
    case pauseDataCollect = "pauseDataCollect"
    case unpauseDataCollect = "unpauseDataCollect"
    case sendfps = "sendfps"
    case stopSendfps = "stopSendfps"
    case request = "request"
    case shutdown = "shutdown"
}

class ConnectionController: ObservableObject {
    @Published var connectionStatus: String = "Not connected"
    @Published var dataReceived: String = ""
    @Published var isDataCollectOn: Bool = false
    @Published var isDataCollectPaused: Bool = false
    @Published var isFpsSendOn: Bool = false
    @Published var dataBase: String = ""
    @Published var fps: [String:Float] = [:]
    @Published var timer: TimerManager? = nil
    
    @Published var logManager: LogManager = LogManager()
    @Published var hasFailed: Bool = false
    var failedMessage: String = ""
    var lastUpdateTime : Date?
    var updateTimer: DispatchSourceTimer?
    private var connection: NWConnection?
    
    func isConnecting() -> Bool {
        return connectionStatus == "Setting up" || connectionStatus == "Preparing"
    }
    
    func isFailed() -> Bool {
        return connectionStatus == "Cancelled" || connectionStatus == "Failed" || connectionStatus == "Waiting"  || connectionStatus == "Closed"
    }
    
    func isConnected() -> Bool {
        return connectionStatus == "Connected"
    }
    
    func startConnection(host:String, port:UInt16 = 12345) {
        connection = NWConnection(host: NWEndpoint.Host(host), port: NWEndpoint.Port(integerLiteral: port), using: .tcp)
        
        connection?.stateUpdateHandler = { (newState) in
            DispatchQueue.main.async {
                switch (newState) {
                    case .ready:
                        print("ready")
                        self.connectionStatus = "Connected"
                        self.receiveMessage()
                    case .setup:
                        print("setup")
                        self.connectionStatus = "Setting up"
                    case .cancelled:
                        print("cancelled")
                        self.connectionStatus = "Cancelled"
                    case .preparing:
                        print("Preparing")
                        self.connectionStatus = "Preparing"
                    default:
                        print("Failed: \(newState)")
                        self.connectionStatus = "Failed"
                        self.failedMessage = "\(newState)"

                        self.hasFailed = true
                }
            }
        }
            
        connection?.start(queue: .global())
        
        DispatchQueue.main.asyncAfter(deadline: .now() + .seconds(5)) {
            if self.isConnecting() {
                self.connection?.cancel()
                print("Connection timed out")
            }
        }

    }
    
    struct Settings: Codable {
        var shouldSendFPS: Bool?
        var dbName: String?
        var isDataCollecting: Bool?
        var isPaused: Bool?
        var fps: String?
        
        enum CodingKeys: String, CodingKey {
            case shouldSendFPS
            case dbName
            case isDataCollecting
            case isPaused
            case fps
        }
    }
    
    func updateFromJson(_ json: String) {
            let jsonData = json.data(using: .utf8)!
            let decoder = JSONDecoder()
            let newSettings = try! decoder.decode(Settings.self, from: jsonData)
            self.isDataCollectOn = newSettings.isDataCollecting ?? self.isDataCollectOn
            self.isDataCollectPaused = newSettings.isPaused ?? self.isDataCollectPaused
            self.isFpsSendOn = newSettings.shouldSendFPS ?? self.isFpsSendOn
            self.dataBase = newSettings.dbName ?? self.dataBase
       
            let Jdata = newSettings.fps?.data(using: .utf8)!
                if Jdata != nil {
                    self.fps = try! JSONDecoder().decode([String: Float].self, from: Jdata!)
                    self.lastUpdateTime = Date()  // update the last update time
                }

                // Start the timer if it's not already running
                if updateTimer == nil {
                    updateTimer = DispatchSource.makeTimerSource(queue: DispatchQueue.main) as DispatchSourceTimer
                    updateTimer?.schedule(deadline: .now(), repeating: .seconds(1))
                    updateTimer?.setEventHandler { [weak self] in
                        guard let self = self else { return }
                        let now = Date()
                        if let lastUpdateTime = self.lastUpdateTime, now.timeIntervalSince(lastUpdateTime) > 1 {
                            self.fps = self.fps.mapValues { _ in 0 }  // reset all values to 0
                        }
                    }
                    updateTimer?.resume()
                }

        
        }
    
    func receiveMessage() {
        connection?.receive(minimumIncompleteLength: 1, maximumLength: 65536) { (data, context, isComplete, error) in
            DispatchQueue.main.async {
                if let data = data, !data.isEmpty {
                    self.handleMessage(data: data)
                }
                if isComplete {
                    print("Receive complete")
                } else if let error = error {
                    print("Receive error: \(error)")
                } else {
                    self.receiveMessage()
                }
            }
        }
    }
    
    func onDeviceError(message: String) {
        logManager.addEntry(type: "Local Error", message: message)
    }
    
    func processAction(received: ReciveTypes, data: String) {
        switch received {
        case .Success:
            logManager.addEntry(type: "Success", message: data)
        case .Error:
            logManager.addEntry(type: "Error", message: data)
        case .Requested:
            updateFromJson(data)
        case .Closing:
            connectionStatus = "Closed"
        default:
            onDeviceError(message: "Error, received "+received.rawValue+" with data: "+data)
        }
    }
        
    func handleMessage(data: Data) {
        do {
            let decodedData = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]

            if let typeString = decodedData?["type"] as? String,
               let data = decodedData?["data"] as? String,
               let type = ReciveTypes(rawValue: typeString) {
                print("\"type\": \(type), \"data\": \(data)")
                    processAction(received: type, data: data)
            } else {
                print("Invalid data received")
            }
        } catch {
            print("Error decoding data: \(error)")
        }
    }
    
    
    func disconnect() {
        connection?.cancel()
        connection = nil
        connectionStatus = "Not connected"
    }
    
    
    
    // Other functions
    
    func startDataCollect() {
        guard !isDataCollectOn else { onDeviceError(message: "isDataCollectOn is already true!"); requestResync(); return }
        let messageToServer = Commands.startDataCollect.rawValue
        sendData(type: SendTypes.command, data: messageToServer)
        isDataCollectOn = true
    }
    
    func stopDataCollect() {
        guard isDataCollectOn else { onDeviceError(message: "isDataCollectOn is already false!"); requestResync(); return }
        let messageToServer = Commands.stopDataCollect.rawValue
        sendData(type: SendTypes.command, data: messageToServer)
        timer?.stop()
        timer = nil
        isDataCollectOn = false
    }
    
    func pauseDataCollect() {
        guard isDataCollectOn && !isDataCollectPaused else { onDeviceError(message: "isDataCollectPaused is already true!"); requestResync(); return }
        let messageToServer = Commands.pauseDataCollect.rawValue
        sendData(type: SendTypes.command, data: messageToServer)
        timer?.pause()
        isDataCollectPaused = true
    }
    
    func unpauseDataCollect() {
        guard isDataCollectOn && isDataCollectPaused else { onDeviceError(message: "isDataCollectPaused is already false!"); requestResync(); return }
        let messageToServer = Commands.unpauseDataCollect.rawValue
        sendData(type: SendTypes.command, data: messageToServer)
        timer?.resume()
        isDataCollectPaused = false
    }
    
    func startSendFps() {
        // guard !isFpsSendOn else { onDeviceError(message: "isFpsSendOn is already true!"); requestResync(); return }
        let messageToServer = Commands.sendfps.rawValue
        sendData(type: SendTypes.command, data: messageToServer)
        // isFpsSendOn = true
    }
    
    func stopSendFps() {
        // guard isFpsSendOn else { onDeviceError(message: "isFpsSendOn is already false!"); requestResync(); return }
        let messageToServer = Commands.stopSendfps.rawValue
        sendData(type: SendTypes.command, data: messageToServer)
        // isFpsSendOn = false
    }
    
    func startDataCollectFor(length : Int) {
        guard !isDataCollectOn else { onDeviceError(message: "can't start timed data collection, already collecting"); requestResync(); return }
        guard (length > 0) else { onDeviceError(message: "Time has to be greater then zero. Number given: \(length)"); return }
        startDataCollect()
        self.timer = TimerManager(totalTime: length, completionHandler: stopDataCollect)
        self.timer?.start()
        isDataCollectOn = true
    }
    
    func requestResync() {
        let messageToServer = Commands.request.rawValue
        sendData(type: SendTypes.command, data: messageToServer)
    }
    
    func sendShutdown() {
        let messageToServer = Commands.shutdown.rawValue
        sendData(type: SendTypes.command, data: messageToServer)
    }
    
    func sendMarker() {
        let date = Date()
        let formatter = DateFormatter()
        
        formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
        let messageToServer = formatter.string(from: date)
        sendData(type: SendTypes.marker, data: messageToServer)
    }
    
    struct JsonData: Encodable {
        var type: String
        var data: String
    }

    private func sendData(type: SendTypes, data: String) {
        let jsonData = JsonData(type: type.rawValue, data: data)
        
        do {
            let encoder = JSONEncoder()
            let json = try encoder.encode(jsonData)
            let jsonString = String(data: json, encoding: .utf8)!
            sendMessageToServer(jsonString)
        } catch {
            print("Error encoding JSON: \(error)")
        }
    }
    
    
    private func sendMessageToServer(_ message: String) {
        print(message)
        let encodedMessage = Data(message.utf8)
        connection?.send(content: encodedMessage, completion: NWConnection.SendCompletion.contentProcessed(({ (NWError) in
            if (NWError == nil) {
                print("Data sent to server")
            } else {
                print("ERROR! Error when data (Type: Data) sending. NWError: \n \(NWError!) ")
            }
        })))

    }
}
