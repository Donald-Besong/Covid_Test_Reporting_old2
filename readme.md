<div id="top"></div>
<!--
*** Thanks for checking out my project
*** Dr Donald O. Besong
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="http://github.com/Donald-Besong">
    <img src="src/data/images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Donald's Covid test Calculations</h3>

  <p align="center">
    project_description
    <br />
    <a href="http://github.com/Donald-Besong/Covid_Test"><strong>Explore the docs »</strong></a>
  </p>
</div>




## How to test the program
<p>
Assume that you would like to travel, and you have been sent a test kit. 
You will not be allowed to travel unless your result is
negative. The test kit contains eight test strips.
</p>
The id's of your strips are shown on your test strips. Please understand that
these are valid id's from the a huge database with millions of id's, but in this prototyoe
it is just my small data file <b>/src/data/data.xlsx</b>. My file has a total
of 60 numbers from x000001 to x000060. Therefore, you can use any of the numbers 
as your test strip. 
<p>
There are two kinds of test I would like you to do. 

1. Testing whether the code actually does what it is intended to do: 
For this purpose you have to look at the data file and select a stip 
id from sheet (or group) S1, S2, or S3.
Please also take note of the value that results in positive or negative.
Then run the test as described below, with those values. Then compare
the result from the program with the corresponding spreadsheet.
Please remember that the values are simply a representation of the lines
you would see on your test trip after the swab and test (please refer to the publication.)

2. Testing whether you can fake a desired result. 
For this purpose, do not look at the data file! Select a stip 
id (x000001 to x000060), without a clue as to which sheet (or group) it belongs.
Please also guess a value that you wish results in a negative.
Then run the test as described below, with those values.
Keep chosing different strips and testing. In the end, your score
as ti how successful you are at cheating will be calculated.
Please do not do the same strip id more than once,
because in real life you only use a strip once(please refer to the publication).
In real life, once a candidate's results are calculated from a strip, that strip
should be deleted from the database. In this prototype, I do not delete, for simplicity.
</p>
           


## Instructions

1. Clone the repository
2. Make sure that in your command line, you are in the root folder, which contains
   requirements.txt, and all the code.
3. virtualenv -p python3 cov_env3

4. Activate the virtual environment  . cov_env3/bin/activate

5. Install python packages in requirements.txt using pip in your python3
environment   
  

5. Run the following command, changing the argument values:
<p align="center"> python3 src/main_program.py --which_test=test1 --name=Jane Dough --strip_id=x000001 --value=101 </p>
<br>
--which_test=test1 if you need the first test listed in the previous section,
--which_test=test2 for the second test.
<br>
Please replace with your name, strip number and test result.
