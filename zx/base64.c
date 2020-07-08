#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "base64.h"

static const char base64[64] = 
{
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
    'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z', '0', '1', '2', '3',
    '4', '5', '6', '7', '8', '9', '+', '/'
};
/*
 *  以base64的编码值作为索引进行原index的索引.即逆转换表
 *  首先,A~Z、a~z、0~9、+、/共64个符号
 *  这64个符号（ASCII）作为base64_back[]的索引,其在base64[]中的索引作为base64_back[]的索引值
 *  其次,由于编码中'=(ASCII为61)'是由补的0转换成的，所以在逆转换表中index=61的位置,值为0
 *  其他index值均为-1
*/
static const char base64_back[128] = 
{
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63,
    52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1,  0, -1, -1,
    -1,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 
    15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, 
    -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
    41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1,
};

int main1(int argc, char ** argv){
    char* str = "1234";
    printf(base64_encrypt_text(str, strlen(str)));
}

char* base64_encrypt_text(const char * pbuf,int plen)
{
    int clen = (plen % 3) ? (plen/3 + 1) : (plen/3);
    //printf("clen:%d\n",clen);
    char * buf = (char *)malloc(clen*3);
    char * cbuf = (char *)malloc(clen * 4);
    if(NULL == cbuf || NULL == buf){
        exit(EXIT_FAILURE);
    }
    memset(cbuf, 0, clen*4);
    memset(buf, 0, clen*3);
    memcpy(buf, pbuf, plen);
    //printf("buf---> %s\n", buf);
    //printf("cbuf---> %s\n", cbuf);
    //编码转换
    for(int i = 0; i < clen; i++){
        //printf("&buf[i*3]---> %s\n", &buf[i*3]);
        base64_encrypt(&buf[i*3], &cbuf[i*4]);
    }
    //printf("buf---> %s\n", buf);
    //printf("cbuf---> %s\n", cbuf);
    //由于对于0进行了统一的base6_encrypt()，所以需要对末尾的'A'进行修正为'='
    if(plen % 3 == 2){//只补一个字节，对应一个'='
        cbuf[clen*4 - 1] = '=';
    }
    else if(plen % 3 == 1){//补两个字节则对应两个'='
        cbuf[clen*4 - 1] = cbuf[clen*4 - 2] = '=';
    }
    show_base64(cbuf, clen*4);
    free(buf);
    return cbuf;
}
unsigned char* base64_decrypt_text(const char * cbuf,int clen, int* tlen)
{
    int plen = clen/4;
    int zerolen = 0;
    if(cbuf[clen-1]=='=')
      zerolen++;
    if(cbuf[clen-2]=='=')
      zerolen++;
    

    char * pbuf = (char *)malloc(plen*3);

    if(NULL == pbuf){
        exit(EXIT_FAILURE);
    }
    memset(pbuf, 0, plen*3);

    for(int i = 0; i < plen; i++){
        base64_decrypt(&cbuf[i*4], &pbuf[i*3]);
    }
    int len = plen*3-zerolen;
    *tlen = len;
    //show_base64(pbuf,len);
    return pbuf;
}
void base64_encrypt(const unsigned char * pbuf, char * cbuf)
{
    int temp = (pbuf[0] << 16) | (pbuf[1] << 8) | (pbuf[2] << 0);
    for(int i = 0; i<4; i++){
        unsigned char index = (temp >> (18-i*6)) & 0x3F;
        cbuf[i] = base64[index];
    }
}
void base64_decrypt(const char * cbuf, char * pbuf)
{
    int temp = 0;
    for(int i = 0; i<4; i++){//反向索引，根据编码求得原index并进行移位异或
        temp |= base64_back[cbuf[i]] << (18-6*i);//temp的高1byte未使用
    }
    for(int i = 0; i<3; i++){//移位异或得到的temp的低三byte分别为原有三个byte
        pbuf[i] = (temp >> (16-i*8)) & 0XFF;
    }
}
void show_base64(const char * buf, int len)
{
    printf("len:%d\n",len);
    for(int i=0; i<len; i++){
        printf("%c",buf[i]);
    }
    printf("\n");
    for(int i=0; i<len; i++){
        printf("%d ",(unsigned char)buf[i]);
    }
    printf("\n");
}
