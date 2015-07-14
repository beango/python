package com.beango.util;

import java.io.File; 
import java.io.IOException; 
import java.io.InputStream; 
import java.net.URLEncoder; 
import java.nio.charset.Charset; 
import java.util.ArrayList; 
import java.util.HashMap; 
import java.util.Iterator; 
import java.util.List; 
import java.util.Map; 
 
import javax.net.ssl.SSLHandshakeException; 
 
import org.apache.http.Header; 
import org.apache.http.HttpEntityEnclosingRequest; 
import org.apache.http.HttpHost; 
import org.apache.http.HttpRequest; 
import org.apache.http.HttpResponse; 
import org.apache.http.NameValuePair; 
import org.apache.http.NoHttpResponseException; 
import org.apache.http.client.ClientProtocolException; 
import org.apache.http.client.CookieStore; 
import org.apache.http.client.HttpRequestRetryHandler; 
import org.apache.http.client.entity.UrlEncodedFormEntity; 
import org.apache.http.client.methods.HttpGet; 
import org.apache.http.client.methods.HttpPost; 
import org.apache.http.client.params.HttpClientParams; 
import org.apache.http.conn.params.ConnRouteParams; 
import org.apache.http.impl.client.DefaultHttpClient; 
import org.apache.http.params.BasicHttpParams; 
import org.apache.http.params.HttpConnectionParams; 
import org.apache.http.params.HttpParams; 
import org.apache.http.protocol.ExecutionContext; 
import org.apache.http.protocol.HTTP; 
import org.apache.http.protocol.HttpContext; 
import org.apache.http.util.EntityUtils; 
 
import android.app.Activity; 
import android.content.Context; 
import android.widget.Toast; 

public class HttpClients {
	/** 执行downfile后，得到下载文件的大小 */ 
    private long contentLength; 
    /** 返回连接失败信息 **/ 
    private String strResult = "服务器无法连接，请检查网络"; 
 
    /** http 请求头参数 **/ 
    private HttpParams httpParams; 
    /** httpClient 对象 **/ 
    private DefaultHttpClient httpClient; 
 
 
    /** 得到上下文 **/ 
    //private Context context; 
    //private Activity activity = null; 
 
    public HttpClients(Activity act) { 
        //this.context = act.getBaseContext(); 
        //this.activity = act; 
        getHttpClient(); 
    } 
 
    /**
     * 提供GET形式的访问网络请求 doGet 参数示例： Map params=new HashMap();
     * params.put("usename","helijun"); params.put("password","123456");
     * httpClient.doGet(url,params)；
     * 
     * @param url
     *            请求地址
     * @param params
     *            请求参数
     * @return 返回 String jsonResult;
     * 
     * **/ 
    @SuppressWarnings("unchecked") 
    public String doGet(String url, Map params) { 
        /** 建立HTTPGet对象 **/ 
        String paramStr = ""; 
        if (params == null) 
            params = new HashMap(); 
        /** 迭代请求参数集合 **/ 
        Iterator iter = params.entrySet().iterator(); 
        while (iter.hasNext()) { 
            Map.Entry entry = (Map.Entry) iter.next(); 
            Object key = entry.getKey(); 
            String val = nullToString(entry.getValue()); 
            paramStr += paramStr = "&" + key + "=" + URLEncoder.encode(val); 
        } 
        if (!paramStr.equals("")) { 
            paramStr = paramStr.replaceFirst("&", "?"); 
            url += paramStr; 
        } 
        return doGet(url); 
    } 
 
    /**
     * 提供GET形式的访问网络请求 doGet 参数示例： Map params=new HashMap();
     * params.put("usename","gongshuanglin"); params.put("password","123456");
     * httpClient.doGet(url,params)；
     * 
     * @param url
     *            请求地址
     * @param params
     *            请求参数
     * @return 返回 String jsonResult;
     * 
     */ 
    public String doGet(String url, List<NameValuePair> params) { 
        /** 建立HTTPGet对象 **/ 
        String paramStr = ""; 
        if (params == null) 
            params = new ArrayList<NameValuePair>(); 
        /** 迭代请求参数集合 **/ 
 
        for (NameValuePair obj : params) { 
            paramStr += paramStr = "&" + obj.getName() + "=" 
                    + URLEncoder.encode(obj.getValue()); 
        } 
        if (!paramStr.equals("")) { 
            paramStr = paramStr.replaceFirst("&", "?"); 
            url += paramStr; 
        } 
        return doGet(url); 
    } 
 
    /**
     * 提供GET形式的访问网络请求 doGet 参数示例：
     * 
     * @param url
     *            请求地址
     * @return 返回 String jsonResult;
     * 
     */ 
    public String doGet(String url) { 
        /** 创建HttpGet对象 **/ 
        HttpGet httpRequest = new HttpGet(url); 
        //httpRequest.setHeaders(this.getHeader()); 
        try { 
            /** 保持会话Session **/ 
            /** 设置Cookie **/ 
            //MyHttpCookies li = new MyHttpCookies(context); 
            //CookieStore cs = li.getuCookie(); 
            /** 第一次请求App保存的Cookie为空，所以什么也不做，只有当APP的Cookie不为空的时。把请请求的Cooke放进去 **/ 
//            if (cs != null) { 
//                httpClient.setCookieStore(li.getuCookie()); 
//            } 
 
            /** 保持会话Session end **/ 
 
            /* 发送请求并等待响应 */ 
            HttpResponse httpResponse = httpClient.execute(httpRequest); 
            /* 若状态码为200 ok */ 
            if (httpResponse.getStatusLine().getStatusCode() == 200) { 
                /* 读返回数据 */ 
                strResult = EntityUtils.toString(httpResponse.getEntity()); 
 
                /** 执行成功之后得到 **/ 
                /** 成功之后把返回成功的Cookis保存APP中 **/ 
                // 请求成功之后，每次都设置Cookis。保证每次请求都是最新的Cookis 
                //li.setuCookie(httpClient.getCookieStore()); 
 
            } else { 
                strResult = "Error Response: " 
                        + httpResponse.getStatusLine().toString(); 
            } 
        } catch (ClientProtocolException e) { 
            strResult = nullToString(e.getMessage()); 
            e.printStackTrace(); 
        } catch (IOException e) { 
            strResult = nullToString(e.getMessage()); 
            e.printStackTrace(); 
        } catch (Exception e) { 
            strResult = nullToString(e.getMessage()); 
            e.printStackTrace(); 
        } finally { 
            httpRequest.abort(); 
            this.shutDownClient(); 
        } 
        return strResult; 
    } 
 
    /**
     * 提供Post形式的访问网络请求 Post 参数示例： doPost 参数示例 List<NameValuePair> paramlist =
     * new ArrayList<NameValuePair>(); paramlist(new BasicNameValuePair("email",
     * "xxx@123.com")); paramlist(new BasicNameValuePair("address", "123abc"));
     * httpClient.doPost(url,paramlist);
     * 
     * @param url
     *            请求地址
     * @param params
     *            请求参数
     * @return 返回 String jsonResult;
     * **/ 
 
    public String doPost(String url, List<NameValuePair> params) { 
        /* 建立HTTPPost对象 */ 
 
        HttpPost httpRequest = new HttpPost(url); 
        // 设置请求Header信息、 
        //httpRequest.setHeaders(this.getHeader()); 
        try { 
            /** 添加请求参数到请求对象 */ 
//          boolean upFileFlag = false;// 是否有文件上传 
//          MultipartEntity mpEntity = new MultipartEntity( 
//                  HttpMultipartMode.BROWSER_COMPATIBLE); 
//          for (NameValuePair param : params) { 
//              ContentBody contentBody = null; 
//              File file = new File(param.getValue()); 
//              if (file.isFile()) { 
//                  contentBody = new FileBody(file); 
//                  upFileFlag = true; 
//              } else { 
//                  contentBody = new StringBody(param.getValue(), Charset 
//                          .forName(HTTP.UTF_8)); 
//              } 
//              mpEntity.addPart(param.getName(), contentBody); 
//          } 
// 
//          if (upFileFlag == true) {// 文件 上传 
//              httpRequest.setEntity(mpEntity); 
//          } else { 
                /** 添加请求参数到请求对象 */ 
                httpRequest.setEntity(new UrlEncodedFormEntity(params, 
                        HTTP.UTF_8)); 
//          } 
 
            /** 保持会话Session **/ 
            /** 设置Cookie **/ 
                //MyHttpCookies li = new MyHttpCookies(context); 
            //CookieStore cs = li.getuCookie(); 
            /** 第一次请求App保存的Cookie为空，所以什么也不做，只有当APP的Cookie不为空的时。把请请求的Cooke放进去 **/ 
            //if (cs != null) { 
            //    httpClient.setCookieStore(li.getuCookie()); 
            //} 
 
            /** 保持会话Session end **/ 
 
            /** 发送请求并等待响应 */ 
 
            HttpResponse httpResponse = httpClient.execute(httpRequest); 
             
            /** 若状态码为200 ok */ 
            if (httpResponse.getStatusLine().getStatusCode() == 200) { 
                /* 读返回数据 */ 
                strResult = EntityUtils.toString(httpResponse.getEntity()); 
 
                /** 执行成功之后得到 **/ 
                /** 成功之后把返回成功的Cookis保存APP中 **/ 
                // 请求成功之后，每次都设置Cookis。保证每次请求都是最新的Cookis 
                //li.setuCookie(httpClient.getCookieStore()); 
 
                /** 设置Cookie end **/ 
            } else { 
                strResult = "Error Response: " 
                        + httpResponse.getStatusLine().toString(); 
            } 
        } catch (ClientProtocolException e) { 
            strResult = ""; 
//          strResult = e.getMessage().toString(); 
            e.printStackTrace(); 
        } catch (IOException e) { 
            strResult = ""; 
//          strResult = e.getMessage().toString(); 
            e.printStackTrace(); 
        } catch (Exception e) { 
            strResult = ""; 
//          strResult = e.getMessage().toString(); 
            e.printStackTrace(); 
        } finally { 
            httpRequest.abort(); 
            this.shutDownClient(); 
        } 
        return strResult; 
    } 
 
    /** 得到 apache http HttpClient对象 **/ 
    public DefaultHttpClient getHttpClient() { 
 
        /** 创建 HttpParams 以用来设置 HTTP 参数 **/ 
 
        httpParams = new BasicHttpParams(); 
 
        /** 设置连接超时和 Socket 超时，以及 Socket 缓存大小 **/ 
 
        HttpConnectionParams.setConnectionTimeout(httpParams, 20 * 1000); 
 
        HttpConnectionParams.setSoTimeout(httpParams, 20 * 1000); 
 
        HttpConnectionParams.setSocketBufferSize(httpParams, 8192); 
 
        HttpClientParams.setRedirecting(httpParams, true); 
 
        /**
         * 创建一个 HttpClient 实例 //增加自动选择网络，自适应cmwap、CMNET、wifi或3G
         */ 
        //MyHttpCookies li = new MyHttpCookies(context); 
        //String proxyStr = li.getHttpProxyStr(); 
//        if (proxyStr != null && proxyStr.trim().length() > 0) { 
//            HttpHost proxy = new HttpHost(proxyStr, 80); 
//            httpClient.getParams().setParameter(ConnRouteParams.DEFAULT_PROXY, 
//                    proxy); 
//        } 
        /** 注意 HttpClient httpClient = new HttpClient(); 是Commons HttpClient **/ 
 
        httpClient = new DefaultHttpClient(httpParams); 
        httpClient.setHttpRequestRetryHandler(requestRetryHandler); 
         
        return httpClient; 
 
    } 
 
    /** 得到设备信息、系统版本、驱动类型 **/ 
//    private Header[] getHeader() { 
//        /** 请求头信息 end **/ 
//        MyHttpCookies li = new MyHttpCookies(context); 
//        return li.getHttpHeader(); 
//    } 
 
    /** 销毁HTTPCLient **/ 
    public void shutDownClient() { 
        httpClient.getConnectionManager().shutdown(); 
    } 
 
//  /** 
//   * 提供GET形式的访问网络请求 doGet 参数示例： 
//   *  
//   * @param url 
//   *            请求地址 
//   * @return 返回 String jsonResult; 
//   *  
//   */ 
//  public InputStream doDownFile(String url) { 
//      /** 创建HttpGet对象 **/ 
//      HttpGet httpRequest = new HttpGet(url); 
//      httpRequest.setHeaders(this.getHeader()); 
//      try { 
//          /** 保持会话Session **/ 
//          /** 设置Cookie **/ 
//          MyHttpCookies li = new MyHttpCookies(context); 
//          CookieStore cs = li.getuCookie(); 
//          /** 第一次请求App保存的Cookie为空，所以什么也不做，只有当APP的Cookie不为空的时。把请请求的Cooke放进去 **/ 
//          if (cs != null) { 
//              httpClient.setCookieStore(li.getuCookie()); 
//          } 
//          /** 保持会话Session end **/ 
//          /* 发送请求并等待响应 */ 
//          HttpResponse httpResponse = httpClient.execute(httpRequest); 
//          /* 若状态码为200 ok */ 
//          if (httpResponse.getStatusLine().getStatusCode() == 200) { 
//              /** 执行成功之后得到 **/ 
//              /** 成功之后把返回成功的Cookis保存APP中 **/ 
//              // 请求成功之后，每次都设置Cookis。保证每次请求都是最新的Cookis 
//              li.setuCookie(httpClient.getCookieStore()); 
//              this.contentLength = httpResponse.getEntity() 
//                      .getContentLength(); 
//              /* 读返回数据 */ 
//              return httpResponse.getEntity().getContent(); 
//          } else { 
//              strResult = "Error Response: " 
//                      + httpResponse.getStatusLine().toString(); 
//          } 
//      } catch (ClientProtocolException e) { 
//          strResult = e.getMessage().toString(); 
//          e.printStackTrace(); 
//      } catch (IOException e) { 
//          strResult = e.getMessage().toString(); 
//          e.printStackTrace(); 
//      } catch (Exception e) { 
//          strResult = e.getMessage().toString(); 
//          e.printStackTrace(); 
//      } finally { 
//          // httpRequest.abort(); 
//          // this.shutDownClient(); 
//      } 
//      this.contentLength = 0; 
//      return null; 
//  } 
 
    /**
     * 异常自动恢复处理, 使用HttpRequestRetryHandler接口实现请求的异常恢复
     */ 
    private static HttpRequestRetryHandler requestRetryHandler = new HttpRequestRetryHandler() { 
        // 自定义的恢复策略 
        public boolean retryRequest(IOException exception, int executionCount, 
                HttpContext context) { 
            // 设置恢复策略，在发生异常时候将自动重试N次 
            if (executionCount >= 3) { 
                // 如果超过最大重试次数，那么就不要继续了 
                return false; 
            } 
            if (exception instanceof NoHttpResponseException) { 
                // 如果服务器丢掉了连接，那么就重试 
                return true; 
            } 
            if (exception instanceof SSLHandshakeException) { 
                // 不要重试SSL握手异常 
                return false; 
            } 
            HttpRequest request = (HttpRequest) context 
                    .getAttribute(ExecutionContext.HTTP_REQUEST); 
            boolean idempotent = (request instanceof HttpEntityEnclosingRequest); 
            if (!idempotent) { 
                // 如果请求被认为是幂等的，那么就重试 
                return true; 
            } 
            return false; 
        } 
    }; 
 
    public long getContentLength() { 
        return contentLength; 
    } 
 
    /**
     * 假如obj对象 是null返回""
     * @param obj
     * @return
     */ 
    public static String nullToString(Object obj){ 
        if(obj==null){ 
            return ""; 
        } 
        return obj.toString(); 
    } 
 
}
