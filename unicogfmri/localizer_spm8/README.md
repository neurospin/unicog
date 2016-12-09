# TUTORIAL "Analysing Neurospin's localizer dataset with SPM8"

This tutorial briefly explains how to analyse the Pinel's standard localizer data with SPM8. 

As a reminder, the "localizer" consists of a 5 minutes experiment during which the participant sees various visual stimuli (checkboard, letter strings, ...), listens to spoken stimuli, performs some simple arithmetic computations, and presses response buttons. 

### Prerequisites

Data must be ready for first level analyses, i.e. they must be organized accordingly to the expected structure and preprocessed.

## Preparation

You will have to adapt the parameters in file "create_design_batches.m" (first lines of the script). The values of the onsets for Pinel's standard localizer are in file "localizer.mat" (you can check these values, just in case).

File "dirs.txt" must contain the list of the subjects names (names of the directories).

You will also have to adapt the parameters in file "create_contrasts_batches.m" (first lines of the script)

### First-level processing 
    
In Matlab, run "create_design_batches.m" in order to create the design matrix.

Then, you can run file "create_contrasts_batches.m" in order to create the contrasts for the localizer.



