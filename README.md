# 🎨 Raspberry Pi Color Symphony

A beginner-friendly interactive light and sound show using RGB LED, buzzer, and button!

## 🛠️ Hardware Setup

### Components Needed:
- 1x RGB LED (common cathode)
- 1x Active buzzer
- 1x Push button
- 4x 220Ω resistors (for RGB LED and buzzer)
- 1x 10kΩ resistor (optional, for button pull-up)
- Jumper wires
- Breadboard

### Wiring Diagram:
```
RGB LED:
- Red pin → 220Ω resistor → GPIO 17
- Green pin → 220Ω resistor → GPIO 27
- Blue pin → 220Ω resistor → GPIO 22
- Common cathode → GND

Buzzer:
- Positive → 220Ω resistor → GPIO 18
- Negative → GND

Button:
- One side → GPIO 23
- Other side → GND
(Internal pull-up resistor is used)
```

## 🚀 Getting Started

1. **Clone the repository on your Raspberry Pi:**
   ```bash
   git clone https://github.com/ilaydabdogan/pi5.git
   cd pi5
   ```

2. **Run the interactive show:**
   ```bash
   python3 color_symphony.py
   ```

3. **Press the button** to cycle through different light patterns!

## 🎭 Features

- **5 Unique Patterns**: Each with its own color sequence and melody
  - 🌅 Sunrise Melody
  - 🌊 Ocean Wave
  - 🌸 Cherry Blossom
  - ⚡ Lightning Storm
  - 🎆 Fireworks

- **Interactive**: Press the button to change patterns
- **Musical**: Each color has a corresponding musical note
- **Poetic**: Each pattern tells a tiny story
- **Idle Animation**: Gentle breathing effect when waiting

## 🎓 Learning Points

This project teaches:
- GPIO control (input and output)
- PWM for LED brightness and buzzer tones
- Event-driven programming (button interrupts)
- Object-oriented Python
- Hardware-software integration

## 📝 Scripts

- `rgb_led_test.py` - Simple RGB LED test
- `color_symphony.py` - Interactive light and sound show

## 🔧 Troubleshooting

- **No light?** Check your wiring and resistor values
- **No sound?** Make sure you're using an active buzzer
- **Button not working?** Ensure good connections and proper grounding
- **Permission error?** Run with `sudo` if needed: `sudo python3 color_symphony.py`

## 🌟 Next Steps

Try modifying the code to:
- Add your own patterns
- Change the musical notes
- Create longer sequences
- Add more buttons for direct pattern selection

Happy tinkering! 🤖✨