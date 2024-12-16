Отдача статического документа напрямую через nginx:

```shell
ab -n 1000 -c 10 http://127.0.0.1/static/sample.html
```

```txt
Server Software:        nginx/1.27.3
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /static/sample.html
Document Length:        4699 bytes

Concurrency Level:      10
Time taken for tests:   0.064 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      4971000 bytes
HTML transferred:       4699000 bytes
Requests per second:    15630.62 [#/sec] (mean)
Time per request:       0.640 [ms] (mean)
Time per request:       0.064 [ms] (mean, across all concurrent requests)
Transfer rate:          75878.71 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.2      0       1
Processing:     0    0   0.2      0       3
Waiting:        0    0   0.2      0       3
Total:          0    1   0.4      0       4
ERROR: The median and mean for the total time are more than twice the standard
       deviation apart. These results are NOT reliable.

Percentage of the requests served within a certain time (ms)
  50%      0
  66%      0
  75%      1
  80%      1
  90%      1
  95%      2
  98%      2
  99%      2
 100%      4 (longest request)
```

Отдача статического документа напрямую через gunicorn:

```shell
ab -n 1000 -c 10 http://127.0.0.1:8000/static/sample.html
```

```txt
Server Software:        gunicorn
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /static/sample.html
Document Length:        4699 bytes

Concurrency Level:      10
Time taken for tests:   0.726 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      5065000 bytes
HTML transferred:       4699000 bytes
Requests per second:    1378.29 [#/sec] (mean)
Time per request:       7.255 [ms] (mean)
Time per request:       0.726 [ms] (mean, across all concurrent requests)
Transfer rate:          6817.41 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       1
Processing:     3    7   1.1      7      30
Waiting:        2    7   1.0      7      28
Total:          4    7   1.1      7      30

Percentage of the requests served within a certain time (ms)
  50%      7
  66%      7
  75%      7
  80%      7
  90%      7
  95%      7
  98%      8
  99%     13
 100%     30 (longest request)
```

Отдача динамического документа напрямую через gunicorn:

```shell
ab -n 1000 -c 10 http://127.0.0.1:8000/settings
```

```txt
Server Software:        gunicorn
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /settings
Document Length:        4704 bytes

Concurrency Level:      10
Time taken for tests:   3.914 seconds
Complete requests:      1000
Failed requests:        0
Non-2xx responses:      1000
Total transferred:      4993000 bytes
HTML transferred:       4704000 bytes
Requests per second:    255.49 [#/sec] (mean)
Time per request:       39.141 [ms] (mean)
Time per request:       3.914 [ms] (mean, across all concurrent requests)
Transfer rate:          1245.75 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       4
Processing:     7   39   4.6     38      70
Waiting:        7   38   4.6     38      70
Total:          7   39   4.6     38      71

Percentage of the requests served within a certain time (ms)
  50%     38
  66%     38
  75%     38
  80%     39
  90%     40
  95%     41
  98%     57
  99%     68
 100%     71 (longest request)

```

Отдача динамического документа через проксирование запроса с nginx на gunicorn:

```shell
ab -n 1000 -c 10 http://127.0.0.1/settings
```

```txt
Server Software:        nginx/1.27.3
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /settings
Document Length:        4699 bytes

Concurrency Level:      10
Time taken for tests:   3.846 seconds
Complete requests:      1000
Failed requests:        0
Non-2xx responses:      1000
Total transferred:      4992000 bytes
HTML transferred:       4699000 bytes
Requests per second:    259.99 [#/sec] (mean)
Time per request:       38.463 [ms] (mean)
Time per request:       3.846 [ms] (mean, across all concurrent requests)
Transfer rate:          1267.44 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       1
Processing:     6   38   2.2     38      46
Waiting:        6   38   2.2     38      46
Total:          7   38   2.1     38      46

Percentage of the requests served within a certain time (ms)
  50%     38
  66%     38
  75%     38
  80%     38
  90%     39
  95%     40
  98%     43
  99%     45
 100%     46 (longest request)
```

Отдача динамического документа через проксирование запроса с nginx на gunicorn, при кэшировние ответа на nginx (proxy cache):

```shell
ab -n 1000 -c 10 http://127.0.0.1/
```

```txt
Server Software:        nginx/1.27.3
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /settings
Document Length:        4699 bytes

Concurrency Level:      10
Time taken for tests:   0.067 seconds
Complete requests:      1000
Failed requests:        0
Non-2xx responses:      1000
Total transferred:      4992000 bytes
HTML transferred:       4699000 bytes
Requests per second:    15024.94 [#/sec] (mean)
Time per request:       0.666 [ms] (mean)
Time per request:       0.067 [ms] (mean, across all concurrent requests)
Transfer rate:          73246.59 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.2      0       1
Processing:     0    0   0.4      0      11
Waiting:        0    0   0.3      0       9
Total:          0    1   0.5      0      11
ERROR: The median and mean for the total time are more than twice the standard
       deviation apart. These results are NOT reliable.

Percentage of the requests served within a certain time (ms)
  50%      0
  66%      0
  75%      0
  80%      1
  90%      1
  95%      1
  98%      1
  99%      2
 100%     11 (longest request)
```

Насколько быстрее отдается статика по сравнению с WSGI? nginx раздает статику быстрее, чем wsgi в 11.3 раза

Во сколько раз ускоряет работу proxy_cache? proxy_cache ускоряет раздачу динамики в 50 раз
