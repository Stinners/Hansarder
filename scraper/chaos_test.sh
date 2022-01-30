# Get the correct addaptor name 
wifi=`iw dev | awk '$1=="Interface"{print $2}'`

# Slow down the internet 
sudo tc qdisc add dev $wifi root netem delay 1000ms

# run the tests 
time python main.py

# Reset the internet 
sudo tc qdisc del dev $wifi root netem
