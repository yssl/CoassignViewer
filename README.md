# PACERs
Programming Assignments Compiling, Executing, and Reporting system

## Quick start

**0. Download PACERs.**  

Run ```git clone https://github.com/yssl/PACERs.git``` and ```cd PACERs```,  
or Releases > Latest release > Download source code, extract it, and ```cd``` to the extracted directory..

**1. Collect submitted source files.**  

For example:
```
<CWD>/test-assignments/c/
    |-student 01.c
    |-student 02.c
    |-student 03.c
```
![example-source]

**2. Run PACERs.**  
- On Windows: ```pacers.py test-assignments\c --std-input "1 2" "3 4"```
- On Linux: ```./pacers.py test-assignments/c --std-input "1 2" "3 4"```

You can also provide command line arguments instead of standard input, or both standard input and command line arguments as program input:

```
./pacers.py test-assignments/stdin-cmdarg-4 --cmd-args "a b" "c d"
./pacers.py test-assignments/stdin-cmdarg-3 --std-input "2 1" "2 2" "2 3" --cmd-args "a b"
```

**3. Open the generated HTML report**  

Open the generated report ```<CWD>/output/c/report-c.html``` with your favorite browser.  
The generated html file is written in unicode (utf-8), so if your browser shows broken characters, please change the browser text encoding option to unicode or utf-8.

![example-result]
To score each submission, you can open the report in WYSIWYG HTML editors (e.g. Visual Studio) and edit it.

## Requirements
- Python 2.x
- CMake
- Pygments - ```pip install pygments```  
- Unidecode - ```pip install unidecode```  
- Chardet - ```pip install chardet```  

## Note for Windows
On MS Windows, please add the path to `vcvars32.bat` to the system path. For example:
- Visual Studio 2010
```
C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\bin  
```
- Visual Studio 2015
```
C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin  
```
- Visual Studio 2017
```
C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build  
```
If you have installed multiple versions of Visual Studio and want to use one of them for PACERs, just add the path of that version to the system path.  
Currently, PACERs only supports Visual Studio for C/C++ complier on Windows.  


## Supported submission types & languages
The type of each submission is auto-detected by PACERs.

| Submission types | Meaning      |
|--------------------------|-------------------------|
| SINGLE_SOURCE_FILE        | Each submission has a single source or resource file which constitutes a single project (program).	 |
| SOURCE_FILES              | Each submission has source or resource files without any kind of project files. A single source file in a submission constitutes a single project (program).|
| CMAKE_PROJECT             | Each submission has CMakeLists.txt and constitutes a single project (program). |
| VISUAL_CPP_PROJECT        | Each submission has *.vcxproj or *.vcproj and	constitutes a single project (program). |
| MAKE_PROJECT             | Each submission has Makefile and constitutes a single project (program). |

The tested environments for each submission type are shown in the table.

| Submission types | Language | Tested environment      |
|-------------------------|--------------------------|-------------------------|
| SINGLE_SOURCE_FILE or SOURCE_FILES  | C & C++                      | Microsoft Visual Studio Community 2015 - Windows 10 (Kor)<br> Microsoft Visual Studio 2010 - Windows 10 (Kor)<br> Microsoft Visual C++ 2010 Express - Windows 8.1 with Bing (Eng)<br> gcc 4.8.4 - Ubuntu 14.04 (Kor)<br> gcc 5.4.0 - Ubuntu 16.04 (Eng)<br> gcc 7.4.0 - Ubuntu 18.04 (Eng) |
| SINGLE_SOURCE_FILE or SOURCE_FILES  | Python                      | Python 2.7.14 - Windows 10 (Kor)<br> Python 3.5.4 - Windows 10 (Kor)<br> Python 3.6.7 - Linux Mint 19.1 ("Tessa" Cinnamon)<br> Python 2.7.15+ - Ubuntu 18.04 (Eng)<br> Python 3.6.8 - Ubuntu 18.04 (Eng) |
| SINGLE_SOURCE_FILE or SOURCE_FILES | text file                     | N/A (just showing the text) |    
| SINGLE_SOURCE_FILE or SOURCE_FILES | image file                     | N/A (just showing the image, '.jpg', '.jpeg', '.gif', '.png', '.bmp' are supported.) |    
| CMAKE_PROJECT | C & C++                     | Microsoft Visual Studio Community 2015 - Windows 10 (Kor)<br> Microsoft Visual Studio 2010 - Windows 10 (Kor)<br> gcc 5.4.0 - Ubuntu 16.04 (Eng)<br> gcc 7.4.0 - Ubuntu 18.04 (Eng) |    
| VISUAL_CPP_PROJECT | C & C++                     | Microsoft Visual Studio Community 2015 - Windows 10 (Kor)<br> Microsoft Visual Studio 2010 - Windows 10 (Kor) |    
| MAKE_PROJECT | C & C++                     | gcc 7.4.0 - Ubuntu 18.04 (Eng) |    

## Try other test-assignments
- C source file tests
```
./pacers.py test-assignments/c --std-input "1 2" "3 4"
```
- C++ source file tests
```
./pacers.py test-assignments/cpp --std-input "1 2" "3 4"
```
- Python source file tests
```
./pacers.py --interpreter-cmd "python2" test-assignments/python2
./pacers.py --interpreter-cmd "python3" test-assignments/python3
```
- Standard input and/or command line arguments tests
```
./pacers.py test-assignments/stdin-cmdarg-1 --std-input "2 1" --cmd-args "a b \"cd ef\""
./pacers.py test-assignments/stdin-cmdarg-2 --std-input "2 1" "2 2" "2 3" --cmd-args "a b" "c d" "e f"
./pacers.py test-assignments/stdin-cmdarg-3 --std-input "2 1" "2 2" "2 3" --cmd-args "a b"
./pacers.py test-assignments/stdin-cmdarg-4 --cmd-args "a b" "c d"
./pacers.py test-assignments/stdin-cmdarg-5 --std-input "2 1" "2 2" "2 3"
./pacers.py test-assignments/escape-arguments --std-input $'ab\ncd\nef'
```
- CMake project tests
```
./pacers.py test-assignments/cmake
```
- Make project tests (Linux/Unix only)
```
./pacers.py test-assignments/make
```
- Visual C++ project tests (Windows only)
```
./pacers.py test-assignments/vcxproj
```
- Visual C++ GUI project tests (Windows only)
```
./pacers.py test-assignments/vcxproj-GUI --timeout 0 --exclude-patterns SDL2-2.0.4/*
```
- Error cases tests
```
./pacers.py test-assignments/error-cases
```
- Text and image file tests
```
./pacers.py test-assignments/txt
./pacers.py test-assignments/img
```
- SOURCE_FILES submission type tests
```
./pacers.py test-assignments/source_files-zip-1 --std-input "2 5" "10 20"
./pacers.py test-assignments/source_files-zip-2 --std-input "2 5" "10 20"
./pacers.py test-assignments/source_files-dir --std-input "2 5" "10 20"
```
You can run all test-assignments at once by the run-test-assignments script.
- On Windows: ```run-test-assignments.bat```
- On Linux: ```./run-test-assignments.sh```

<!--
If you checked all the test-assignments are working correctly in your PC, please let me know your tested language, compiler, and OS by submitting an issues on this project so that I could update the "Tested language, compiler(or interpreter), OS" section in this page :).
-->

## Note for interpreted languages
PACERs runs a default interpreter command based on the source file extension.  
For example, the following command would execute `python test-assignments/python2/<a python file>.py` for each .py file in `./test-assignments/python2/`:
```
./pacers.py test-assignments/python2
```
If you need to run other interpreter commands rather than default one, you can use `--interpreter-cmd` argument.  
For example, if you want to use Python 3 on a system with both Python 2 and Python 3 installed, you can do it like:
- On Windows: `py -2 pacers.py --interpreter-cmd "py -3" test-assignments/python3`
- On Linux: `python2 pacers.py --interpreter-cmd "python3" test-assignments/python3`

If you need to run some shell command before running the target script, you can use `--pre-shell-cmd` argument.  
For example, if you want to specify the Python virtual environment (using [virtualenvwrapper]) for .py files different from the environment where PACERs runs, you can do it like:
```
./pacers.py --pre-shell-cmd "workon <environment name>" test-assignments/python2
```

## Escape characters in `--std-input` or `cmd-args`

How to insert new lines (\n) or other escape characters to standard input or command line arguments depends on the shell you are using, because the shell parses all commands.

### Linux

* Bash: Use `$'...'`. See http://mywiki.wooledge.org/Quotes#Types_of_Quoting_--_The_Verbose_Version for more information.
```
$ echo $'ab\ncd'
ab
cd
$ ./pacers.py test-assignments/escape-arguments --std-input $'ab\ncd\nef'
```

### Windows

* PowerShell: Use backtick(`). See https://ss64.com/ps/syntax-esc.html for more information.
```
PS> echo "ab`ncd"
ab
cd
PS> pacers.py test-assignments/escape-arguments --std-input "ab`ncd`nef"
```

## Usage
Please read [help-pacers.txt] for detailed usage.

## Support for encodings

PACERs supports various encodings for file name, directory name, and source file contents with ```chardet``` and ```unidecode``` modules.  
You can try the test-assignments for encodings:
```
./pacers.py test-assignments/test-encoding
./pacers.py test-assignments/test-한글-cp949
./pacers.py test-assignments/test-한글-utf8
```

# pacers-cmd.py
```pacers-cmd.py``` is a PACERs script for capturing shell command output for each submission as a text file.  
Please try:
```
./pacers-cmd.py test-assignments/zip --cmds "ls" "ls -al"
```
Please read [help-pacers-cmd.txt] for detailed usage.



[example-source]: https://cloud.githubusercontent.com/assets/5915359/15735192/82744a64-28d1-11e6-85e6-fa958f96e758.png
[example-result]: https://cloud.githubusercontent.com/assets/5915359/23886079/4e0da5b6-08bb-11e7-8ec2-15ec263a0ff4.png
[help-pacers.txt]: help-pacers.txt
[help-pacers-cmd.txt]: help-pacers-cmd.txt
[virtualenvwrapper]: https://virtualenvwrapper.readthedocs.io/en/latest/
