#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "base64.h"

typedef unsigned char uchar;
char* encode_demo(char* scr, int timevalue);

uchar KeyMap[256]=
{ 12, 118, 170, 84, 3, 35, 23, 38,163, 162, 75, 114, 77, 244, 146,
  65, 9, 100, 76, 175, 0, 139, 254, 36, 15, 247, 113, 244, 194, 110, 
  247, 252, 114, 142, 192, 9, 184, 221, 102, 206, 58, 166, 12, 48, 
  252, 109, 34, 184, 129, 56, 65, 96, 50, 244, 102, 37, 218, 212, 
  94, 165, 84, 37, 27, 108, 250, 173, 154, 182, 159, 152, 163, 40, 
  177, 212, 235, 52, 58, 141, 62, 147, 171, 189, 76, 141, 47, 54, 
  100, 87, 249, 152, 80, 232, 237, 80, 70, 182, 90, 231, 205, 31, 
  112, 244, 12, 88, 171, 101, 153, 41, 129, 254, 87, 196, 20, 163, 
  218, 69, 232, 78, 226, 210, 40, 220, 110, 116, 227, 204, 230, 212,
  169, 104, 166, 47, 132, 110, 134, 15, 133, 154, 195, 88, 138, 190, 
  253, 166, 157, 213, 62, 121, 136, 89, 238, 135, 70, 188, 86, 184, 
  157, 63, 33, 114, 214, 15, 16, 110, 68, 59, 251, 213, 39, 176, 164, 
  120, 113, 85, 34, 240, 159, 123, 23, 125, 117, 149, 114, 23, 66, 
  173, 75, 194, 161, 93, 229, 64, 163, 32, 26, 223, 192, 213, 127, 
  240, 125, 196, 77, 89, 209, 235, 148, 48, 112, 12, 79, 169, 188, 
  214, 172, 89, 176, 121, 97, 225, 3, 5, 131, 232, 71, 4, 18, 245, 
  53, 237, 226, 249, 140, 176, 28, 55, 71, 175, 161, 193, 232, 105,
  239, 61, 140, 95, 49, 181, 223, 150, 220, 100, 85, 114, 33, 39};


int main(int argc, char **argv)
{
//    if(argc != 3){
 //       printf("number of parameter error:\n"); 
 //       printf("\t./base64 -d(e) text\n");
 //       exit(EXIT_FAILURE);
 //   }
 //
  char *s = "{\"succ\":0}";
  encode_demo(s, 46231);
}

  /*
		scr  待加密初始数据字符
  */
  
char* encode_demo(char* scr,  int timevalue)
{
		char* base_scr = base64_encrypt_text(scr,strlen(scr));
    //sprintf("%s\n", base_scr);
        uchar index = timevalue%256;			//	获取Keyindex
        int len = strlen(scr);
        char* cbuf = (char*)malloc(sizeof(char)*len);
        int i = 0;
        if(cbuf==NULL)
        {
          printf("cbuf is null\n");
          exit(0);
        }
        printf("Enctyptindex=%d,enctry_%d:%s,Keyactive:%d\n",index,len,scr,KeyMap[index]);
        printf("Get New Map:\n{");
        for(i=0 ; i<len; i++)					//	获取加密用的keymap
        {
          cbuf[i] = KeyMap[i%256]^KeyMap[index];
          printf("%d,",(uchar)cbuf[i]);
        }
        uchar checksum = 0;
        uchar* ss = scr;
        printf("\b};\nEnctry %s :\n{",ss);
        for(i=0; i<len; i++)					//	用获取到的keymap加密
        {
          
          checksum += ss[i];						//	校验和
          printf(">>%d,%d\n", ss[i], checksum);
          cbuf[i] = cbuf[i]^ss[i];
          printf("%d,",(uchar)cbuf[i]);
        }
        printf("\b};\n");
        char* base = base64_encrypt_text((char*)cbuf,len);		//	做一次base64
        printf("Base: %s",base);
        printf("Get :\n{\"MainKey\":\"%d\",\n\"Value\":%d,\n\"Data\":\"%s\"}\n",timevalue,checksum,base);
        free(cbuf);
        free(base);
}

char* decode_demo(char* decode_scr, int timevalue)
{
	int lenth = 0;
	char* base = base64_decrypt_text(decode_scr, strlen(decode_scr),&lenth);		//	base64转换
	uchar *buf = (uchar*)malloc(sizeof(uchar)*lenth); 
	memcpy(buf,base,lenth);
	free(base);
	printf("Get  %d encryptData:{",lenth);

	uchar Encryptkey = KeyMap[timevalue%256];							//	获取加密key
	uchar* sbuf = (uchar*)malloc(sizeof(uchar)*lenth);
	int i=0;
	for(i=0; i<lenth; i++)
	  printf("%d,",buf[i]);
	printf("\b}\nDecryptKey:%d\n",Encryptkey);
	for(i=0; i<lenth; i++)													//	转换加密用的keymap，并直接解密
	{
	  sbuf[i] = Encryptkey^KeyMap[i];
	  sbuf[i] ^= buf[i];
	}
	printf("Decrypt:\n%s\n",(char*)sbuf);
	free(buf);
	free(sbuf);
}