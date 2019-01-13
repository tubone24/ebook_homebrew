How to use
==========

After installation, you can use command line :command:`ebookhomebrew` ::


Show help
---------

Command option :command:`-h` shows helps. ::

    $ ebookhomebrew -h


ebookhomebrew command line interfaces provides subcommand. ::

     Choose subcommands. Usually choose "auto"

     {auto}
      auto      Make only digit file name, convert e-book file such as PDF

Also provides Options. ::

      -h, --help            show this help message and exit
      -s SRC_DIR, --src_dir SRC_DIR
                            Source directory which put original image files.
      --dst_dir DST_DIR     Destination directory which put e-book file.
      -d N,N, --digit N,N   Serial number digits you remain file name
      -e EXT, --extension EXT
                            Destination directory which put e-book file.
      -f FILENAME, --filename FILENAME
                            Destination directory which put e-book file.
      -m, --manual          Duplicate file name, solving manually.
      -r, --remove          Remove original image file.
      -y, --assume_yes      no verify users.


Auto command
------------

Rename image file to only digit and Create PDF file. ::

    $ ebookhomebrew auto -s ./tests -d 3,4 -e jpg -f test.pdf


