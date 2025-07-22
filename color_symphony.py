#!/usr/bin/env python3
"""
🎨 Color Symphony - An Interactive RGB LED Game
Press the button to create your own light and sound show!
Perfect for your first Raspberry Pi project.
"""

import RPi.GPIO as GPIO
import time
import random

# GPIO Pin Definitions (matching your module's R, G, B pins)
RED_PIN = 17      # Connected to R pin
GREEN_PIN = 27    # Connected to G pin  
BLUE_PIN = 22     # Connected to B pin
BUZZER_PIN = 18   # Buzzer
BUTTON_PIN = 23   # Push Button

# Musical note frequencies (Hz)
NOTES = {
    'C': 261,
    'D': 294,
    'E': 329,
    'F': 349,
    'G': 392,
    'A': 440,
    'B': 493,
    'C_HIGH': 523
}

# Color patterns with their musical notes
COLOR_PATTERNS = [
    {
        'name': '🌅 Sunrise Melody',
        'colors': [(1, 0, 0), (1, 1, 0), (1, 0.5, 0)],  # Red -> Yellow -> Orange
        'notes': ['C', 'E', 'G'],
        'message': 'Dawn breaks over digital horizons...'
    },
    {
        'name': '🌊 Ocean Wave',
        'colors': [(0, 0, 1), (0, 1, 1), (0, 1, 0)],  # Blue -> Cyan -> Green
        'notes': ['E', 'G', 'B'],
        'message': 'Electric tides flow through copper shores...'
    },
    {
        'name': '🌸 Cherry Blossom',
        'colors': [(1, 0, 1), (1, 0, 0.5), (1, 0.5, 0.5)],  # Magenta -> Pink variations
        'notes': ['A', 'C_HIGH', 'E'],
        'message': 'Silicon petals bloom in spring circuits...'
    },
    {
        'name': '⚡ Lightning Storm',
        'colors': [(1, 1, 1), (0, 0, 1), (1, 1, 1)],  # White -> Blue -> White
        'notes': ['C_HIGH', 'A', 'C_HIGH'],
        'message': 'Thunder echoes through transistor clouds...'
    },
    {
        'name': '🎆 Fireworks',
        'colors': [(1, 0, 0), (0, 1, 0), (0, 0, 1)],  # Classic RGB cycle
        'notes': ['C', 'F', 'A'],
        'message': 'Celebrating electrons in festive formation...'
    }
]

class ColorSymphony:
    def __init__(self):
        self.setup_gpio()
        self.pattern_index = 0
        self.button_pressed = False
        self.running = True
        
    def setup_gpio(self):
        """Initialize all GPIO pins"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Setup LED pins as outputs first
        GPIO.setup(RED_PIN, GPIO.OUT)
        GPIO.setup(GREEN_PIN, GPIO.OUT)
        GPIO.setup(BLUE_PIN, GPIO.OUT)
        
        # Setup LED pins as PWM outputs for color mixing
        self.red_pwm = GPIO.PWM(RED_PIN, 100)
        self.green_pwm = GPIO.PWM(GREEN_PIN, 100)
        self.blue_pwm = GPIO.PWM(BLUE_PIN, 100)
        
        # Start PWM with 0% duty cycle (off)
        self.red_pwm.start(0)
        self.green_pwm.start(0)
        self.blue_pwm.start(0)
        
        # Setup buzzer as PWM for different tones
        GPIO.setup(BUZZER_PIN, GPIO.OUT)
        self.buzzer_pwm = GPIO.PWM(BUZZER_PIN, 1000)
        self.buzzer_pwm.start(0)  # Start with 0% duty cycle
        
        # Setup button with pull-up resistor
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, 
                            callback=self.button_callback, 
                            bouncetime=300)
        
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
            self.buzzer_pwm.start(10)  # Lower duty cycle for passive buzzer
            time.sleep(duration)
            self.buzzer_pwm.stop()
        else:
            time.sleep(duration)
            
    def play_pattern(self, pattern):
        """Play a complete color and sound pattern"""
        print(f"\n{pattern['name']}")
        print(f"   {pattern['message']}")
        
        for color, note in zip(pattern['colors'], pattern['notes']):
            self.set_color(*color)
            self.play_tone(NOTES[note], 0.3)
            time.sleep(0.1)
            
        # Fade out
        self.set_color(0, 0, 0)
        
    def welcome_sequence(self):
        """Play a welcome animation"""
        print("\n🎭 Welcome to Color Symphony!")
        print("Press the button to play different patterns")
        print("Each press cycles through magical light shows\n")
        
        # Quick RGB test with ascending notes
        colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        notes = ['C', 'E', 'G']
        
        for color, note in zip(colors, notes):
            self.set_color(*color)
            self.play_tone(NOTES[note], 0.2)
            
        self.set_color(0, 0, 0)
        time.sleep(0.5)
        
    def idle_animation(self):
        """Gentle breathing animation while waiting"""
        # Slow fade in and out of white
        for i in range(50):
            brightness = i / 50.0
            self.set_color(brightness * 0.3, brightness * 0.3, brightness * 0.3)
            time.sleep(0.02)
            
        for i in range(50, 0, -1):
            brightness = i / 50.0
            self.set_color(brightness * 0.3, brightness * 0.3, brightness * 0.3)
            time.sleep(0.02)
            
    def run(self):
        """Main program loop"""
        try:
            self.welcome_sequence()
            
            print("💡 Tip: Press Ctrl+C to exit gracefully")
            print("═" * 40)
            
            while self.running:
                if self.button_pressed:
                    self.button_pressed = False
                    
                    # Play current pattern
                    pattern = COLOR_PATTERNS[self.pattern_index]
                    self.play_pattern(pattern)
                    
                    # Move to next pattern
                    self.pattern_index = (self.pattern_index + 1) % len(COLOR_PATTERNS)
                    
                    # Show what's next
                    next_pattern = COLOR_PATTERNS[self.pattern_index]
                    print(f"   Next up: {next_pattern['name']}")
                else:
                    # Idle animation
                    self.idle_animation()
                    
        except KeyboardInterrupt:
            print("\n\n🌙 The symphony concludes...")
            
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Clean up GPIO resources"""
        self.set_color(0, 0, 0)
        self.red_pwm.stop()
        self.green_pwm.stop()
        self.blue_pwm.stop()
        self.buzzer_pwm.stop()
        GPIO.cleanup()
        print("✨ Until the next performance!\n")

if __name__ == "__main__":
    symphony = ColorSymphony()
    symphony.run()