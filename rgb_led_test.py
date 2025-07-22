#!/usr/bin/env python3
"""
RGB LED Test Script for Raspberry Pi
Controls a 4-pin RGB LED module with poetic flair
"""

import RPi.GPIO as GPIO
import time

# GPIO Pin Definitions
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22

def setup_gpio():
    """Initialize GPIO settings and LED pins"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Setup LED pins as outputs
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(BLUE_PIN, GPIO.OUT)
    
    # Start with all LEDs off
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.LOW)

def illuminate_red():
    """Activate the red LED with poetic description"""
    print("\n🔴 Awakening the crimson flame...")
    print("   Like sunset's final whisper across silicon dreams")
    GPIO.output(RED_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(RED_PIN, GPIO.LOW)

def illuminate_green():
    """Activate the green LED with poetic description"""
    print("\n🟢 Summoning the emerald pulse...")
    print("   Digital photosynthesis in circuits of hope")
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(GREEN_PIN, GPIO.LOW)

def illuminate_blue():
    """Activate the blue LED with poetic description"""
    print("\n🔵 Invoking the sapphire current...")
    print("   Electric oceans flowing through copper veins")
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(BLUE_PIN, GPIO.LOW)

def main():
    """Main execution flow"""
    print("═══════════════════════════════════════════")
    print("    RGB LED Symphony - First Movement")
    print("═══════════════════════════════════════════")
    
    try:
        # Initialize GPIO
        setup_gpio()
        print("\n⚡ GPIO initialized. The stage is set...")
        time.sleep(1)
        
        # Cycle through each color
        illuminate_red()
        illuminate_green()
        illuminate_blue()
        
        # Final flourish
        print("\n✨ The chromatic dance concludes...")
        print("   Until electrons meet photons again")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Performance interrupted by cosmic intervention")
    
    finally:
        # Ensure all LEDs are off and cleanup GPIO
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.LOW)
        GPIO.cleanup()
        print("\n🌙 GPIO cleaned. The circuits rest in darkness.")
        print("═══════════════════════════════════════════\n")

if __name__ == "__main__":
    main()