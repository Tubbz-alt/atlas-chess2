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
        std::vector<int> _Matrix0_dv;
        std::vector<int> _Matrix1_dv;
        std::vector<int> _Matrix2_dv;
        std::vector<int> _Matrix0_mv;
        std::vector<int> _Matrix1_mv;
        std::vector<int> _Matrix2_mv;

    public:
        DataClass();
        ~DataClass();
        void setFrame(struct Frame *frame);
        std::vector<std::vector <int> > get_Hitmap(int matrix);
        std::vector<int> get_dv(int matrix);
        std::vector<int> get_mv(int matrix);
        void add_data(uint16_t data_t,int matrix_t);
        void Init(); 

};

#endif 
