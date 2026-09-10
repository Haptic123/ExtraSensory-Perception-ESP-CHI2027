# Initial Installation - Phone & Watch

> Follow these steps to create a user, install the watch app, install the phone app, connect the devices, and start monitoring.
Consider watching the  as a follow-up video guide.
> 

---

## 1. Create a New User

1. Open the **ResearcherSide** app on the server.
2. In the left tab, go to **Users** and click the **+** button.
3. Give the user a **unique ID**; naming is optional.

---

## 2. Reset the Watch

Make sure the watch is reset, has no prior connections to a phone, and has no app installed.

Go to:

```
General management > Reset
```

1. On your phone open the Wear App and follow the instructions on your phone and watch [Support] [LINK REMOVED FOR ANONYMITY].
2. Open the watch, start the **Wear** app on the phone. The app should recognize your watch.
3. Continue as instructed on the **Wear** app and watch.

---

## 3. Download the App to the Watch


❗ Make sure you have Android Studio installed on your computer



1. Download the `watch.apk` file to your computer. Link to download:

[LINK REMOVED FOR ANONYMITY]

1. On the watch, go to:

```
Settings > About watch > Software info
```

1. Repeatedly tap **Software version** 5 to 7 times.
2. Go back to:

```
Settings → Developer options
```

1. Enable **Wireless Debugging**.

> Make sure your watch and computer are connected to the same network.
> 
1. In CMD, navigate to the platform-tools folder by typing:

```bash
cd %LOCALAPPDATA%\Android\Sdk\platform-tools
```

---

## 4. Pair the Watch with ADB

On the watch, tap:

```
Wireless debugging → Pair new device with pairing code
```

You will see:

```
IP & Pairing Port
```

Example:

```
192.168.0.123:37015
```

You will also see a **6-digit Pairing Code**.

---

## 5. Pair from CMD

On CMD write:

```bash
adb pair 192.168.0.123:37015
```

Then enter the pairing code.

---

## 6. Find the ADB Connection Port

Still on the pairing screen, you’ll see the **ADB connection port**.

It usually looks something like:

```
192.168.0.123:5555
```

---

## 7. Connect to the Watch

On CMD write:

```bash
adb connect 192.168.0.123:5555
```

You should see:

```
connected to 192.168.0.123:5555
```

---

## 8. Install the Watch App

On CMD run:

```bash
adb -s WATCH_IP:ADB_PORT install -r path\to\watch-app.apk
```

Replace `WATCH_IP:ADB_PORT` with those you used in 3.8, and replace `path\to\watch-app.apk` with the path of the APK on your computer.

Example:

```bash
adb -s 192.168.0.123:5555 install -r C:\Users\YourName\Downloads\watch.apk
```

---

## 9. Download the Phone App

Download the `phone.apk` to your phone, open the file and download it.

> If asked, do not let the phone run a security check on the app.
> 

---

## 10. Connect the Watch to the Phone

1. In the Wear app, go to:

```
Watch settings > About watch > Change name
```

1. Change the name to:

```
UserID-xxx-SmartWatchID-xxx
```

Example:

```
UserID-333-SmartWatchID-334
```

For the user ID, use the same one you choose in **1.3**.

---

## 11. Start Monitoring

To start monitoring, make sure the phone is connected to the watch via Bluetooth.

Then open the apps on the watch and phone.