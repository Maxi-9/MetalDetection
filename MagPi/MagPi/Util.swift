//
//  Util.swift
//  MagPi
//
//  Created by Max Schwickert on 1/13/24.
//

import Foundation
import Combine

class TimerManager: ObservableObject {
    @Published var timer: Timer? = nil
    @Published var timeRemaining: Int
    @Published var running: Bool = false
    var stopped : Bool = false
    let totalTime: Int
    var completionHandler: (() -> Void)

    init(totalTime: Int, completionHandler: @escaping (() -> Void)) {
        self.totalTime = totalTime
        self.timeRemaining = totalTime
        self.completionHandler = completionHandler
    }

    func start() {
        running = true
        self.timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { [self] _ in
            if self.timeRemaining > 0 {
                timeRemaining -= 1
            } else {
                if !stopped {
                    completionHandler()
                }
                stop()
            }
        }
    }

    func stop() {
        self.timer?.invalidate()
        running = true
        self.timer = nil
        self.timeRemaining = totalTime
        self.stopped = true
    }

    func pause() {
        self.timer?.invalidate()
        self.timer = nil
    }

    func resume() {
        start()
    }
    

}
