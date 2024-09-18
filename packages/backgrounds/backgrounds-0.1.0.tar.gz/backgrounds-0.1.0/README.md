# backgrounds

Principal component analysis application to stochastic gravitational wave detection.

## Dependencies

Backgrounds requires LISA Constants and LISA GW Response from the LISA Simulation suite, which can be installed as
```
pip install git+https://@gitlab.in2p3.fr/lisa-simulation/constants.git@latest
pip install git+https://gitlab.in2p3.fr/lisa-simulation/gw-response.git@latest
```
To run the scripts in the tests folder it is recommanded to install the packages listed in the requirements:
```
pip install --no-cache-dir -r requirements.txt
```

## Installation

Please clone the repository and do a manual installation:
```
git clone git@gitlab.in2p3.fr:qbaghi/backgrounds.git
cd backgrounds
python3 setup.py install
```