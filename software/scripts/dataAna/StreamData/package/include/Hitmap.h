#ifndef Hitmap_H
#define Hitmap_H

#include <vector>
#include <stdint.h>

class Hitmap {

    public:
        int _hitmap[4096];
        char *_name;
        void add(uint16_t data_16);
        Hitmap();
        ~Hitmap();
        int *getHitmap();


};



#endif
