# printerNfc

for mifare classic we have to authenticate every block we want to write using key A mifare classic 1k/4k
FF 88 00 04 60 00h # for block 04
FF 88 00 05 60 00h # for block 05
FF 88 00 06 60 00h # for block 06
for some cards we have to authenticate some blocks using Key B


Update the binary block 04h of MIFARE Classic 1K/4K with Data {00 01 .. 0Fh} e.g. smart cards and keycahins
APDU = {FF D6 00 04 10 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0Fh} 
 Update the binary block 04h of MIFARE  Ultralight with Data {00 01 02 03} e.g. ntag
APDU = {FF D6 00 04 04 00 01 02 03h} 

sudo apt-get install pcscd git python-setuptools swig gcc libpcsclite-dev python-dev
sudo echo "install nfc /bin/false" >> /etc/modprobe.d/blacklist.conf
sudo echo "install pn533 /bin/false" >> /etc/modprobe.d/blacklist.conf
cd ~
git clone https://github.com/LudovicRousseau/pyscard.git
cd pyscard
sudo python setup.py build_ext install
reboot
