//
//  ContentView.swift
//  MagPi
//
//  Created by Max Schwickert on 1/1/24.
//

import SwiftUI
import Combine
import Network

struct ContentView: View {
    @AppStorage("host") private var host = ""
    @AppStorage("port") private var port = ""
    @StateObject private var connectionController = ConnectionController()

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Connection Details")) {
                    TextField("Host", text: $host)
                        .disableAutocorrection(true)
                    TextField("Port", text: $port)
                        .keyboardType(.numberPad)
                }

                Button(action: {
                    if !host.isEmpty && !port.isEmpty {
                        connectionController.startConnection(host: host, port: UInt16(port) ?? 12345)
                    }
                }) {
                    Text("Connect")
                }
                .disabled(host.isEmpty || port.isEmpty || connectionController.isConnecting())
            }
            .navigationBarTitle("Connect to Pi", displayMode: .inline)
            .sheet(isPresented: Binding(get: { connectionController.isConnected() }, set: { _ in })) {
                DetailView(connectionController: connectionController)
            }
            .overlay(Group {
                if connectionController.isConnecting() {
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle(tint: .accentColor))
                        .scaleEffect(2)
                }
            })
            .alert(isPresented: $connectionController.hasFailed) {
                Alert(title: Text("Connection Failed"), message: Text(connectionController.failedMessage), dismissButton: .default(Text("OK")) { })
            }
        }
    }
}

struct DetailView: View {
    @ObservedObject var connectionController: ConnectionController
    @AppStorage("timelength")  private var timeLength: String = ""
    @State private var showingAlert = false
    
    var body: some View {
        
        VStack {
            NavigationView {
                VStack {
                    // Grouping related components within boxes (GroupBox)
                    
                    GroupBox(label: Text("Controls")) {
                        VStack {
                            HStack {
                                Spacer()
                                // Start, Stop, Pause, and Resume buttons
                                if connectionController.isDataCollectOn {
                                    Button("Stop") {
                                        connectionController.stopDataCollect()
                                        
                                    }
                                    Spacer()
                                    if connectionController.isDataCollectPaused {
                                        Button("Resume", action: connectionController.unpauseDataCollect)
                                    } else {
                                        Button("Pause", action: connectionController.pauseDataCollect)
                                    }
                                    Spacer()
                                    Button("Marker", action:
                                            connectionController.sendMarker)
                                } else {
                                    Button("Start") {
                                        self.showingAlert = false
                                        connectionController.startDataCollect()
                                    }
                                    
                                    Spacer()
                        
                                    Button("Start(Timed)") {
                                        self.showingAlert = true
                                    }
                                    .disabled(connectionController.isDataCollectOn)
                                }
                                Spacer()
                            }
                            if let timer = connectionController.timer {
                                HStack {
                                    ProgressView(value: Float(timer.timeRemaining), total: Float(timer.totalTime))
                                    Text(String(timer.timeRemaining))
                                }
                            }
                            
                            
                            if showingAlert {
                                ShowAlert(connectionController: connectionController, timeLength: $timeLength, showingAlert: $showingAlert)
                            }
                        }
                    }
                    GroupBox(label: Text("Stats")) {
                        NavigationLink("Show log", destination: LogView(logManager: connectionController.logManager))
                        Text("DataBase: \(connectionController.dataBase)")
                        Toggle(isOn: $connectionController.isFpsSendOn) {
                            Text("FPS Send")
                                }
                        .onChange(of: connectionController.isFpsSendOn) {
                                    if connectionController.isFpsSendOn {
                                        connectionController.startSendFps()
                                    } else {
                                        connectionController.stopSendFps()
                                    }
                                }
                        ForEach(connectionController.fps.sorted(by: <), id: \.key) { key, value in
                            Text("\(key): \((value*100).rounded()/100)")
                        }
                    }
                    Spacer()
                }
                .padding()  // Add padding for better visual separation
                .navigationBarTitle(connectionController.connectionStatus, displayMode: .inline)
                .navigationBarItems(
                    leading: Button(action: {
                        connectionController.disconnect()
                    }) {
                        Image(systemName: "chevron.backward")
                    },
                    trailing: Menu {
                        Button("Shutdown Pi", action: { connectionController.sendShutdown() })
                        Button("ReSync Settings", action: { print("Resync pressed"); connectionController.requestResync() })
                        
                    } label: {
                        Label("Options", systemImage: "ellipsis.circle")
                    })
            }
        }
        .onDisappear {
            connectionController.disconnect()
        }
    }
}

struct ShowAlert: View {
    @ObservedObject var connectionController: ConnectionController
    @Binding var timeLength: String
    @Binding var showingAlert : Bool
    
    var body: some View {
        
        return ZStack {
            
            VStack(spacing: 20) {
                TextField("Enter time length", text: $timeLength)
                    .padding()
                    .background(Color.black)
                    .keyboardType(.numberPad)
                
                Button("Submit") {
                    connectionController.startDataCollectFor(length: Int(timeLength) ?? 0)
                    showingAlert = false
                }
                .padding()
                .foregroundColor(.white)
                .clipShape(Capsule())
            }
            .frame(width: 300)
            .background(Color.black)
            .cornerRadius(10)
        }
    }
}

struct Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
