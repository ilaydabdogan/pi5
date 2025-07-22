#!/usr/bin/env python3
"""
Hardware Debug Script - Test each component individually
"""

import RPi.GPIO as GPIO
import time

# GPIO Pin Definitions
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22
BUZZER_PIN = 18
BUTTON_PIN = 23

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Setup outputs
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(BLUE_PIN, GPIO.OUT)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    
    # Setup button
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    print("GPIO setup complete!")

def test_led_direct():
    """Test LED with direct HIGH/LOW"""
    print("\n=== Testing RGB LED (Direct) ===")
    
    # Test common cathode (HIGH = ON)
    print("Testing as Common Cathode (HIGH = ON):")
    
    print("RED on...")
    GPIO.output(RED_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(RED_PIN, GPIO.LOW)
    
    print("GREEN on...")
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    
    print("BLUE on...")
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(BLUE_PIN, GPIO.LOW)
    
    # Test common anode (LOW = ON)
    print("\nTesting as Common Anode (LOW = ON):")
    
    print("RED on...")
    GPIO.output(RED_PIN, GPIO.LOW)
    time.sleep(1)
    GPIO.output(RED_PIN, GPIO.HIGH)
    
    print("GREEN on...")
    GPIO.output(GREEN_PIN, GPIO.LOW)
    time.sleep(1)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    
    print("BLUE on...")
    GPIO.output(BLUE_PIN, GPIO.LOW)
    time.sleep(1)
    GPIO.output(BLUE_PIN, GPIO.HIGH)

def test_buzzer():
    """Test buzzer with different methods"""
    print("\n=== Testing Buzzer ===")
    
    # Simple on/off test
    print("Buzzer ON (simple)...")
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    time.sleep(0.5)
    
    # PWM test
    print("Buzzer with PWM (tone)...")
    pwm = GPIO.PWM(BUZZER_PIN, 1000)
    pwm.start(50)
    time.sleep(0.5)
    pwm.stop()

def test_button():
    """Test button input"""
    print("\n=== Testing Button ===")
    print("Press the button 3 times (or Ctrl+C to skip)...")
    
    presses = 0
    last_state = GPIO.input(BUTTON_PIN)
    
    try:
        while presses < 3:
            current_state = GPIO.input(BUTTON_PIN)
            
            # Detect button press (HIGH to LOW transition)
            if last_state == GPIO.HIGH and current_state == GPIO.LOW:
                presses += 1
                print(f"Button pressed! ({presses}/3)")
                time.sleep(0.3)  # Debounce
                
            last_state = current_state
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("Button test skipped")

def main():
    try:
        setup()
        
        print("\n🔧 HARDWARE DEBUG MODE 🔧")
        print("This will test each component individually")
        print("Watch your hardware and note what works!\n")
        
        test_led_direct()
        test_buzzer()
        test_button()
        
        print("\n✅ Debug complete!")
        print("\nNOTES:")
        print("- If LED worked with 'Common Anode', you have a common anode LED")
        print("- If buzzer was quiet, try connecting VCC to 5V instead of 3.3V")
        print("- If button didn't work, check wiring or try without pull-up")
        
    except KeyboardInterrupt:
        print("\n\nDebug interrupted")
    finally:
        GPIO.cleanup()
        print("GPIO cleaned up")

if __name__ == "__main__":
    main()