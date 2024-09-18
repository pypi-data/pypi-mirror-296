README: 
Python's math, and scipy implementations compared to the C-wrapped implementation of the LM technique for estimating the loglikelihood function.

Prerequisites:
This code requires a Linux environment and specific Python packages:
	- Python 3: Ensure you have Python 3.11 or higher installed on your system. You can check by running python3 --version in your terminal.
	- Packages: The script relies on the following Python libraries:
		1. mpmath
		2. scipy
		3. numpy

Description:
	- This code compares 3 techniques in terms of the time and number of iterations of estimating the loglikelihood function in the context of executing Minka's fixed-point iteration in order to fit categorical count data using the Dirichlet multinomial distribution.
	- These techniques are Python's math implementation, Python's scipy implementation, and a C-wrapped implementation of the LM technique. 

Notes:
	- The folder python_tests contains multiple Python scripts that load a count dataset, randomly sample from it, and apply the LM technique to compute the loglikelihood function to model the data using Dirichlet multinomial distribution.
	- The folder comprises a set of C and associated header files that provide the C implementation of LM technique.
	- The code is configured to execute under a Linux distribution and assumes all necessary code and data files are in the same directory.
	- It is assumed that Python 3.11 or higher is installed, the code requires the packages numpy, scipy, and mpmath are installed apriori.
	- executor.py is the entry script, it loads the dataset, calls scrambler.py to randomly sample a subset of the dataset, and calls LogL-global-v5.py to fit the subset using the Dirichlet multinomial distribution while utilizing the LM technique to compute the loglikelihood function required by the Minka procedure to do the data fitting.
	- Open a terminal window and navigate to the directory containing executor.py. 
	- Run the script using the following command:
		python3 executor.py
	- The user will be prompted with a set of files (the datasets) to choose from.
	- The user will be prompted to choose one of the provided sampling ratios.
	- The user will be prompted to enter the mpmath and LM precision values, (6 was selected for both in the experiments of the accompanying paper).
	- The code will execute and produce the time, number of iterations and psi using Python's math library implementation of the loglikelihood function, then using Python's scipy implementation of the loglikelihood function, then using the LM C-wrapped implementation of the loglikelihood function.
	- For the LM technique, the results of the distance functions and goodness-of-fit tests are provided.
	
Exceptions:
		- The LM technique verifies that the loglikelihood is computable using the provided value of precision before the actual computation, if that accuracy cannot be achieved the script aborts with an informative error message of the form:
		*********** ERROR (check_with_asym1): LogL too large to ensure the desired precision in double; switch to multiprecision
		*********** ABORTING
		*********** ERROR FROM MINKA by LM PROCEDURE: LogL too large to ensure the desired precision in double; switch to multiprecision
		- The theoretical explanation for this is contained into the submitted paper, see the discussion about the asymptotic state of the system.
		- This exception was not reported with any the datasets in this directory using the precision value of 6, however, it was reported with other datasets with various levels of precision. Should the user test the code with higher values of precision, they may or may not experience this exception.

Disclaimer:
	- This script is provided for educational and research purposes only. The authors are not responsible for any misuse or unintended consequences of using this script. Any commercial use of this software is prohibited without the explicit consensus of the authors.

License:	
	- This software is licensed under the GNU General Public License version 3 (GPL-3), as published by the Free Software Foundation. You can find a copy of the license at https://www.gnu.org/licenses/gpl-3.0.en.html
	

Authors:
	- Sherenaz Al-Haj Baddar (s.baddar@ju.edu.jo)
	- Alessandro Languasco (alessandro.languasco@unipd.it)
	- Mauro Migliardi (mauro.migliardi@unipd.it)
	
	
	