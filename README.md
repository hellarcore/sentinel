<h1 align="center">Hellar Core<a href="https://github.com/hellarcore/sentinel" target="_blank"> Sentinel</a> 
<h3 align="center">Sentinel is an all-powerful toolset for Hellarpay</h3>


Sentinel is an autonomous agent for persisting, processing and automating Hellar Core v.1.0.2 governance objects and tasks, and for expanded functions in upcoming releases.
Sentinel is implemented as a Python application that binds to a local version 1.0.2 hellard instance on each Hellar Core V1.0.0 Masternode.

<h3 align="center">This guide covers installing Sentinel onto an existing v.1.0.2 Masternode in Ubuntu 18.04</h3>

Alternatively to the guide on the Hellar website, you can also follow the simple step-by-step guide below. Before you proceed it is advisable to restart your masternode with -reindex to make sure you start off the steps fresh and fully synced - it will save you time later on in the guide as well.

```./hellar-cli stop ``` // Adjust according to your root Hellar Core directory path

```cd .hellar```

delete all files excluding "hellar.conf" and "wallet.dat"

```cd ..```

```./hellard --daemon --reindex```

<h3 align="center">Installation</h3>

<h3 align="center">1. Install Prerequisites</h3>
Make sure Python version 2.7.x or above is installed:

```python --version```

Update system packages and ensure virtualenv is installed:

```sudo apt-get update```

```sudo apt-get -y install python-virtualenv```

Make sure the local Hellar Core daemon running is at least version 1.0.2

```./hellar-cli getinfo | grep version```

<h3 align="center">------------------------------------------------------</h3>
<h3 align="center">2. Install Sentinels</h3>

Clone the Sentinel repo and install Python dependencies.

```git clone https://github.com/hellarpay/sentinel/sentinel.git && cd sentinel```

```virtualenv ./venv```

```./venv/bin/pip install -r requirements.txt```

<h3 align="center">------------------------------------------------------</h3>
<h3 align="center">3. Configure & Test Your Configuration</h3>

Open sentinel.conf - Run the following command in linux:

```nano sentinel.conf```

Uncomment the #hellar_conf line, at the top of the file, then adjust the path to your Masternode’s hellar.conf. Save the file then close it.

//hellar_conf=/path/to/hellar.conf

Now run:
```venv/bin/python bin/sentinel.py```
You should see: “hellard not synced with network! Awaiting full sync before running Sentinel.” This is exactly what we want to see at this stage.

If the wallet has been resynched alreaedy, you will see no output which is what you want to see and it means you can skip the next sync step.

<h3 align="center">------------------------------------------------------</h3>
4. Check That Your Hellarpay Wallet is Synced
# Go back into your root Hellar directory, then check the status of your sync:

```cd ..```

```./hellar-cli mnsync status```
This is what you’re waiting to see:

AssetId 999, all trues, one false, and a FINISHED. Keep issuing ./hellar-cli mnsync status until it looks like this:

```{
"AssetID": 999,
"AssetName": "MASTERNODE_SYNC_FINISHED",
"AssetStartTime": 1555922063,
"Attempt": 0,
"IsBlockchainSynced": true,
"IsMasternodeListSynced": true,
"IsWinnersListSynced": true,
"IsSynced": true,
"IsFailed": false
}```

At this point, your remote masternode is synchronized and chatting with the network but is not accepted as a masternode because it hasn’t been introduced to the network by your collateral.

<h3 align="center">------------------------------------------------------</h3>
5. Start Your Masternode
Go back to your local wallet, open the debug console, and run these commands to start your masternode (LABEL is the name you used for your MN in the masternode.conf):

walletpassphrase <YOURPASSPHRASE> 120 (only if you have a wallet password)
masternode start-alias <LABEL>

<h3 align="center">------------------------------------------------------</h3>
6. Test Your Sentinel
# You’re needed back in Sentinel directory:

```cd sentinel```

Run:
```venv/bin/python bin/sentinel.py```
# It should return no output if everything is working correctly. This is how you know it’s working, and your masternode and sentinel setup is properly configured.
<h3 align="center">------------------------------------------------------</h3>
7. Create Your Sentinel Crontab Entry
# Run:

```crontab -e```
#Add the following line below to the end of the file:

```* * * * * cd /USERNAME/sentinel && ./venv/bin/python bin/sentinel.py 2>&1 >> sentinel-cron.log```
# Make sure you:

# Change USERNAME to your username (VPS is /root/sentinel).
# Hit enter to create another line at the end after this line, or the file will not work.
# Save and exit.

<h3 align="center">------------------------------------------------------</h3>
8. All Done On Sentinel. Finally Check Your Masternode
# Go back into your Hellar Core root directory:

```cd ..```

Run:
```./hellar-cli masternode debug```
You should see the message “Masternode successfully started.”. If you have followed all the steps outlined in the guide accurately and achieved this result - this is it, you've made it. Congratulations!

<h3 align="center">------------------------------------------------------</h3>
Troubleshooting
To view debug output, set the SENTINEL_DEBUG environment variable to anything non-zero, then run the script manually:

```SENTINEL_DEBUG=1 ./venv/bin/python bin/sentinel.py```

