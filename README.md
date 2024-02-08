# Display <> Bluetooth Accessory Switcher

Ever felt like a DJ, juggling between multiple MacBooks, each with its own Magic Keyboard, Magic Trackpad, and Sonos speakers? Well, it's time to drop the beat and let the Accessory Switcher take over the stage!

This nifty tool is like a backstage manager for your Bluetooth devices. It ensures your Bluetooth keyboard and mouse are always connected to the right MacBook when you're plugging in or unplugging a display device via USB-C. No more awkward pauses during your productivity concert!

## Installation

The tool requires Python3 for executing, but the Python homebrew distribution is too bloated and I didn't want to include it in the package. Make sure to have a `python3` executable in your PATH (no additional libraries needed). If you haven't, you can install it via `brew install python3`. 

Installing the Display <> Bluetooth Accessory Switcher is as easy as 1-2-3:

1. Tap into the rhythm of our repository:
   ```
   brew tap tobias-gp/accessory-switcher
   ```
2. Install the star of the show:
   ```
   brew install accessory-switcher
   ```
3. Start the playlist:
   ```
   brew services start accessory-switcher
   ```

## Configuration

During its first performance, the Display <> Bluetooth Accessory Switcher will create a sample configuration file at `$HOME/.accessoryswitcher/config`, which you will have to change according to your setup: 

```
[DEFAULT]
devices=00-00-00-00-00-00,00-00-00-00-00-00
display_name=Display Name
sleep_time_in_s=5
```

To find out the MAC addresses of your devices (think of them as the VIP passes for your devices), run the following command:

```
blueutil --paired
```

This will give you a list of devices that looks something like this:

```
address: 00-00-00-00-00-00, connected (master, -46 dBm), not favourite, paired, name: "Magic Keyboard von Tobias", recent access date: 2024-02-07 02:46:57 +0000
address: 00-00-00-00-00-00, connected (master, -41 dBm), not favourite, paired, name: "Magic Trackpad von Tobias", recent access date: 2024-02-07 02:46:57 +0000
```

To get the name of your display (the main stage for your productivity concert), use the following command:

```
system_profiler SPDisplaysDataType
```

## Backstage

My journey to find the perfect Python Bluetooth libraries turned out to be more of a wild goose chase. So, I turned to blueutil as a trusty sidekick for this formula. It comes preinstalled as a dependency of the homebrew formula.

Beyond that, there's no entourage of additional Python libraries needed.

## Todos & Limitations

- Multiple environments are not yet supported (e.g. if you have mutliple workplaces).