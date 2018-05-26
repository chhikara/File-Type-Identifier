# File-Type-Identifier
Identify file types and other details for bulk files.

Windows Instruction--
Requirements:
1.Install Python 3
2.Install BeautifulSoup4 module :-
$pip install bs4
3.Install requests module :-
$pip install requests


4.Run the python file in command line:-
$python <fileName.py>


Here file name is the python file(in our case File_Type_Identifier.py).
IMPORTANT : Make sure that the input.txt file is present in the same directory as the python file.
Also, to run python in the command line, you must have your python software path added to the environment variables.Python3 installer asks for that during installation.




Notes.
The python code takes the input file and returns a corresponding CSV File which contains all the details fetched from fileinfo.csv and information based on the directory of file as given by the input file.


As the data is being fetched from the internet, it is recommended to keep an account of the time it will require to fetch the file types. Its depends on your internet connection as well. For a rough estimate of the time required, we recommend you to first run the code for a single file and then do the mathematics for the number of files required.
