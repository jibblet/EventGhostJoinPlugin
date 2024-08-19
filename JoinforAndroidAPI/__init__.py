import eg
import urllib
import requests
import wx


##TODO##
# add device id validation on addition and edit of devices
# add support for sending to multiple devices
# add in whatsapp functionality?
# add in chatgpt/gemini functionality?


eg.RegisterPlugin(
    name=u"Join for Android API",
    author=u"jconic.com",
    version=u"0.2",
    kind=u"other",
    description=u"This plugin exposes the Join for Android API to EventGhost.",
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABEAAAARCAYAAAA7bUf6AAAAAXNSR0IArs4c6QAAAARnQU1BAAC"
        "xjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAJDSURBVDhPtZNLaBNRFIb/uTOTSdMqMdBEQp"
        "KFEUVMFyJSNyUg1GQnahUKFUsXwZ0bEaHFKDa6dWEWgi4UxE2p+wpCFVEKYoOaUh9FrBqqTeojj"
        "2Yy917vPIgxRBTBj7lz59z/P4eZwxkJHXANZYYIkbNEIgYIpqq3T590pI4QZ2+BS+K6tT+R9A8m"
        "EkFmsFFH+C0KUldV1D/KWPFxRNwMi+c444raGwhAVAOltMfyvFsnqJUoZs8bTm4TST00WYUkqfr"
        "guOKc/RHphKjfgpno2rsvKQPj9kmLnmUZfDJ6wTkX7wRc0FK20IYidKlhUECUMTn2+qyVYCYGA1"
        "4UVz/YRcTCVtvTjtXY3KPZ71Yk+Foq4ltpVawiGKfQpLpdoAX1cKahHb205j5ycdiMiSyT7dSo7"
        "bFUAWNMLC4KcIx03UTKP4106Jqj2oyOjSkDA3GvsFwxY1Ivdy/rn+kbSxUwztC3LQq9WsaN8gguv"
        "4rjzOIw9Pq64xBfTmSEwiHzUTNvRNEqXxSf0nSYb/F04aXolmo2BvD4ISsyxPA5DqBQKCD//AUns"
        "jJlxqInXA319Tcdbk+Ptbo3eK0awXAYkS1RsUccBzBzd+ZtLpd7X6tUTpmxpBzIGJtju+XlcNIy/"
        "A3tc0JAeGNl4YnuxP+EhONpN9Y8KliVogtipHdSjS3Nh3fEYhs3+fDs4b1GY3rChXjanuhOY+/sv"
        "6AcnKTRXf1E0zTkH99nxp2Jn13tQIe/WFTmJLs0P6fn5x5QIpPrzvH/BPgBSwHVyxsk72QAAAAASUVORK5CYII="
    )
)




class JoinWebAPI(eg.PluginBase):
    def __init__(self):
        self.AddAction(SendNotification)
        self.api_key=""
        self.devices={}

    def Configure(self, api_key="", devices=None):
        if devices is None:
            devices = getattr(self, 'devices', {})
        
        panel = eg.ConfigPanel()
        apiKeyCtrl = panel.TextCtrl(api_key or self.api_key)  # Use existing API key if available
        deviceListBox = wx.ListBox(panel, -1, style=wx.LB_SINGLE)

        for device_name in devices.keys():
            deviceListBox.Append(device_name)

        addButton = wx.Button(panel, -1, "Add Device")
        editButton = wx.Button(panel, -1, "Edit Device")
        removeButton = wx.Button(panel, -1, "Remove Device")

        addButton.Bind(wx.EVT_BUTTON, lambda evt: self.OnAdd(evt, deviceListBox, devices))
        editButton.Bind(wx.EVT_BUTTON, lambda evt: self.OnEdit(evt, deviceListBox, devices))
        removeButton.Bind(wx.EVT_BUTTON, lambda evt: self.OnRemove(evt, deviceListBox, devices))
        
        settingsBox = panel.BoxedGroup(
            "User Credentials",
            ("API Key:", apiKeyCtrl),
            ("Devices:", deviceListBox),
            (addButton, editButton, removeButton)
        )

        panel.sizer.Add(settingsBox, 0, wx.EXPAND)

        while panel.Affirmed():
            self.devices = devices  # Use existing device list
            self.api_key = api_key
            if not devices:
                # Handle empty devices (e.g., display a warning message)
                wx.MessageBox("Please add at least one device.", "Error", wx.ICON_ERROR)
                return
            
            api_key = apiKeyCtrl.GetValue()

            # Save configuration
            #eg.SetPluginSetting("api_key", api_key)
            #eg.SetPluginSetting("devices", devices)

            panel.SetResult(api_key, devices)

    def __start__(self, api_key, devices):
        self.api_key = api_key
        self.devices = devices

    def OnAdd(self, event, deviceListBox, devices):
        panel = event.GetEventObject().GetParent()
        dlg = wx.TextEntryDialog(panel, "Enter device name:")
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            dlg.Destroy()
            dlg = wx.TextEntryDialog(panel, "Enter device ID:")
            if dlg.ShowModal() == wx.ID_OK:
                device_id = dlg.GetValue()
                devices[name] = device_id.strip()
                deviceListBox.Append(name)
            dlg.Destroy()

    def OnEdit(self, event, deviceListBox, devices):
        sel = deviceListBox.GetSelection()
        if sel != wx.NOT_FOUND:
            old_name = deviceListBox.GetString(sel)
            dlg = wx.TextEntryDialog(event.GetEventObject().GetParent(), "Edit device name:")
            if dlg.ShowModal() == wx.ID_OK:
                new_name = dlg.GetValue()
                dlg.Destroy()
                dlg = wx.TextEntryDialog(event.GetEventObject().GetParent(), "Edit device ID:")
                if dlg.ShowModal() == wx.ID_OK:
                    new_id = dlg.GetValue()
                    del devices[old_name]
                    devices[new_name] = new_id.strip()
                    deviceListBox.SetString(sel, new_name)
                dlg.Destroy()

    def OnRemove(self, event, deviceListBox, devices):
        sel = deviceListBox.GetSelection()
        if sel != wx.NOT_FOUND:
            name = deviceListBox.GetString(sel)
            del devices[name]
            deviceListBox.Delete(sel)

    def validate_credentials(self, api_key, device_id):
        url = "https://joinjoaomgcd.appspot.com/_ah/api/registration/v1/listDevices"
        params = {"apikey": api_key}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            devices = response.json().get('records', [])
            return any(device['deviceId'] == device_id for device in devices)
        except requests.RequestException:
            return False


class SendNotification(eg.ActionBase):
    name = "Send Notification"
    description = "Sends a notification to selected Android devices."

    def __call__(self, title, text, selected_device_names):
        api_key = self.plugin.api_key
        url = "https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush"
        
        for device_name in selected_device_names:
            device_id = self.plugin.devices.get(device_name)
            if device_id:
                url = url+"?apikey="+api_key+"&text="+urllib.quote(text)+"&title="+urllib.quote(title)+"&deviceId="+device_id
                try:
                    response = requests.post(url)
                    response.raise_for_status()
                    print(url)
                    print "Notification sent successfully to device %s" % device_name
                except requests.RequestException as e:
                    print "Failed to send notification to device %s: %s" % (device_name, str(e))

    def Configure(self, title="", text="", selected_device_names=None):
        panel = eg.ConfigPanel()
        titleCtrl = panel.TextCtrl(title)
        textCtrl = panel.TextCtrl(text)
        
        deviceChoices = wx.CheckListBox(panel, -1, choices=list(self.plugin.devices.keys()))
        if selected_device_names:
            for i, device_name in enumerate(self.plugin.devices.keys()):
                if device_name in selected_device_names:
                    deviceChoices.Check(i, True)
        
        panel.AddLine("Title:", titleCtrl)
        panel.AddLine("Text:", textCtrl)
        panel.AddLine("Select devices:", deviceChoices)
        
        while panel.Affirmed():
            selected = [name for i, name in enumerate(self.plugin.devices.keys()) if deviceChoices.IsChecked(i)]
            panel.SetResult(titleCtrl.GetValue(), textCtrl.GetValue(), selected)
