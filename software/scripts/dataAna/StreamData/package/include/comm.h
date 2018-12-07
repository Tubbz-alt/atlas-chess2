#ifndef comm_H
#define comm_H

#include <iostream>
#include <fstream>
#include <vector>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

std::vector<int> split_string_h(std::string string_in);


struct Atlas_chess2_header {
    uint32_t atlas_chess2_h_0;
    uint32_t atlas_chess2_h_1;
    uint32_t atlas_chess2_h_2;
    uint32_t atlas_chess2_h_3;
    uint32_t atlas_chess2_h_4;
    uint32_t atlas_chess2_h_5;
    uint32_t atlas_chess2_h_6;
    uint32_t atlas_chess2_h_7;
 
};

struct Frame_Header {
    uint32_t frame_size;
    uint32_t frame_header_2;
    struct Atlas_chess2_header atlas_chess2_header;
};

//struct Payload {
//    uint16_t *content_u;
//};

struct Frame {
    struct Frame_Header frame_Header;
    uint16_t *payload; 
    int payload_size; 

};

int get_next_payload(FILE *stream, struct Payload *payload, int f_len);
int get_next_frame(FILE *stream, struct Frame *frame);
void delete_frame(struct Frame *frame);
std::vector<int> split_string_h(std::string string_in);


#endif
