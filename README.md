# RasPi-automated-On-Off-circuit
Automated safe shutdown of a Raspberry Pi single-board computer.
                                  
![RasPi-automated-On-Off-circuit](https://github.com/nlohr1/RasPi-automated-On-Off-circuit/blob/main/Raspi-On-Off_PMos_SMD_nl.png)
**Board with soldered components (52 x 28 mm)**  

![Raspi-On-Off_PMos_SMD_n_Foto](https://github.com/nlohr1/RasPi-automated-On-Off-circuit/blob/main/Raspi-On-Off_PMos_SMD_n_Foto.png)  

This **automated** circuit acts in combination with a Python-Script (on the RasPi), shutting-off safely a Raspberry-Pi Single-Board-Computer.
Shut-off can be inizialized with a remote-controlled Switch (activated per WLAN) or with a Hardware-Button connecting one of the GPIO-Pins
of the RasPi to GND (=Ground).  
It provides the possibility to switch a concatenated Power-Relay on at startup (f.ex. to start a 3D-Printer) and a 2nd Button to manually
switch-on the 5V-Power for the RasPi (this switching "On" also the Printer-Power-Relais) and hold by the one of the GPIOs of the RasPi,
which on startup were switched high and on shutdown low.

This board is a modified copy of the work created from  
Hochschule München, FK 04, Prof. Jürgen Plate, http://www.netzmafia.de/skripten/hardware/RasPi/Projekt-OnOff/index.html

**Main attributes:**  
- integrated Schmitt-Trigger between Timing-Capacitor and Main-Switching-Mosfet,  
- detection of present Mains-Power through an optocoupler, activating the main Power-Relais (20A / 230VAC) for the machine/3D-Printer, because most
common available Remote-Switches can't **switch** safely more than a maximum of about 0,5 Amperes (~100W) - although they mostly are specified for "220V / 16A"
(= this beeing true only for the **uninterrupted** current...!).

Wiring of the System - schematic:
---------------------------------
![Wiring-Circuit](https://github.com/nlohr1/RasPi-automated-On-Off-circuit/blob/main/RasPi-On-Off-Wiring.png)

Preliminary remarks
-------------------
A Computer booting from a File-System needs to have a built-in **save** shutdown before turning off his (main-)power.
The Raspberry Pi alas has no buit-in safe shutdown-program nor Shutdown-Button and normally will be directly "killed" powering off.  
This abrupt "Power-Off" is default use and mostly causes no problems. But if just at this "shut-off"-moment the system is writing to the file-system
(f.ex. to the SD-Card), this may result in a (boot-)file beeing unreadable or worse in a corrupted boot-sector - and probaby next time
the system can't boot anymore – the SD-Card (the booting-system) has to be set-up again... almost much work, which can be avoided
with an additional Python-Script + a safe Shutdwon-Circuit (Hardware like this) or a simple manual Button activating the Script.
The advantage of this Circuit is it shuts the whole Power off, keeping only the small 5V/2A-(USB)-Power-Supply in StandBy-Mode.

This Shutdwon-Box acts automatically: On startup it activates a Shutdown-Routine Script on the RasPi, waiting for the Signal (or Button)
to Power-Off. This Routine (a Python-Script) can be found on many places on the internet, but mostly it isn't activated automatically
but with a manual "Shut-down" Button. To automate this process the RasPi here gets his own 5V-Supply **beeing always on**, but 
shorted off inside the circuit, so that the RasPi (yet beeing in StandBy-Mode) now is completely off.

Shut-down Signal by absence of Main-Power
-----------------------------------------
If the Main-Power (f.ex. 230VAC or 24VDC for a 3D-Printer) is shut-off (per Main-Switch or Remote-Switch), this Circuit gets the missing
Power through an Optocoupler, which signals the Raspi to run the above mentionned shutdown-script before the Circuit switches the
5V-Power-line off after a waiting-time of about 30 seconds. After that only the small USB-Power-Supply rests "On", consuming only
a few mA sensing for presence of Main-Power, and if so, the (USB) 5V-Power-line is switched on again.

Design: Mains-Power (~230VAC) on the Optocoupler!
-------
!!! ATTENTION - DANGER: Mains Power or Voltages above 40V or currents above 30mA *flowing through human body* can cause mortal heart-paralysis,
even after minutes, hours or days after a shock ocurred! So be aware of what you do, specially:
1. NEVER touch the board manually beeing "On" with connected Mains-Power! Be cautious, put the circuit in a safe box and isolate every cable
with high-voltages!
2. In (hopeful never) the case of a shock: DONT STAY ALONE, visit a doctor IN ANY CASE - if your heart stands still and you are alone - this
beeing possible also after a longer time (!) - you are definitively dead!
3. You are warned, responsibility of what you are doing with the provided circuit + files here is on to you!

Function
--------
On StartUp the Shutdown-Script sets BCM-Pin-18 (WPi GPIO-1) as Output + HIGH to signal our On-Off-Board that the Raspi is up and running.
This Signal on the Board loads and holds the Timer-Capacitor on our Circuit permanently at "full-status" (+5V) during RasPi's active-time.  
Meanwhile the +Signal from Optocoupler (HIGH) is connected to RasPi's BCM-Pin-23 (WPi GPIO-4) and is constantly monitored on background.
If LOW it activates the Shutdown-script.
After the RasPi has run the Shutdown script and is savely "down" (= in StandBy-Mode, but yet not "off"), having disconnected (unmounted)
his file-system (shutdown-routine "sudo shutdwon -h now"), his main 5V-Power-Supply may also be switched off as above mentionned. (Note:
the RasPi blinks 10 times while going down, before beeing inactive / in StandBy-Mode).
After being "down" (at the end of the Shut-Down-Script), Pin-18 is switched LOW. This LOW-Signal on the Circuit goes through Dual-Mosfet
T2 to the Timer-Capacitor (C1), which now unloads through his parallel resistance (R4: 3,9MOhm). On about ~1/3 of Voltage (after ~30s)
the connected Schmitt-Trigger switches Mosfets T3 and T4 off and so the +5V-Power line is cut-off.  
Using here a Power-Mosfet (=T4) insted of a Relay has the advantage of consuming negligible current, beeing active as well as in waiting
(StandBy-)Mode.  
If more Switching-Power is necessary (for greater loads as a small RasPi), the P-Mosfet IRF7416 (10A/20mOhm) simply may be exchanged with
a stronger type, f.ex. a IRF8736 (18A/5mO) or IRF8788 (24A/3mO), having identical packages as the IRF7416, so possible exchange without 
layout-modification. (I choosed here the IRF7416 due to good availability, but also other compatible Mosfets may be used as well).

This automated "On-Off-Switch" can be used for all Raspberry-Pi versions or also PC-Boxes, consuming upto 4 Amps (or even more) on 5VDC.  

---------------------------------------------------------------------------------------------------------------------
Add-On: Reset-Button for the Pi
-------------------------------
If in someway the RasPi went into its StandBy-Mode, we need a (Hardware-)Reset-Button to wake it up. Since Pi's boards as yet misses
Reset Buttons, nevertheless on most boards we may find a prepared via named "Run", whitch is the Pin we are looking for as Reset-Pin.
Connecting this pin to "GND" (often located directly beside) – through a Push-Button, the Raspi comes up again and so the
whole periphery as Printer, etc.  

---------------------------------------------------------------------------------------------------------------------
