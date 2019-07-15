This is a set of basic instructions I (Jacob) used to profile my code on OzStar.

**Requirements:** Have the ability to display a GUI from OzStar onto your screen.  For Mac I used *Xquartz* and for Windows I believe it's called *Xming*. 
	   
0. Launch *Xquartz*/*Xming*.  **Note**: For the GUI to be displayed I had to launch a terminal directly from *Xquartz*; right click Xquartz > Applications > Terminal.  From what I've read this isn't common behaviour but I'd recommend doing this. 

1. ``ssh`` onto OzStar using Xforwarding which forwards the Vtune GUI onto your local screen. For terminal you simply need to add the ``-Y`` option to your ``ssh`` call,  e.g. ``ssh -Y jseiler@ozstar.swin.edu.au``. If you're using *Putty* on Windows there will be an option under SSH > X11 that says *Enable X11 Forwarding* which you need to check.

2a. Load the Vtune module; ``ml vtune/2018_update2``

2b. Remember to load any modules that your code needs to run on OzStar.

2c. Recompile your code with the modules loaded to make sure everything is properly linked for your module list. 

3. Launch Vtune; ``amplxe-gui``.  This should launch an interactive screen for Vtune. 

4. Set up a new project.  You will need to specify the location of your code you want to profile (*Application*) and any input parameters that it takes (*Application parameters*). It also may be a good idea to change the *Automatically stop collection after (sec)* parameter to a few minutes; if your full program iterates a number of times but does the same calculations each iteration then it may not be necessary to run your code for the entire time.  Simply run it for a few minutes and you should get a good idea of the bottlenecks.
	
5. Start a New Analysis by clicking *New Analysis*.  Specify *CPU Sample Time* as 1ms and hit Start.
 
6. Wait patiently.

7. The summary of your code should be automatically generated. Clicking on *Bottom-Up Tree* will show you a list of functions and their corresponding CPU time.  From this you can identifiy the parts of your code that is causing the largest delay.

8. Celebrate! 
