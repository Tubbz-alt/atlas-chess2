#ifndef DataClass_H
#define DataClass_H

#include <stdint.h>
#include <vector>
#include "comm.h"

class DataClass {
    
    private:
        std::vector<std::vector <int> > _Matrix0;
        std::vector<std::vector <int> > _Matrix1;
        std::vector<std::vector <int> > _Matrix2;

    public:
        DataClass();
        DataClass(struct Frame *frame);
        ~DataClass();
        void setFrame(struct Frame *frame);
        void Init();
        std::vector<std::vector <int> > get_Hitmap(int matrix);
        void add_data(uint16_t data_t,int matrix_t);

};

#endif 
