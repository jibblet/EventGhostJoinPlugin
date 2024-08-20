# EventGhostJoinPlugin
an EventGhost plugin that exposes the Join for Android API, removing difficult set up

Simply copy the entire "JoinforAndroidAPI" directory into your EventGhost plugin directory, typically in:

C:\Program Files (x86)\EventGhost\plugins


From there, restart EventGhost and add the Join for Android API from the General Plugins menu after
clicking on the puzzle piece at the top. Then add your API key and devices+device IDs. 

Currently, only "Send Notification" is available. 

I am working on adding additional functionality, the most important being the ability to send to multiple
devices at once. Currently, multi-device messaging does not work as well as it should. 




UPDATE 20240820
#################

Thank you to /u/Lord_Sithek for suggesting system clipboard functionality. I'm pleased to announce that feature
is now available to you as an Action, no configuration required. Simply click Add Action from the toolbar, Join
for Android API > Send Clipboard. 

A menu immediately pops up and lets you select from all available devices. You can test fire it as well from the 
same menu. 

Oddly, sending the system clipboard to multiple devices is highly effective and works great, especially in 
comparison to sending a notification to multiple devices at once. This is one of the major bugs I plan on 
fixing as soon as possible. 

One point of clarity around how the send clipboard action works.

What it does is send the specified device(s) a Join push notification. The title of this notification is 
"clipboard" and the text of this notification is <contents of windows clipboard>. For a notification like
ours that is sent with both text and title, Join creates a popup notification on the device(s) that displays
the contents of the clipboard as the text, along with buttons 'Copy' and 'Share'.

However, you need to actually click the 'Copy' button in order to transfer the clipboard info 
you just sent. If you would like to have your phone's clipboard overwritten in the background
without having to manually interact, you'll need to set up a profile that listens for the command
'clipboard' (the title of the notification) and sets the text of the notification to your 
device's clipboard when it detects it.