bind = "0.0.0.0:5000"
workers = 4
threads = 1
 # due to a bug in signal, threads = 1 is required, otherwise we get an error: ValueError: signal only works in main thread
timeout = 120