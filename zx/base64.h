#ifndef _BASE64_H_
#define _BASE64_H_

#include "stdio.h"
#include "stdlib.h"

unsigned char* base64_decrypt_text(const char* cbuf,int clen,int* tlen);
char* base64_encrypt_text(const char* pbuf,int plen);
void show_base64(const char* buf,int len);


#endif
