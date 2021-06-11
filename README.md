# RasPi-automated-On-Off-circuit
Automated safe shutdown of a Raspberry Pi single-board computer.

This board is a modified copy of the work created from  
Hochschule München, FK 04, Prof. Jürgen Plate, http://www.netzmafia.de/skripten/hardware/RasPi/Projekt-OnOff/index.html

This automated circuit acts in combination with a Python-Script (on the RasPi), shutting-off safely this Raspberry-Pi Single-Board-Computer.
This shut-off can be done through a remote Switch (activated per WLAN f.ex. per App, Browser or with a Python-Script on another System),
per Hardware-Button-Switch on the circuit or via an external 5V-Signal. It provides also the possibility to switch a concatenated
Power-Relay on/off (f.ex. for a 3D-Printer) and has a 2nd Button-Switch to switch-On the 5V-Power for the RasPi, this naturally
depending on present main-voltages...

Preliminary remarks:  
A Computer booting from a File-System needs to have a built-in **save** shutdown before turning off his (main-)power.
The Raspberry Pi alas has no buit-in safe shutdown-program and normally will be directly "killed" powering off.  
This abrupt "Power-Off" mostly causes no problems. But if just at this "shut-off"-moment the system is writing to the file-system
(f.ex. to the SD-Card), this may result in this file beeing unreadable or worse in a corrupted boot-sector - and probaby next time
the system can't boot anymore – the SD-Card (the booting-system) has to be set-up again... almost much work, which can be avoided
with an additional safe Shutdwon-Circuit (Hardware) or a simple manual Button...

This Shutdwon-Box can prevent such (worst) cases automatically. It activates a Shutdown-Routine, running on the RasPi before switching
his 5V-Power-Off. This Routine (a Python-Script) can be found on many places on the internet, but mostly it isn't activated automatically
but with a manual "Shut-down" Button. To automate this process the RasPi here gets his own 5V-Supply with a small 5V(USB)-Power-Supply
beeing always on, but switched off by the circuit.

If the Main-Power (f.ex. 230VAC or 24VDC for a 3D-Printer) is shut-off (f.ex. with a Remote-Switch), this Circuit gets the missing
Power-Voltage through an Optocoupler, which signals the Raspi (on GPIO21) to run the above mentionned shutdown-script before shutting-off
himself and after a waiting-time of about 30 seconds the circuit switches also the 5V-Power-line off, so this Power-line is no longer burdened,
consuming only a few mA (StandBy mode), waiting to the RasPi beeing powered-on again...

Design: Mains-Power (~230VAC) detected through an Optocoupler!
-------
!!! ATTENTION - DANGER: Mains Power or Voltages above 40V or currents above 30mA *flowing through human body* can cause a mortal heart-paralysis,
even after minutes, hours or days after a shock ocurred! So be aware of what you do, specially:
1. NEVER touch the board manually beeing "On"! Be cautious, put the circuit in a safe box and isolate every cable with high-voltages!
2. For (hopeful never) the case of a shock: DONT STAY ALONE, visit a doctor IN ANY CASE - if your heart stands still - possible also
after a longer time (!) and you are alone at this moment - you are definitively dead!
3. You are warned, responsibility of what you are doing with provided files here is on to you!

Function:
---------
After Main-Power Off (see the "RasPi On-Off Wiring" file):
After the RasPi has run the script and is savely "down" (but yet not "off"), having disconnected (unmounted) his file-system per script,
his 5V-Power-Supply may also be switched off. (Note: the RasPi blinks 10 times after the script is done, before beeing "down").

But: How does the On-Off-Box know when this Python-Script has finished and the inbuilt-30s-timer can begin to "count-down"?
=> The script searches for a Signal on the TX-line: Beeing "online", both Series-Lines (TX / RX) are mostly active, so this signals  
can be caught through the named TX-line-Pin on RasPi's Pin-header(output on BCM Pin 14 = GPIO TxD = Physical-Pin 8), which  
-beeing "On"- loads the Timer-Capacitor in our On-Off-Box permanently to "full-status" (+5V).  
After the RasPi went savely "down" (at the end of the Shut-Down-Script), the TX-line *isn't firing anymore*, so the 10uF Timer-Capacitor (C1)
begins to unload through his parallel resistance (R4: 3,9MOhm). On about ~1/3 of Voltage (after ~30s) the following Schmitt-Trigger activates
both Mosfets T3 and T4 (insted of a Relay-Switch as posted in the original version), which cuts the +5V-Power line off.

The difference here to a Relay-Switch is a significant lower "hold"-current while Power-"On": with these days really Low-Resistance
(P-)Mosfets, possible losses or heatings are mostly negligible.  
But if more Switching-Power is necessary (for greater loads), the P-Mosfet IRF7416 (10A/20mOhm) may be changed with a stronger type, f.ex.  
with a IRF8736 (18A/5mO) or a IRF8788 (24A/3mO), having the same package as the IRF7416, so changing without any layout-modification.

So this automated "On-Off-Switch" can be used also for the Raspberry-Pi 4, consuming 4 Amps or more, this Amperage depending also
on additional connected periphery, as screens, harddrives, coolers, etc, which in sum may consume a lot more than 4A...
