clear
echo "******* The Onion installer ********"
echo ""
echo "=====> Installing tor bundle "
sudo apt-get install tor -y -qq
echo "=====> Installing The Onion "
sudo cp onion /usr/bin/onion
sudo chmod +x /usr/bin/onion
echo "=====> Done "
echo "=====> Open terminal and type 'onion' for usage "
