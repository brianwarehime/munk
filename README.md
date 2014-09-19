### Munk
##### Visualize Splunk Architecture in Maltego
-------------------------------------------------

Munk is a Maltego transform pack for use with your Splunk deployment. Using the Munk machines, you can map out all of your Indexers, Indexes, Sourcetypes and Hosts with one click. You can also map out your full Splunk Deployment Server configuration, to include, Apps, ServerClasses and Hosts. With Munk, you can also perform a search on a specific entity right from Maltego (works on Indexes, Sourcetypes and Hosts).

### Installation

```
$ cd /opt
$ git clone git@github.com:brianwarehime/munk.git
In Maltego, click on Maltego icon > Import > Import Configuration
Select munk.mtz
```

Before running the transforms/machines, you will need to edit the configuration file in munk/local called munk.conf. You will need to set your Splunk username and password, as well as the authentication type. If you are using the free license with Splunk, set the credentials to anything you would like and set authentication type to 0, otherwise, set it 1 and enter valid credentials.

*Note: When entering your password in the conf file, you will need to escape any special characters in your password. For example, l33t!pass would need to be l33t\!pass

In munk.conf there is also a setting for timeframe. This will change your searches to include earliest=”timerange” where “timerange” is a Splunk formatted timerange. For example, to look back one day at the beginning of the day, it would be -1d@d, or to go back just a few hours, -5h. Generally, the narrower the timerange, the quicker your architecture will be displayed in Maltego.

Also in munk.conf there is a setting for status. If this value is set to 1, the box that Maltego is running on will attempt to ping the entity you are displaying, such as the host, indexer, or deployment server.

Lastly, there are two different settings for the various ports you configured in Splunk, splunkweb and the management port. Change these to reflect your environment.

### Using Munk

After you have edited the configuration file and imported the .mtz file, you are ready to use Munk. The first thing you should do, is drag the “Search Head” entity from the Munk entities on the left-hand side to the work area. You can change the name of the Search Head, however, it is not needed, since Munk uses the hostname provided in the configuration file to run the transforms.

Next, right-click on the Search Head you just created, and either select “Run Transform” or “Run Machine”. “Run Transform” will allow you to go one layer deep at a time into your deployment, whereas “Run Machine” will run a series of transforms for you all at once, and is definitely the easier of the two. Since there is a limitation of 12 entities returned in the Community Edition of Maltego, the Munk machine will run several iterations 15 seconds apart to keep populating entities that aren’t displayed yet. This will keep running until you press the stop button in the top right corner under “Machines”. If you have a large environment, it should complete your architecture in a few iterations.

Here is a demo environment snapshot to illustrate what Munk does. This screenshot shows a small deployment, in larger environments, this would obviiously be a lot larger. Below you can see the Splunk Search Head at the top, branching off of it is the Deployment Server (splunk-ds), along with the Indexer (Splunk). Below them are the indexes (main, firewall, and vuln), with their sourcetypes (brah, firewall, nessus). Lastly, you can see the different hosts that populate those sourcetypes (securityonion, demo, nessus-1, nessus-2).

<p align="center">
<img src="https://camo.githubusercontent.com/3f3e7bf6fe3c1a835009941a4af97a5fd9496cb9/687474703a2f2f692e696d6775722e636f6d2f326f48375a41792e706e67"></p>

Along with mapping our your Splunk toplogy, you can map our your Deployment Server configuration. This will show you the different apps you are currently deploying to clients, as well as the Server Classes, and the hosts that are contained in those Server Classes. Below is a screenshot of the full environment, along with DS configuration.

<p align="center">
<img src="https://camo.githubusercontent.com/2d059045c12953a112a2990014d3856bb08abf53/687474703a2f2f692e696d6775722e636f6d2f6b346f52725a4e2e706e67"></p>

With Munk, you also have the ability to open a Splunk search starting with the entity you clicked on. For example, if you were to right-click on an Index and selected “Run Transform”, then “Splunk Entity Search”, it would open your default browser to a Splunk page with “index=”selected index”. This capability extends to host, sourcetype and index for now.

