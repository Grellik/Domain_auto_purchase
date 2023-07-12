Made by Danilov Gennady

How to use config file:
Add domains separated by comma.

Account ID is found in DNSimple account settings, in Automation
You can get Api Token there as well

Contact ID is found by calling "https://api.dnsimple.com/v2/*your account ID*/contacts" with same auth parameters
I put in an additional script called check_contacts.py just for that.

Time_start and Time_end is the time during which script will attempt to register any domains. It uses same time as your PC!

Timer, will shut off script automatically after it reaches 0. It is set in minutes. If you put it on 0, there will be no timer.

Retry_rate is intervals of time between registration attempts.

Test - testmode, script will attempt to to its job in sandbox.dnsimple. This includes check_contacts.py.
In this mode no money will be charged, but you need to create separate account to use it. More info : https://developer.dnsimple.com/sandbox/


How to run this script?
well, it should work just fine by simply running it from the folder it is in. If it does not work, there are problems with Python or its PATH on your PC,
please contact me in that case. Or try running it from any Python compatible IDE, like VSC.

