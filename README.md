# Interactive Discord Bot project
##### Travis Montgomery (aba9jj) and Joe Thompson (zwt4pb)

DS2002: DS Systems Final Project pt2

The core of the Discord Bot's Charlottesville-specific knowledge originates from [Charlottesville Open Data](https://opendata.charlottesville.org). The 'data_handling' directory of this repository handles the data ingestion of 6 different sources from the above open data site. Crime and road/sidewalk closure data is retrieved daily using Python's `schedule` module using an API response. Other relevant Charlottesville data, including information regarding the trails, parks, bus stops, and bike racks, is more static and thus loaded through csv files. 


The Discord Bot provided is trained to query the MySQL database based on user commands. Commands `!trails`, `!parks`, `!bike`, `!bus`, and `!crime` signal to the bot to query the respective MySQL tables for appropriate information to respond with. These commands allow users to get specific, accurate, real-time Charlottesville data presented in an informing manner. The Bot also recognizes commands `help` (provide possible commands) and `quit` (quit the session).


To utilize the Charlottesville Bot, a user must first have Discord downloaded. The test server used to host this bot can be joined at [this link](https://discord.gg/tU9qUCXe). (Note: Discord server inite links expire every 7 days, so it's likely the provided link is expired if you attempt to join.) Alternatively, this repository can be cloned to your local machine and used to instantiate the Charlottesville Discord Bot on your own created Discord server. Visit [Discord Developers](https://discord.com/developers/docs/intro) for more information on creating your Bot and connecting it to a server to be able to utilize this Python repository for Bot functionality.


<p align="center">
  <img src="/bot_icon.png" />
</p>
