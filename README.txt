DOCUMENTATION for slaclab/atlas-chess2 'ucsc-testing' branch
by Derek Hamersly
08/20/2018

SETUP
First, make sure you have downloaded Rogue and all other dependencies for this project as listed on the slaclab github page for Rogue: 
https://github.com/slaclab/rogue/blob/master/README.md

Then clone atlas-chess2 with the following commands:
	git clone https://github.com/slaclab/atlas-chess2.git
	git checkout ucsc-testing
	git branch <new-branch-name>

Now you should have the software you need to start running tests.

Finally, you may need to edit the paths within 'atlas-chess2/software/setup_template.sh' to specify the locations of python packages. When the paths are correct, RUN:

	source setup_template.sh

in order to inform python of where it should look for libraries.


OVERVIEW
FebScriptTest.py (found in atlas-chess2/software/scripts/.) is the main file that runs tests. ('Feb' refers to 'front-end board')
In FebScriptTest.py, gui() is the function that runs the guis (makes hitmaps and plots). This function is called at the end of this script. It takes two arguments: (1) the IP of the board, and (2) the configuration file for the chip. These arguments can be hardcoded depending on setup, or they can be passed via command line arguments. 

To RUN, type:

	python3 FebScriptTest.py <board IP> <path/to/config/file.yml> 
or just
	python3 FebScriptTest.py

if the board IP and config file path are hardcoded into the gui() call.

When the script is run, it will do the following:
1) Initialize connections and settings in Rogue (a bulky tool that helps organize all communications with the chip)
2) Load config file
3) Disable all pixels (takes about 10seconds)
4) You may see these warnings: 
	CRITICAL:pyrogue.UdpRssiPack.UdpRssiPack:Size arg is deprecated. Use jumbo arg instead
	ERROR:pyrogue.System.System:'Memory Error for System.feb.dac.dacPIXTHRaw at address 0x100004 Verify error. Local=0xef0x20x00x0. Verify=0x00x00x00x0. Mask=0xff0xf0x00x0'

   but these warnings don't seem to be disastrous, just a minor bug (that should be investigated).   It seems like this only happens the first time you run the script after powering on the computer anyway.
5) The test will run... 
6) To exit, press control-C a few times. If the program is still going, try closing the gui windows and then pressing control-C a few more times.

CLASSES

	I. ScanTest (see ScanTest.py)

The scan() function runs the test. ScanTest was built with the idea that most tests would consist of some kind of scan of a parameter over a range of values. This class makes it very easy to create such a test. For example, let's say we want to scan the full range of the parameter 'system.feb.dac.VPFBatt' and make histograms of hit vs. threshold for each param value. We would do this in the following way (near the end of the gui() function in FebScriptTest.py):

1) First initialize scan_test object with the parameters we care about:

	scan_test = ScanTest(scan_field='dac.VPFBatt', scan_range=range(0,32))

2) Then the scan_type must be set. Since we are not scanning over baselines or thresholds, we choose "other_scan", which is what should be used for parameter scans. This puts thresholds on the x axis by default:

	scan_test.set_scan_type("other_scan")

3) Then we must set the limits for the x axis. Since we specified "other_scan", we implied that the x axis would be threshold voltage:

	scan_test.set_x_vals(range(0,2500)) #common threshold range

4) Now we must choose what region of the chip we want to look at, specifying matrix (0-2), topleft, and block shape. Here, we set the matrix to 1, set the topleft corner of our pixel block of interest at (0,0), and set the dimensions of our rectangular region to be 8 rows by 1 column. Each matrix has 128 rows and 32 columns, so pick 0-127 for row, and 0-31 for column:

	scan_test.matrix(1)
	scan_test.set_topleft((116,2))
	scan_test.set_shape((8,1))

5) We can set more configurations for this test:
	
	scan_test.set_ntrigs(5) # sets number of times readout is triggered, separated by sleeptime
	scan_test.set_sleeptime(10) #ms
	scan_test.set_pulserStatus("OFF") #just to inform filename, doesn't control pulser status
	scan_test.set_chargeInjEnabled(0) #1 is enabled, 0 is disabled (if just interested in noise)

5) Then we must enable this block of pixels to be controlled by software. We must pass two args into scan_test as the actual enabling is done by system, and chess_control executes system commands:
	
	scan_test.enable_block(chess_control,system)

6) In order to do a controlled scan of a single parameter, other parameters must be kept constant. In my tests, I kept a dictionary ("best_vals") storing values for all the parameters and kept all but the scan_param fixed througout the scan. These parameter values can be set with:
	
	chess_control.set_val(system,<str scan_field>,<hex value of scan_field>)
Ex.     chess_control.set_val(system,'dac.VPFBatt',0xa)

Loop through all parameters and set them to whatever you want before beginning a scan.

7) Begin the scan. 'param_config_info' is just a string that gives info about the test. It is in the format "dac.VPFBatt=0xa,dac.VNatt=0xe,...etc...":
	
	scan_test.scan(chess_control,system,eventReader,param_config_info)

Now we look at the classes that facilitate ScanTest.


	II. System (see System.py)

System controls all communications between software and the board. Unfortunately there isn't much documentation for the functions that control the chip. Since System is difficult to work with, we made a new class, ChessControl, that facilitates System commands.



	III. ChessControl (see ChessControl.py)

We got tired of typing various long commands so many times, so we made this class to make these long commands easier to use. For example, we can simply call:

	chess_control.set_threshold(system,<threshold>)

instead of
 
	system.feb.dac.dacPIXTHRaw.set(<threshold value>).

This object-oriented approach makes this complex testing framework easier to use.


	IV. EventReader (see EventReader.py)

This class inherits 'rogue.interfaces.stream.Slave'. The '_acceptFrame()' method of this class is called when the readout is triggered. In this method, we accept a frame, read it, decode it, and immediately send hits to the live hitmap (if valid hits were registered). We also add the frame data to a list (self.data_frames) that will eventually be encoded into a csv file after the current histogram is saved.

	V. Hist_Plotter (see Hist_Plotter.py)

This class plots the histograms.

	VI. Hitmap_Plotter (see Hitmap_Plotter.py) 

This class plots the hitmaps.

	VII. Frame_data (see Frame_data.py)

This class decodes the binary data that is produced by the chip containing information about (1) data_valid, (2) multi_hit, (3) row, and (4) col. Each frame received is 64bits, where the first 32 make up the header, and the latter 32 make up the data.






