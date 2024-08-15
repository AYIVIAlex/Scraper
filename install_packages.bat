@echo off
echo Installing Python packages...
python -m pip install --upgrade pip

pip install pyktok
pip install beautifulsoup4
pip install browser-cookie3
pip install numpy
pip install pandas
pip install requests
pip install streamlit
pip install TikTokApi

echo All packages installed successfully!
pause