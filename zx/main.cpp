#include "reverse.h" 

//服务方法的实现
int Service::reversestr(char *iStr, char **oStr)
{
    if (NULL == iStr || NULL == oStr)
    {
       return this->error;
    }
    int strLen = strlen(iStr);
    *oStr = (char*)soap_malloc(this, strLen + 1);
    memset(*oStr, 0, strLen + 1);
    char *pOutBuf = *oStr;
    while (strLen-- > 0)
    {
       *(pOutBuf++) = *(iStr + strLen);
    }
    return this->error;
} 

//服务入口，这里是最基本的服务形式
int main()
{
    Service serv;
    serv.serve();
    int port = 800;  //服务端口，启用前先用netstat查看下该端口是否被占用
    if (serv.run(port))
    {
       serv.soap_stream_fault(std::cerr);
       exit(-1);
    }

    return 0;

}