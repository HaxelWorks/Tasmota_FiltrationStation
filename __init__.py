import octoprint.plugin
import requests
import time
import threading
# Tasmota power strip IP address and URL
IP = "192.168.0.233"
POWER_STRIP_URL = f"http://{IP}/cm?cmnd="

def set_channel(channel, on):
    """Turn a channel on or off.
    Default channel mapping:
    Ch1 = Raspberry Pi
    Ch2 = 3D Printer
    Ch3 = Filter Fan
    Ch4 = Lights (usb 5v)
    """
    # Build the command string
    cmd = f"POWER{channel} {'ON' if on else 'OFF'}"
    # Send the request to the Tasmota power strip
    response = requests.get(POWER_STRIP_URL + cmd)
    # Print the response from the Tasmota power strip
    print(response.text)

# Define the plugin class
class TasmotaPowerStripPlugin(octoprint.plugin.StartupPlugin,
                              octoprint.plugin.TemplatePlugin,
                              octoprint.plugin.EventHandlerPlugin):
    # Initialize the plugin
    def on_after_startup(self):
        self.cancel = False
        # Turn on the printer
        set_channel(2, True)
        # Turn off the fan
        set_channel(3, False)
        
    # Implement the hook for handling events
    
    def on_event(self, event, payload):
        
        # Check if a print has started or ended
        if event == "PrintStarted":
            self.cancel = True
            # Turn on the fan
            set_channel(3, True)
            # Turn on the lights
            set_channel(4, True)
           
        elif event in ["PrintDone", "PrintCancelled", "PrintFailed"]:
            
            def turn_off():
                self.cancel = False
                """Turn off the everything after 10 minutes."""
                time.sleep(10 * 60)
                if self.cancel:
                    return
                
                set_channel(2, False)
                set_channel(3, False)
                set_channel(4, False)
                # time.sleep(1)
                # set_channel(1, False) # WARNING: Turns off the Raspberry Pi
                  
            # Start the thread
            t = threading.Thread(target=turn_off)
            t.start()


# Register the plugin
__plugin_name__ = "Tasmota Power Strip Plugin"
__plugin_pythoncompat__ = ">=3,<4"
__plugin_implementation__ = TasmotaPowerStripPlugin()