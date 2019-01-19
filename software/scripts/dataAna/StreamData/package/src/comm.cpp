#include "../include/comm.h"
#include <vector>
#include <stdlib.h>

//int get_next_payload(FILE *stream, struct Payload *payload, int f_len){
//    payload->content_u = (uint16_t *) malloc(f_len);
//    if (fread(payload->content_u, f_len,1,stream)==1){
//        return 0;
//    } else {
//        free(payload->content_u);
//        return 1;
//    }
//
//}

int get_next_frame(FILE *stream, struct Frame *frame){
    if (fread(frame, sizeof frame->frame_Header,1,stream)==1){
         //header is 40 bytes in total 
        uint32_t frame_length=((frame->frame_Header.frame_size)-36)/8; // size of the payload in unit of bytes
        if (frame_length == 0){
            std::cout<< "could read the header but length is 0"<<std::endl;
            frame->payload=NULL;
            frame->payload_size =0;
            return 1;
        }
        else {
          //  std::cout<<frame_length<<std::endl;
            long pos_now=ftell(stream);
            //if (1){
            if (ftell(stream)- pos_now < frame->frame_Header.frame_size){
                frame->payload = (uint16_t *) malloc(frame_length*8);
                if (fread(frame->payload,frame_length*8,1,stream)!=0){
                   frame->payload_size = frame_length;
                   return 0;
                }
                else{
                  free(frame->payload);
                  std::cout<<"__end of file"<<std::endl;
                  return 1;
               }
            }
            else { std::cout<<"errors"<<std::endl; return 1;}
            }
        }else {
        std::cout<<"end of file"<<std::endl;
        return 1;
    }
}   

void delete_frame(struct Frame *frame){
   free(frame->payload);

}

std::vector<int> split_string_h(std::string string_in) {

    std::vector<int> outp;
    std::size_t split_point=string_in.find('=');
    if (split_point<=string_in.size()){
        std::string s1=string_in.substr(0,split_point);
        std::string s2=string_in.substr(split_point+1);
        int n1=atoi(s1.c_str());
        int n2=atoi(s2.c_str());
        outp.push_back(n1);
        outp.push_back(n2);
    }
    else{
        std::string s1=string_in;
        int n1=atoi(s1.c_str());
        //std::cout<< n1 <<std::endl;
        
        outp.push_back(n1);

    }
    return outp;

}
