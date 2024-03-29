# ki6487

Software to drive the Keithley 6487 picoammeter using serial, usb serial or usb GPIB (Prologix)


## Requirements

   pip install serial

for developpement
   
   pip install ipython


## Configure the Keithley

press the **COMM** button and select the interface RS323 or GPIB using the up and down button in the range section. And press **Enter** to select.

To access parameters press the **config/local** button and then **comm** it will display the information for the selected protocol.

For GPIB:
  - ADDR: 22
  - LANG: SCPI (but can be DDC or 488.1)

For RS232:
  - BAUD: 57.6 k
  - FLOW: None
  - TX-TERM: CR
  - PARITY: None
  - BITS: 8
  

Notes:

   these informtation are important to drive the Keithley.
   that for the present software LANG of GPIB should be SCPI


## Other ressources


   The documentation:
      https://www.tek.com/low-level-sensitive-and-specialty-instruments/series-6400-picoammeters-manual/model-6485-model-6487

   Other software
      https://github.com/EPFL-LPI/keithley-picoammeter-controller/tree/master (GUI but uses visa)