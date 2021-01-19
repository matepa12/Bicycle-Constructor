Welcome to my project - Bicycle Constructor!

In this program you can compose your bicycle.

Python packages used by Bicycle Constructor: os, sqlite3, PySimpleGUI (external).

During first run program creates database called "bicycle_database.sqlite". Inside you may find tables:
  "companies", "subsystem_groups",  "part_groups",  "parts", "custom_subsystems". 
Tables "subsystem_groups" and "part_groups" are premade to contain specific bicycle subsystems and parts. There is no possibility to change them inside the program.

To make a user life easier I've prepared PyInstaller packages. .zip files are located in proper folder in repo.
For PyInstaller packages:

To run a program under Windows you need to upnack .zip into desired directory and open Bicycle Constructor folder. 
Inside you may find executable file called:	
	main.exe

To run a program under Linux you need to upnack .zip into desired directory and open Bicycle Constructor folder in terminal. 
Then you can simply run it by command:

./main


If you're struggling with access to the folder:	
	you may have distro, which supports mouse Right Key or Shift + Right Key to open a folder in terminal,	
	or you can change the directory directly in terminal by using 'cd' command.		

Have fun!
