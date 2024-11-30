# Magnetic Field Mine Detector

## Overview
This project develops an affordable mine detection system using the Earth's magnetic field to locate unexploded ordnance (UXO) and landmines. The system uses three RT3100 magnetic sensors combined with a Raspberry Pi 4 to detect magnetic field disturbances caused by metallic objects.

## Problem Statement
- Approximately 15 people die daily from unexploded mines in farmlands
- Current mine detection methods are expensive and inefficient
- Estimated hundreds of years needed to clear mines in Ukraine alone using current technology
- Commercial mine detectors are often restricted to military use and too expensive for civilian applications

## Solution
A low-cost mine detection system that:
- Uses three RT3100 magnetic field sensors
- Processes data through a Raspberry Pi 4
- Can be mounted on a UAV for safer operation
- Costs under $200 to build

## Components
- 3x RT3100 magnetic field sensors
- 1x Raspberry Pi 4
- Portable battery pack
- Mounting hardware and cables
- Wooden beam for sensor mounting

### Cost Breakdown
| Component | Cost |
|-----------|------|
| RT3100 Sensors (3x) | $75 |
| Raspberry Pi 4 | $55 |
| Battery Pack | $20 |
| Hardware/Cables | $10 |
| **Total** | **$160** |

## Features
- Detects magnetic field disturbances at up to 0.6m distance
- Supports both vertical and horizontal sensor configurations
- Lightweight design (<500g) suitable for drone mounting
- Real-time data processing capabilities
- Customizable detection algorithms

## Technical Specifications
- Sensor sensitivity: 13 nT
- Sensor noise level: 15 nT
- Sensor spacing: 27cm center-to-center
- Operating height: 50-60cm from ground

## Future Improvements
1. Integration with GPS for precise location mapping
2. Machine learning implementation for:
   - Object depth estimation
   - Size determination
   - Improved detection accuracy
3. Advanced filtering algorithms
4. Optimization for Earth's magnetic field lines
5. Enhanced false positive/negative reduction

## Technical Documentation
The system uses I2C communication between sensors and the Raspberry Pi. Data processing includes:
- Magnetic field vector calibration
- Rotation matrix calculations
- Signal processing and filtering
- Real-time data visualization

## Installation and Setup
[To be added: Step-by-step installation instructions]

## Usage
[To be added: Operating instructions and safety guidelines]

## Safety Warning
⚠️ This device is experimental and should not be relied upon as the sole means of mine detection. Always follow proper safety protocols and consult with explosive ordnance disposal experts when dealing with potential unexploded ordnance.

## Contributing
This project is open for improvements and contributions. Key areas for development include:
- GPS integration
- Machine learning algorithms
- Signal processing optimization
- User interface improvements

## License
MIT License

Copyright (c) 2024 Max Schwickert

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgments
This project was developed as part of an 11th-grade engineering project by Max Schwickert.
