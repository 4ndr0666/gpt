> I cannot start my display server on an arch distro running wayland. out a readme.md with step by step instructions on how to resolve this.

> If you are having trouble starting your display server on an Arch Linux distribution running Wayland, here are some steps you can follow:

1. Confirm that your graphics card drivers are installed and up to date.
   - You can check this by running the following command in your terminal: `lspci -vnn | grep VGA`. This will show you which graphics card you have, and whether the drivers are installed and active.
2. Check that your display manager is configured to use Wayland.
   - If you are using GNOME, you can check this by going to Settings > About and scrolling down to the "Graphics" section. If it says "Wayland" next to "Windowing System", that means Wayland is enabled.
   - If you are using a different display manager, you may need to check its documentation to see how to enable Wayland.
3. Check that your system has the necessary packages for Wayland.
   - You can install the necessary packages by running the following command: `sudo pacman -S wayland`.
4. Check that your user has permission to access the Wayland socket.
   - Wayland uses a socket file to communicate with the display manager. You need to make sure your user has permission to access this socket file. Run the following command: `ls -la /run/user/*/wayland-0`. This will show you the permissions for the socket file. Make sure your user has read and write permissions.
   - If your user does not have permission, you can change the permissions by running the following command: `sudo chmod 660 /run/user/*/wayland-0`.
5. Make sure your user is a member of the "video" group.
   - In some cases, you may need to add your user to the "video" group in order to use Wayland. Run the following command: `sudo usermod -a -G video your_username`.
6. Reboot your system.
   - After making these changes, it's important to reboot your system to ensure the changes take effect.

If you still have trouble starting your display server after following these steps, it may be helpful to check your system logs for error messages. You can do this by running the following command: `journalctl -xe`. This will show you any error messages related to your display server.