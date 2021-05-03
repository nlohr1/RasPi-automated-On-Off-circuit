# RasPi-automated-On-Off-circuit
Automated shutdown of a Raspberry Pi single-board computer.

This board is a modified copy of the work created from  
Hochschule München, FK 04, Prof. Jürgen Plate, http://www.netzmafia.de/skripten/hardware/RasPi/Projekt-OnOff/index.html

Preliminary remarks:
A Computer booting from a File-System needs to have a built-in **save** shutdown before turning off his (main-)power.
The Raspberry Pi alas has no buit-in save shutdown and normally will be directly "killed" powering off.  
This abrupt "Power-Off" mostly causes no problems. But if just at this "shut-off" moment the system is writing to the file-system
(f.ex. to the SD-Card), this may result in file beeing unreadable or worse in a corrupted boot-sector - and probaby next time
the system can't boot anymore – the SD-Card (the booting-system) has to be set-up again... almost much work, which can be avoided
with this additional safe shutdown-box. 

This Shutdwon-Box can prevent such (worst) cases. It activates a Shutdown-Routine running before switching the RasPi's 5V-Power-Off.
This Routine (a Python-Script) can be found on many places on the internet, but in most cases it isn't activated automatically
but with a manual "Shut-down" Button. To automate this process the RasPi here gets his own 5V-Supply with a (relativly small) 5V(USB)-Power-Supply.

If the Main-Power (f.ex. 230VAC or 24VDC for a 3D-Printer) is shut-off (f.ex. with a Remote-Switch), this On-Off-Box here gets the missing
Power-Voltage through an Optocoupler, which signals the Raspi (on GPIO21) to run the above mentionned shutdown-script before shutting-off himself.

!!! ATTENTION - DANGER: Main Power or Voltages above 40V or currents above 30mA *flowing through human body* can cause a mortal heart-paralysis,
even after minutes, hours or days after a shock ocurred! So be aware of what you do, specially:
1. NEVER touch the board manually beeing "On", be cautious!
2. For (hopeful never) the case of a shock: DONT STAY ALONE, visit a doctor - if your heart stands still and you are alone, nobody can reanimate you!
3. You are warned, responsibility of what you are doing with provided files here is on to you!

After Main-Power Off (see the "RasPi On-Off Wiring" file):
After the RasPi has run the script and is savely "down" (but yet not "off"), having disconnected (unmounted) his file-system per script,
his 5V-Power-Supply may also be switched off. (Note: the RasPi blinks 10 times after the script is done, before beeing "down").

But: How does the On-Off-Box know when this Python-Script has finished and the inbuilt-30s-timer can begin to "count-down"?
=> The script activates a Signal on the TX-Pin of the RasPi's Pin-header: Beeing online, the Series-Lines (TX / RX) are mostly active,
so this signals can be caught through the named TX-line (output on BCM Pin 14, GPIO TxD, Physical-Pin 8), which -beeing "On"
loads the Timer-Capacitor in our On-Off-Box permanently to "full-status" (~5V).

After the RasPi went savely "down" (at the end of the Shut-Down-Script), the TX-line *isn't firing anymore*, so the 10uF Timer-Capacitor (C1)
begins to unload through his parallel resistance (R4: 3.9mOhm). On about ~1/3 of Voltage (after ~30s) the following Schnitt-Trigger activates
Mosfets T3 and T4 (insted of a Relay-Switch as posted in the original version), which acts as a Switch and cuts the +5V-Power line off.

The difference here to a Relay-Switch is a significant lower "hold"-current while Power-"On": with these days really Low-Resistance
(P-)Mosfets, possible losses or heatings are mostly negligible. And if more Switching-Power (for greater loads) are necessary, it's
also possible to change the proposed P-Mosfet IRF7416 (10A/20mOhm) with a stronger type, f.ex. a IRF8736 (18A/5mO) or a IRF8788 (24A/3mO).

So this automated "On-Off-Switch" can be used also for the new Raspberry-Pi 4, consuming 4 Amps or more, this depending also
on additional connected periphery, as sized screens, harddrives, etc, which in sum may consume a lot more than 4A.
