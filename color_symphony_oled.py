#!/usr/bin/env python3
"""
🎨 Color Symphony with OLED Display
Interactive RGB LED + Buzzer + OLED show!
"""

import RPi.GPIO as GPIO
import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont

# GPIO Pin Definitions
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22
BUZZER_PIN = 18
BUTTON_PIN = 23

# OLED setup (128x64, I2C address 0x3C)
serial = i2c(port=1, address=0x3C)
oled = ssd1306(serial)

# Musical note frequencies (Hz)
NOTES = {
    'C': 261, 'D': 294, 'E': 329, 'F': 349,
    'G': 392, 'A': 440, 'B': 493, 'C_HIGH': 523
}

# Color patterns with their musical notes
COLOR_PATTERNS = [
    {
        'name': 'Sunrise',
        'icon': '🌅',
        'colors': [(1, 0, 0), (1, 0.3, 0), (1, 0.5, 0), (1, 0.7, 0), (1, 1, 0), (1, 1, 0.5), (1, 0.5, 0)],
        'notes': ['C', 'D', 'E', 'F', 'G', 'A', 'G'],
        'durations': [0.4, 0.3, 0.3, 0.3, 0.5, 0.4, 0.6]
    },
    {
        'name': 'Ocean Wave',
        'icon': '🌊',
        'colors': [(0, 0, 1), (0, 0.3, 1), (0, 0.6, 1), (0, 1, 1), (0, 1, 0.6), (0, 1, 0.3), (0, 1, 0)],
        'notes': ['E', 'F', 'G', 'A', 'B', 'A', 'G'],
        'durations': [0.5, 0.3, 0.3, 0.4, 0.5, 0.3, 0.6]
    },
    {
        'name': 'Cherry Blossom',
        'icon': '🌸',
        'colors': [(1, 0, 1), (1, 0, 0.7), (1, 0.2, 0.5), (1, 0.4, 0.4), (1, 0.5, 0.5), (1, 0.3, 0.6)],
        'notes': ['A', 'B', 'C_HIGH', 'E', 'C_HIGH', 'A'],
        'durations': [0.4, 0.3, 0.5, 0.4, 0.3, 0.7]
    },
    {
        'name': 'Lightning',
        'icon': '⚡',
        'colors': [(1, 1, 1), (0, 0, 1), (1, 1, 1), (0.5, 0.5, 1), (1, 1, 1), (0, 0, 0.5), (1, 1, 1)],
        'notes': ['C_HIGH', 'A', 'C_HIGH', 'G', 'C_HIGH', 'E', 'C_HIGH'],
        'durations': [0.2, 0.2, 0.2, 0.3, 0.2, 0.3, 0.5]
    },
    {
        'name': 'Fireworks',
        'icon': '🎆',
        'colors': [(1, 0, 0), (1, 0.5, 0), (0, 1, 0), (0, 0.5, 1), (0, 0, 1), (1, 0, 1), (1, 0, 0)],
        'notes': ['C', 'E', 'G', 'C_HIGH', 'G', 'E', 'C'],
        'durations': [0.3, 0.3, 0.3, 0.5, 0.3, 0.3, 0.6]
    },
    {
        'name': 'Love for Boogie',
        'icon': '💕',
        'colors': [(1, 0.2, 0.3), (1, 0.4, 0.5), (1, 0.6, 0.6), (1, 0.8, 0.7), (1, 0.6, 0.8), (1, 0.4, 0.6)],
        'notes': ['G', 'E', 'G', 'A', 'E', 'C'],
        'durations': [0.6, 0.4, 0.6, 0.8, 0.6, 1.0]
    }
]

class ColorSymphonyOLED:
    def __init__(self):
        self.setup_gpio()
        self.setup_oled()
        self.pattern_index = 0
        self.button_pressed = False
        self.running = True
        
    def setup_gpio(self):
        """Initialize all GPIO pins"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Setup LED pins
        GPIO.setup(RED_PIN, GPIO.OUT)
        GPIO.setup(GREEN_PIN, GPIO.OUT)
        GPIO.setup(BLUE_PIN, GPIO.OUT)
        
        self.red_pwm = GPIO.PWM(RED_PIN, 1000)
        self.green_pwm = GPIO.PWM(GREEN_PIN, 1000)
        self.blue_pwm = GPIO.PWM(BLUE_PIN, 1000)
        
        self.red_pwm.start(0)
        self.green_pwm.start(0)
        self.blue_pwm.start(0)
        
        # Setup buzzer
        GPIO.setup(BUZZER_PIN, GPIO.OUT)
        self.buzzer_pwm = GPIO.PWM(BUZZER_PIN, 1000)
        self.buzzer_pwm.start(0)
        
        # Setup button
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, 
                            callback=self.button_callback, 
                            bouncetime=300)
    
    def setup_oled(self):
        """Initialize OLED display"""
        # Try to load fonts
        try:
            self.font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
            self.font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
        except:
            self.font = ImageFont.load_default()
            self.font_large = self.font
            
    def button_callback(self, channel):
        """Handle button press events"""
        self.button_pressed = True
        
    def set_color(self, r, g, b):
        """Set RGB LED color (values 0-1)"""
        self.red_pwm.ChangeDutyCycle(r * 100)
        self.green_pwm.ChangeDutyCycle(g * 100)
        self.blue_pwm.ChangeDutyCycle(b * 100)
        
    def play_tone(self, frequency, duration):
        """Play a tone on the passive buzzer"""
        if frequency > 0:
            self.buzzer_pwm.ChangeFrequency(frequency)
            self.buzzer_pwm.start(10)
            time.sleep(duration)
            self.buzzer_pwm.stop()
        else:
            time.sleep(duration)
            
    def display_pattern_info(self, pattern, note_index=None):
        """Update OLED with pattern information"""
        with canvas(oled) as draw:
            # Pattern name at top
            draw.text((10, 5), pattern['name'], font=self.font_large, fill="white")
            
            # Progress bar
            if note_index is not None:
                progress = (note_index + 1) / len(pattern['notes'])
                bar_width = int(100 * progress)
                draw.rectangle((14, 30, 14 + bar_width, 35), fill="white")
                draw.rectangle((14, 30, 114, 35), outline="white")
            
            # Current note
            if note_index is not None and note_index < len(pattern['notes']):
                note_text = f"Note: {pattern['notes'][note_index]}"
                draw.text((40, 45), note_text, font=self.font, fill="white")
            
            # Pattern number
            pattern_num = f"{self.pattern_index + 1}/{len(COLOR_PATTERNS)}"
            draw.text((90, 50), pattern_num, font=self.font, fill="white")
        
    def display_idle(self):
        """Display idle screen"""
        with canvas(oled) as draw:
            # Title
            draw.text((15, 10), "Color Symphony", font=self.font_large, fill="white")
            
            # Instructions
            draw.text((20, 35), "Press button", font=self.font, fill="white")
            draw.text((25, 48), "to start!", font=self.font, fill="white")
        
    def play_pattern(self, pattern):
        """Play a complete color and sound pattern"""
        durations = pattern.get('durations', [0.3] * len(pattern['notes']))
        
        for i, (color, note, duration) in enumerate(zip(pattern['colors'], pattern['notes'], durations)):
            self.display_pattern_info(pattern, i)
            self.set_color(*color)
            self.play_tone(NOTES[note], duration)
            time.sleep(0.05)
            
        # Fade out
        self.set_color(0, 0, 0)
        
    def welcome_sequence(self):
        """Play a welcome animation"""
        # Display welcome message
        with canvas(oled) as draw:
            draw.text((20, 20), "Welcome to", font=self.font, fill="white")
            draw.text((10, 35), "Color Symphony!", font=self.font_large, fill="white")
        
        # Quick RGB test
        colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        notes = ['C', 'E', 'G']
        
        for color, note in zip(colors, notes):
            self.set_color(*color)
            self.play_tone(NOTES[note], 0.2)
            
        self.set_color(0, 0, 0)
        time.sleep(0.5)
        
    def run(self):
        """Main program loop"""
        try:
            self.welcome_sequence()
            time.sleep(1)
            self.display_idle()
            
            while self.running:
                if self.button_pressed:
                    self.button_pressed = False
                    
                    # Play current pattern
                    pattern = COLOR_PATTERNS[self.pattern_index]
                    self.play_pattern(pattern)
                    
                    # Move to next pattern
                    self.pattern_index = (self.pattern_index + 1) % len(COLOR_PATTERNS)
                    
                    # Show idle screen
                    time.sleep(0.5)
                    self.display_idle()
                else:
                    # Simple breathing LED while idle
                    for i in range(50):
                        brightness = i / 50.0
                        self.set_color(brightness * 0.1, brightness * 0.1, brightness * 0.1)
                        time.sleep(0.01)
                    for i in range(50, 0, -1):
                        brightness = i / 50.0
                        self.set_color(brightness * 0.1, brightness * 0.1, brightness * 0.1)
                        time.sleep(0.01)
                    
        except KeyboardInterrupt:
            print("\n\nSymphony concludes...")
            
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Clean up resources"""
        # Clear OLED
        oled.clear()
        
        # Turn off LEDs
        self.set_color(0, 0, 0)
        self.red_pwm.stop()
        self.green_pwm.stop()
        self.blue_pwm.stop()
        self.buzzer_pwm.stop()
        GPIO.cleanup()
        print("Until next time!\n")

if __name__ == "__main__":
    symphony = ColorSymphonyOLED()
    symphony.run()