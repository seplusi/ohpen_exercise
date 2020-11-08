# ohpen_exercise

How to run the testsuite:

1) Create virtual environment and activate it. It's optional. 

2) Install necessary packages: requests, xmlrunner, ddt, unittest-xml-reporting

3) Execute the testsuite by runnin the following command:
#python -m xmlrunner discover -t ./ -o ./junit-reports

4) XML reports are available under subfolder junit-reports
