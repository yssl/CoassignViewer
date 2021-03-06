# Programming languages
./pacers.py test-assignments/c --std-input "1 2" "3 4"

./pacers.py test-assignments/cpp --std-input "1 2" "3 4"

./pacers.py --interpreter-cmd "python2" test-assignments/python2
./pacers.py --interpreter-cmd "python3" test-assignments/python3

# Program inputs
./pacers.py test-assignments/stdin-cmdarg-1 --std-input "2 1" --cmd-args "a b \"cd ef\""
./pacers.py test-assignments/stdin-cmdarg-2 --std-input "2 1" "2 2" "2 3" --cmd-args "a b" "c d" "e f"
./pacers.py test-assignments/stdin-cmdarg-3 --std-input "2 1" "2 2" "2 3" --cmd-args "a b"
./pacers.py test-assignments/stdin-cmdarg-4 --cmd-args "a b" "c d"
./pacers.py test-assignments/stdin-cmdarg-5 --std-input "2 1" "2 2" "2 3"
./pacers.py test-assignments/escape-arguments --std-input $'ab\ncd\nef'

# Projects
./pacers.py test-assignments/cmake

./pacers.py test-assignments/make

# Text and image files
./pacers.py test-assignments/txt
./pacers.py test-assignments/img

# SOURCE_FILES submission type
./pacers.py test-assignments/source_files-zip-1 --std-input "2 5" "10 20"
./pacers.py test-assignments/source_files-zip-2 --std-input "2 5" "10 20"
./pacers.py test-assignments/source_files-dir --std-input "2 5" "10 20"

# Error cases
./pacers.py test-assignments/error-cases
