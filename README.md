
# DNA-Sequencer-Kinetic-Analysis

**High Throughput Quantification of Short Nucleic Acid Samples by Capillary Electrophoresis with Automated Data Processing**

Dangerfield TL, Huang NZ, Johnson KA. High Throughput Quantification of Short Nucleic Acid Samples by Capillary Electrophoresis with Automated Data Processing [published online ahead of print, 2021 May 9]. Anal Biochem. 2021;114239. doi:10.1016/j.ab.2021.114239
https://pubmed.ncbi.nlm.nih.gov/33979658/







**If you're looking to edit the program, all the files for version 2.0 should be in *DNA-Sequencer-Kinetic-Analysis/docs/v2.0 files/***
- *plot_fsa_v2.py* has all the logic and quantification code
- *seq_analysis_v2.py* handles all the pyqt5 interaction with *ui_begin_v2.py*
- *ui_begin_v2.py* is the GUI created in pyqt5.
- The .ui file that can be opened in QtDesigner is found in: *DNA-Sequencer-Kinetic-Analysis/pyqt5/v2.0 files/begin_v2.ui*

Used to quickly quantify short nucleotide fragments from capillary electrophoresis. Download can be found in the releases. Manual can be found in the installer.
After you download the program from the installer, the program should be in an .exe called seq_analysis_v2.exe.
If you created a desktop icon, it should be DNA Sequencer Analysis Software v2.0.

![program files](https://user-images.githubusercontent.com/29495707/114663417-e7687000-9cbf-11eb-9fea-f9bfd693987e.png)

Burst on PThio DNA is the example .txt file. (The hello world of the program).
Electropherogram fsa Files folder contains all the .fsa files from the sequencer.

![fsa files](https://user-images.githubusercontent.com/29495707/114663603-357d7380-9cc0-11eb-949c-237b5389d72b.png)

Example output files in *Example Output* folder

![ex output](https://user-images.githubusercontent.com/29495707/114663751-69589900-9cc0-11eb-901a-61ffc21639e0.png)

*Burst_on_PThio_output_text* files are for unadulterated Burst on PThio DNA data.
*Burst_on_PThio_output_text_deleted* files are for Burst on PThio DNA data with the 28mer data deleted.

*unins000* is the uninstaller link.

Contact at nhuang110@utexas.edu for questions
