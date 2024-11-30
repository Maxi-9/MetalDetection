//
//  LogManager.swift
//  MagPi
//
//  Created by Max Schwickert on 1/2/24.
//

import Foundation
import SwiftUI


class LogManager: ObservableObject {
    @Published var entries: [LogEntry] = []
    
    func addEntry(type:String, message: String) {
        let entry = LogEntry(message: message, type: type, date: Date())
        entries.append(entry)
    }
}

struct LogEntry: Identifiable {
    let id = UUID()
    let message: String
    let type: String
    let date: Date
}

struct LogEntryView: View {
    let entry: LogEntry
    @State private var isMessageVisible = false

    var body: some View {
        VStack(alignment: .leading) {
            HStack {
                Text(entry.date, formatter: DateFormatter.shortDate)
                    .font(.system(size: 12))
                    .foregroundColor(.gray)
                Spacer()
                Text(entry.type)
                    .font(.system(size: 16, weight: .bold))
                Spacer()
                Button(action: {
                    self.isMessageVisible.toggle()
                }) {
                    Text(isMessageVisible ? "Hide Message" : "Show Message")
                        .font(.system(size: 14))
                        .foregroundColor(.blue)
                }
            }
            if isMessageVisible {
                Text(entry.message)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .fixedSize(horizontal: false, vertical: true)
                    .padding(.top, 8)
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(8)
    }
}

extension DateFormatter {
    static let shortDate: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateStyle = .short
        formatter.timeStyle = .medium
        return formatter
    }()
}

struct LogView: View {
    @ObservedObject var logManager: LogManager

    var body: some View {
        List(logManager.entries, id: \.id) { entry in
            LogEntryView(entry: entry)
        }
        .listStyle(.plain)
        .background(Color.gray.opacity(0.1))
        .scrollContentBackground(.hidden)
    }
}

func addAfterOneSec(log:LogManager) {
    let randomAction = Int.random(in: 1...3)

    switch randomAction {
    case 1:
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            log.addEntry(type: "log", message: "Lorem ipsum dolor sit amet, consectetur adipiscing elit")
            addAfterOneSec(log: log)
        }
    case 2:
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            log.addEntry(type: "error", message: "Ut enim ad minim veniam")
            addAfterOneSec(log: log)
        }
    case 3:
        DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
            log.addEntry(type: "other", message: "Duis aute irure dolor in reprehenderit in voluptate")
            addAfterOneSec(log: log)
        }
    default:
        break
    }
}

struct LogView_Previews: PreviewProvider {
    static var previews: some View {
        let log = LogManager()
        addAfterOneSec(log: log)
        
        return VStack {
            LogView(logManager: log).padding()
        }
    }
}
