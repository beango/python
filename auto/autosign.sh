python3 /root/CC签到.py > /root/log.txt 
python3 /root/zdm.py >> /root/log.txt 
python3 /root/TS签到.py >> /root/log.txt 
 
sendEmail -f 6588617@qq.com -t 6588617@qq.com -s pop.qq.com \ 
 -u "自动签到提醒" -o message-content-type=text -xu 6588617@qq.com \ 
-xp oarfdmbxsxfhbjia -o message-charset=utf8 message-file=/root/log.txt
