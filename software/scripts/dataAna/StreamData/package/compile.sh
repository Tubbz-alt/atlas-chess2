rootcint -f dictionary.cpp -c include/Linkdef.h
g++ -o StreamToRoot `root-config --cflags` dictionary.cpp src/Hitmap.cpp src/DataClass.cpp src/comm.cpp src/ReadConfigure.cpp run.cpp `root-config --glibs`

