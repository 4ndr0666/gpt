You:
### **Universal Debugging & Development Prompt for GPT**
#### *(For Structured, Iterative Debugging, Code Refinement, and Comprehensive Error Resolution)*

---
**ROLE & FUNCTIONALITY**  
You are an advanced **debugging and development assistant** designed to systematically analyze, debug, refine, merge and optimize scripts and codebases. Your responses must be concise, structured, and formatted for **maximum readability and direct implementation**. You will follow an **iterative debugging process**, ensuring **error-free, production-ready, and highly optimized outputs**.

---
## **1️⃣ SYSTEMATIC DEBUGGING & ERROR RESOLUTION**
When provided with a codebase, follow this structured debugging process:
1. **Analyze** the script, identify errors, and categorize them as **syntactical, logical, or dependency-based**.
2. **Reference terminal outputs**, error messages, and logs to pinpoint the root cause.
3. **Iteratively refine** the script, ensuring that each modification maintains logic consistency.
4. **Retain modular execution**, ensuring that functions work in isolation before integrating them dynamically.

---
## **2️⃣ RESPONSE FORMAT & OUTPUT FLOW**
Your responses must be structured in the following format:
1. **Summary of Issues**: Briefly describe detected issues.
2. **Error Analysis**: If logs or error messages are provided, dissect them and correlate with faulty logic.
3. **Solution Strategy**: Explain your plan for resolving errors before applying fixes.
4. **Refined Code**: Deliver a complete, structured, and error-free version in a single, formatted code block.
5. **Comparative Analysis** *(if applicable)*: Show a structured table comparing old vs. new functions.
6. **Follow-up Prompt** *(if applicable)*: Suggest test cases or validation steps.

---
## **3️⃣ MODULAR, IDEMPOTENT CODE REFINEMENT**
When refactoring code:
- **Ensure Idempotency**: Each function should execute consistently without side effects.
- **Preserve Functionality**: Do not introduce placeholders (`# TODO`)—only provide **complete** logic.
- **Handle Edge Cases**: Address empty inputs, permission errors, and dependency conflicts.
- **Use Structured Logging**: Implement `echo_status` for updates and `handle_error` for failures.

---
## **4️⃣ ITERATIVE TESTING & REAL-WORLD USABILITY**
After initial debugging:
- If the user provides new errors, **continue iterative refinement** until the script executes without issues.
- Implement **progressive enhancements** such as **improved logging, automatic conflict resolution, and dependency management**.
- Avoid **over-explaining**—focus on **directly implementing solutions** in each iteration.

---
## **5️⃣ RULES FOR OUTPUT DELIVERY**
- **NO EXCESSIVE EXPLANATION**: Prioritize **precise** solutions over unnecessary descriptions.
- **NO PARTIAL CODE**: Always provide the **entire script** when making changes.
- **NO PLACEHOLDERS OR INCOMPLETE LOGIC**: Every function must be complete.
- **PERSIST FORMATTING**: Responses must be structured with markdown (`bash`, `python`, etc.) and tables where applicable.
- **ENSURE COPY-PASTE RELIABILITY**: Scripts should be executable **as-is** without additional modifications.

---
## **6️⃣ ERROR HANDLING & SYSTEM SAFEGUARDS**
For any script execution:
1. **Verify Root Privileges** *(if required)* before executing privileged commands.
2. **Check Dependencies**: Detect and install missing packages automatically.
3. **Prevent Conflicts**: Handle package replacements cleanly before installing alternatives.
4. **Log Actions Clearly**: Ensure every operation logs output for traceability.

---
## **7️⃣ TECHNICAL IMPLEMENTATION BEST PRACTICES**
When modifying or optimizing code, **adhere to the following standards**:
- **For Shell Scripting**:
  - Use `set -eu -o pipefail` for safer execution.
  - Prefer `[[ ... ]]` over `[ ... ]` unless POSIX compliance is required.
  - Redirect errors to logs while preserving real-time console output.
- **For Python**:
  - Use structured logging instead of `print()` for error handling.
  - Ensure **strict exception handling** without suppressing meaningful errors.
  - **Optimize loops and conditionals** for efficiency.

---
## **8️⃣ FUNCTIONAL ENHANCEMENTS & CUSTOM REQUIREMENTS**
If the user requests **specific integrations** (e.g., MPV build flags, VapourSynth support), ensure:
- **Exact implementation** of provided configurations.
- **Verification that settings persist** across installations.
- **Avoid redundant installations** by checking if components exist before proceeding.

---
## **9️⃣ OUTPUT COMPRESSION & RESPONSE OPTIMIZATION**
Your responses must:
- **Never exceed 8,000 characters**.
- Prioritize **code over lengthy explanations**.
- Use **tables for structured comparisons** where applicable.
- Maintain a **logical flow** that aligns with real-world debugging.

---
### **SUMMARY**
By following this prompt, you will act as a **highly efficient, structured, and iterative debugging assistant**, ensuring **error-free, optimized, and production-ready solutions** with a **clear and logical flow**. Your **output must be directly executable**, formatted for readability, and **free of incomplete logic or placeholders**.

---

### **USAGE INSTRUCTIONS**
To use this prompt, **copy and paste it into any new GPT instance** before providing your code for any operation. 

---
*(End of Prompt)*

---

# Mode Of Operation

For this coding task, you will be operating in merge/refactor mode. Leverage a comparative analysis with the intent of producing a comprehensive and superior solution that encompasses the strengths from each codebase. Uphold revered coding philosophies and industry best practices. Specifically ensure uniform compliance with the Suckless philosophy and standards. Identify all similarities in order to see a high level overview of the initial structure for you revision. Gradually hone in on all ambiguity and resolve any overlap and unbound variables. Utilize detected gaps in order to borrow, migrate and merge the necessary logic to fully flesh out all functions for a complete, fully-functional, error-free and production ready codebase for testing. I will provide one script at a time. **Here is the first code base** for analysis:

```shell
#!/bin/bash
# LUSC - Linux UEFI STUB Creator
# 2024 by Lennart Martens - monkeynator78@gmail.com - https://github.com/lennart1978/LUSC -
# Automatically generate UEFI boot entries

# Color Codes
BLUE=$(tput setaf 4)
GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
RESET=$(tput sgr0)

# Display usage information
usage() {
    cat << EOF
Usage: $(basename "$0")
This is a simple interactive tool to automatically generate UEFI boot entries.
It generates efibootmgr commands and exports them to a small executable.
No changes will be written to disk before confirmation.
The EFI partition must be mountet to /boot and the kernel -and initramfs image must be located at the root of it !
Some UEFI systems don't allow to create more than one EFI STUB entry.
Unfortunately efibootmgr is not able to change EFI entries. You always have to delete/overwrite entries to make changes happen.
Please don't use this Bash script when you don't exactly know what you are doing here and what EFI STUB means.
You can get some great info at : https://wiki.archlinux.org/title/EFISTUB 

And now good luck with EFI STUB booting.
L.Martens

Options:
    -h, --help      Display this help message
EOF
}

# Check if the script is running with root privileges
if [ "$UID" -ne 0 ]; then
    echo "${RED}This script must be run with root privileges !${RESET}"
    echo "type: sudo lusc -h for usage and more info."
    exit 1
fi

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h | --help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
    shift
done

# Prompt user to continue
echo "${BLUE}Welcome to LUSC - A Linux UEFI STUB Creator"
echo "-----------------------------------------"
echo "-----------------------------------------${RESET}"
read -r -p "Start creating UEFI boot entries ? (y/N) " choice
choice=$(echo "$choice" | tr '[:upper:]' '[:lower:]')
if [[ "$choice" != "y" ]]; then
    echo "Goodbye.Exiting..."
    exit 0
fi

# Prompt user to specify EFI partition
read -r -p "Please specify EFI partition (e.g., /dev/nvme0n1p1): " efi_partition

# Check if the EFI partition exists
if ! blkid | grep -q "$efi_partition"; then
    echo "${RED}Error: EFI partition '$efi_partition' not found !${RESET}"
    exit 1
fi

# Extract disk and partition number
efi_disk=$(echo "$efi_partition" | sed -E 's/p?[0-9]+$//')
efi_part_num=$(echo "$efi_partition" | grep -o '[0-9]*$')

# Prompt user to specify the label for the boot entry
read -r -p "Please specify the label for the boot entry (e.g., Arch Linux): " boot_label

# Detect partitions
efi_uuid=$(blkid -o value -s UUID "$efi_partition")
root_uuid=$(blkid -o value -s UUID "$(findmnt -no SOURCE /)")

# Check if swap partition exists
swap_uuid=$(blkid -o value -s UUID "$(findmnt -no SOURCE /swap)")
if [[ -z "$swap_uuid" ]]; then
    echo "${GREEN}No swap partition detected. Assuming Zswap is used.${RESET}"
fi

# Default kernel parameters
default_params="root=UUID=$root_uuid rw"
if [[ -n "$swap_uuid" ]]; then
    default_params="$default_params resume=UUID=$swap_uuid"
fi

# Prompt user to specify additional kernel parameters
echo "Current kernel parameters: $default_params"
echo "${GREEN}initrd and initrd-fallback will be added automatically !${RESET}"
echo "For example additional kernel parameters could be: quiet splash rootfstype=ext4 hostname=my-computer nohibernate noresume vm_debug=- ..."
read -r -p "Add additional kernel parameters (or press Enter to keep current): " extra_params

# Combine default and additional parameters
if [[ -n "$extra_params" ]]; then
    kernel_params="$default_params $extra_params"
else
    kernel_params="$default_params"
fi

# initramdisks with "\" !
initramdisk="\initramfs-linux.img"
initfallback="\initramfs-linux-fallback.img"

# Compose the command strings
linux_cmd="efibootmgr --create --disk $efi_disk --part $efi_part_num --label \"$boot_label\" --loader /vmlinuz-linux --unicode \"$kernel_params initrd=$initramdisk\" --verbose"
fallback_cmd="efibootmgr --create --disk $efi_disk --part $efi_part_num --label \"$boot_label (Fallback)\" --loader /vmlinuz-linux --unicode \"$kernel_params initrd=$initfallback\" --verbose"

# Print the commands for user confirmation
echo "Detected partitions:"
echo "EFI: $efi_partition ($efi_uuid)"
echo "Root: $(findmnt -no SOURCE /) ($root_uuid)"
if [[ -n "$swap_uuid" ]]; then
    echo "Swap: $(findmnt -no SOURCE /swap) ($swap_uuid)"
    resume_option="resume=UUID=$swap_uuid"
else
    resume_option=""
fi

echo
echo "Composed commands:"
echo "$linux_cmd"
echo "$fallback_cmd"


# Prompt user to write or execute commands
read -r -p "Create executable only, create and execute (sets UEFI boot entries), or abort? (c/ce/a) " action
action=$(echo "$action" | tr '[:upper:]' '[:lower:]')
case "$action" in
    c)
        # Write commands to file
        script_file="uefi_stub_gen_$(date "+%d-%-m-%Y--%H:%M")"
        {
            echo "#!/bin/bash"
            echo "# Generated UEFI boot entries by LUSC"
            echo "$fallback_cmd"   
            echo "$linux_cmd"     
            echo "exit 0"
            echo "# See 'man efibootmgr' for more information"
        } > "$script_file"
        chmod +x "$script_file"
        echo "Commands written to file: $script_file"
        ;;
    ce)
        # Write commands to file and execute
        script_file="uefi_stub_gen_$(date "+%d-%-m-%Y--%H:%M")"
        {
            echo "#!/bin/bash"
            echo "# Generated UEFI boot entries by LUSC"
            echo "$fallback_cmd"
            echo "$linux_cmd"
            echo "exit 0"
            echo "# See 'man efibootmgr' for more information"
        } > "$script_file"
        chmod +x "$script_file"
        echo "Commands written to file: $script_file"
        echo "Executing commands..."
        "./$script_file"
        echo "Changes written. Power off and restart (${RED}don't reboot !${RESET})."
        ;;
    a)
        echo "Aborted. No changes made."
        ;;
    *)
        echo "${RED}Invalid choice ! Aborting.${RESET}"
        ;;
esac

exit 0
```

---

I am strategically parsing the code this way in order to avoid platform errors due to length constraints. Do not begin until you receive part 2 which I will send after this reponse.

ChatGPT:
### Revision Overview

- Original Codebase Line Count: 180 lines
- Working Revision Line Count: Pending (awaiting Part 2)

---

### Current Status

I have received Part 1 of your codebase. I will await Part 2 before beginning the full analysis, integration, and refinement process as per your structured debugging prompt.

---

### Next Steps

1. Awaiting Part 2: Please send the next portion of your codebase.
2. Full Analysis & Merging: Upon receipt, I will:
   - Compare and merge the code sections.
   - Perform a systematic error analysis.
   - Provide a complete, modular, and production-ready revision.
3. Iterative Feedback: I will then offer detailed testing suggestions and comparative analysis tables as needed.

---

Please provide Part 2 when ready.


You:
# Merge

# Comparative Analysis

During analysis automatically mitigate any identified syntactical errors as your proceed to present your findings.

# Required Format

Write the API list and task description for all functions in your last revision within a markdown table; then do the same for my script. Sum the total functions of both iterations and systematically present a side-by-side comparative analysis of both tables. Ensure each row(function) is numbered in alignment with the concise list of choices you will present at the end of your response. This process will clearly allow us to select the best implementation for use in a new revision.

# Confirmed Selections

Systematically cover each function asking for a choice between the two while presenting your decision and explain how you got to that decision. Concisely share potential improvements if applicable. At the end of your response, succinctly provide a numerical list that correlates to the comparative analysis table in which I can simply reply with a word or character to signify my choices. I will provide further details in my response to that.

# Codebase

Here is the final part of your instructions with which you can now begin the task:

```shell
#!/bin/bash
# File: liveiso_boot_entry.sh
# Author: 4ndr0666
# Date: 04-11-2024
#
# --- // LIVEISO_BOOT_ENTRY.SH // ========

# --- // COLORS:
CYAN='\033[0;36m'
GREEN='\033[0;32m'
NC='\033[0m'  # No Color

# --- // TRAP:
cleanup() {
    echo -e "${CYAN}Cleaning up... Please wait."
    # Add any cleanup commands here
    echo -e "Cleanup complete.${NC}"
    exit 1  # Ensure the script exits after cleanup
}
trap cleanup SIGINT SIGTERM EXIT

# --- // ROOT:
escalate() {
    if [ "$(id -u)" -ne 0 ]; then
        echo -e "${CYAN}CAUTION: You are now superuser...${NC}"
        exec sudo "$0" "$@"
    fi
}

# --- // DEPS:
dependencies() {
    local required_cmds="curl grep sed sha256sum tee cat find jq btrfs blkid findmnt grub-mkconfig wget"
    for cmd in $required_cmds; do
        if ! command -v $cmd &> /dev/null; then
            echo -e "${CYAN}Error: Required command '$cmd' not found.${NC}"
            exit 1
        fi
    done
}

# --- // FS:
filesystem_type() {
    read -r -p "Select your filesystem type for operations (ext4 or btrfs): " filesystem_type
    if [[ $filesystem_type != "ext4" && $filesystem_type != "btrfs" ]]; then
        echo -e "${CYAN}Unsupported filesystem type. Exiting.${NC}"
        exit 1
    fi
}

# --- // VARIABLES:
setup_variables() {
    subvol="@iso_subvol"
    folder="/mnt/iso_subvol"
    rootdrive=$(findmnt -n -o SOURCE /)
    rootuuid=$(blkid -s UUID -o value "$rootdrive")
}

# --- // BOOTLOADER:
check_bootloader() {
    if [ -d /boot/efi/loader/entries ]; then
        echo -e "${CYAN}System is managed by systemd-boot.${NC}"
        bootloader="systemd"
    elif [ -d /boot/grub ]; then
        echo -e "${CYAN}System uses GRUB.${NC}"
        bootloader="grub"
    else
        echo -e "${CYAN}No supported bootloader found. Manual configuration required.${NC}"
        exit 1
    fi
}

# --- // DISTROLIST:
distrolist() {
    echo -e "${CYAN}Fetching available distributions...${NC}"
    declare -A distros=(
            ["Ubuntu"]="https://www.ubuntu.com/download/desktop"
            ["Fedora"]="https://getfedora.org/en/workstation/download/"
            ["Ubuntu"]="https://www.ubuntu.com/download/desktop"
            ["Edubuntu"]="https://edubuntu.org/download"
            ["Kubuntu"]="https://kubuntu.org/getkubuntu/"
            ["Lubuntu"]="https://lubuntu.net/downloads/"
            ["Xubuntu"]="https://xubuntu.org/download"
            ["Ubuntu Budgie"]="https://ubuntubudgie.org/downloads"
            ["Ubuntu Gnome"]="https://cdimage.ubuntu.com/ubuntu-gnome/releases/"
            ["Ubuntu Server"]="https://www.ubuntu.com/download/server"
            ["Ubuntu Studio"]="https://ubuntustudio.org/download/"
            ["Emmabuntus"]="https://sourceforge.net/projects/emmabuntus/files/latest/download"
            ["Linux Mint"]="https://www.linuxmint.com/download.php"
            ["Linux Mint Debian"]="https://www.linuxmint.com/download_lmde.php"
            ["CentOS Live"]="https://www.centos.org/download/"
            ["CentOS Minimal"]="https://www.centos.org/download/"
            ["Debian Live"]="https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/"
            ["Fedora"]="https://getfedora.org/en/workstation/download/"
            ["OpenSUSE"]="https://get.opensuse.org/desktop/"
            ["Puppy Linux"]="http://distro.ibiblio.org/puppylinux/puppy-fossa/fossapup64-9.5.iso"
            ["BionicPup"]="https://distro.ibiblio.org/puppylinux/puppy-bionic/"
            ["Tahrpup"]="https://distro.ibiblio.org/puppylinux/puppy-tahr/iso/tahrpup64-6.0.5/tahr64-6.0.5.iso"
            ["Fatdog64"]="https://distro.ibiblio.org/fatdog/iso/"
            ["Lucid Puppy Linux"]="https://distro.ibiblio.org/pub/linux/distributions/puppylinux/puppy-5.2.8/lupu-528.005.iso"
            ["Precise Puppy Linux"]="https://distro.ibiblio.org/quirky/precise-5.7.1/precise-5.7.1.iso"
            ["Slacko Puppy"]="https://distro.ibiblio.org/puppylinux/puppy-slacko-6.3.2/64/slacko64-6.3.2-uefi.iso"
            ["Academix"]="https://sourceforge.net/projects/academix/files/latest/download"
            ["AntiX"]="https://sourceforge.net/projects/antix-linux/files/latest/download"
            ["Archbang"]="https://sourceforge.net/projects/archbang/files/latest/download"
            ["Archlinux"]="http://mirrors.us.kernel.org/archlinux/iso/latest/"
            ["EndeavourOS"]="https://mirrors.gigenet.com/endeavouros/iso/EndeavourOS_Galileo-Neo-2024.01.25.iso"
            ["Garuda Hyprland"]="https://iso.builds.garudalinux.org/iso/latest/community/hyprland/latest.iso?r2=1"
            ["Garuda dr460nized"]="https://iso.builds.garudalinux.org/iso/latest/garuda/dr460nized/latest.iso?r2=1"
            ["Garuda Gnome"]="https://iso.builds.garudalinux.org/iso/latest/garuda/gnome/latest.iso?r2=1"
            ["Garuda Xfce"]="https://iso.builds.garudalinux.org/iso/latest/garuda/xfce/latest.iso?r2=1"
            ["Manjaro"]="https://download.manjaro.org/kde/23.1.4/manjaro-kde-23.1.4-240406-linux66.iso"
            ["Axyl"]="https://github.com/axyl-os/axylos-2-iso/releases/download/v2-beta-2024.04.11/axyl-v2-beta-2024.04.11-x86_64.iso"
            ["Archcraft"]="https://sourceforge.net/projects/archcraft/files/latest/download"
            ["CachyOS"]="https://iso.cachyos.org/240401/cachyos-kde-linux-240401.iso"
            ["BigLinux"]="https://iso.biglinux.com.br/biglinux_2024-04-05_k68.iso"
            ["Artix"]="https://artixlinux.org/download.php"
            ["Stormos"]="https://sourceforge.net/projects/hackman-linux/"
            ["Mabox"]="https://sourceforge.net/projects/mabox-linux/files/latest/download"
            ["Bluestar Linux"]="https://sourceforge.net/projects/bluestarlinux/files/latest/download"
            ["Bodhi"]="https://sourceforge.net/projects/bodhilinux/files/latest/download"
            ["CAELinux"]="https://sourceforge.net/projects/caelinux/files/latest/download"
            ["Calculate Linux Desktop"]="http://www.gtlib.gatech.edu/pub/calculate/release/20.6/"
            ["Cub Linux"]="https://sourceforge.net/projects/cublinux/files/latest/download"
            ["Deepin"]="https://sourceforge.net/projects/deepin/files/latest/download"
            ["Endeavour OS"]="https://endeavouros.com/latest-release/"
            ["Feren OS"]="https://sourceforge.net/projects/ferenoslinux/files/latest/download"
            ["JustBrowsing"]="https://sourceforge.net/projects/justbrowsing/files/latest/download"
            ["KDE Neon"]="https://neon.kde.org/download"
            ["KNOPPIX"]="http://ftp.knoppix.nl/os/Linux/distr/knoppix/KNOPPIX_V9.1CD-2021-01-25-EN.iso"
            ["KXStudio"]="https://sourceforge.net/projects/kxstudio/files/latest/download"
            ["LinuxFX"]="https://sourceforge.net/projects/linuxfxdevil/files/latest/download"
            ["Linux Kid X"]="https://sourceforge.net/projects/linuxkidx/files/latest/download"
            ["LXLE Desktop"]="https://sourceforge.net/projects/lxle/files/latest/download"
            ["OpenMandriva"]="https://sourceforge.net/projects/openmandriva/files/latest/download"
            ["mintyMac"]="http://sourceforge.net/projects/mintymacpremium/files/latest/download"
            ["MX Linux"]="https://sourceforge.net/projects/mx-linux/files/latest/download"
            ["Netrunner"]="https://www.netrunner.com/download/"
            ["OSGeo Live"]="https://sourceforge.net/projects/osgeo-live/files/latest/download"
            ["PCLinuxOS"]="https://www.pclinuxos.com/?page_id=10"
            ["Peach OSI"]="https://www.peachosi.com/content/download-patriot"
            ["Pear Linux"]="https://sourceforge.net/projects/pearoslinux/files/latest/download"
            ["Peppermint"]="https://peppermintos.com/guide/downloading/"
            ["Pinguy OS"]="https://sourceforge.net/projects/pinguy-os/files/latest/download"
            ["Porteus"]="http://porteus.org/porteus-mirrors.html"
            ["POP!_OS"]="https://pop.system76.com/"
            ["Q4OS"]="https://sourceforge.net/projects/q4os/files/latest/download"
            ["Raspberry Pi Desktop"]="https://www.raspberrypi.org/software/raspberry-pi-desktop/"
            ["Skywave Linux"]="https://sourceforge.net/projects/skywavelinux/files/latest/download"
            ["SLAX"]="https://www.slax.org/#purchase"
            ["SliTaZ"]="https://www.slitaz.org/en/get/"
            ["LuninuX OS"]="https://sourceforge.net/projects/luninuxos/files/latest/download"
            ["Solus"]="https://getsol.us/download/"
            ["SolydX"]="https://solydxk.com/downloads.php"
            ["Sparky Linux"]="https://sourceforge.net/projects/sparkylinux/files/latest/download"
            ["Sugar on a Stick"]="https://wiki.sugarlabs.org/go/Sugar_on_a_Stick"
            ["Terralinux"]="https://sourceforge.net/projects/terralinuxos/files/latest/download"
            ["Uberstudent"]="https://sourceforge.net/projects/uberstudent/files/latest/download"
            ["Ultimate Edition"]="https://sourceforge.net/projects/ultimateedition/files/latest/download"
            ["Xiaopan"]="https://sourceforge.net/projects/xiaopanos/files/latest/download"
            ["Zorin OS Core"]="https://zorinos.com/download/"
            ["Kodachi"]="https://sourceforge.net/projects/linuxkodachi/files/latest/download"
            ["Liberte"]="https://sourceforge.net/projects/liberte/files/latest/download"
            ["4M Linux"]="https://sourceforge.net/projects/linux4m/files/latest/download"
            ["Antivirus Live CD"]="https://sourceforge.net/projects/antiviruslivecd/files/latest/download"
            ["AVIRA AntiVir Rescue CD"]="https://download.avira.com/download/rescue-system/avira-rescue-system.iso"
            ["Dr.Web LiveDisk"]="https://download.geo.drweb.com/pub/drweb/livedisk/drweb-livedisk-900-cd.iso"
            ["ESET SysRescue Live"]="https://www.eset.com/int/support/sysrescue/#download"
            ["GDATA Rescue CD"]="https://secure.gd/dl-int-bootcd"
            ["Kaspersky Rescue Disk"]="https://rescuedisk.s.kaspersky-labs.com/updatable/2018/krd.iso"
            ["Acronis True Image"]="NONE"
            ["BackBox"]="https://www.backbox.org/download/"
            ["Boot Repair Disk"]="https://sourceforge.net/projects/boot-repair-cd/files/latest/download"
            ["Caine"]="https://www.caine-live.net/page5/page5.html"
            ["Clonezilla"]="https://clonezilla.org/downloads.php"
            ["DBAN"]="https://sourceforge.net/projects/dban/files/latest/download"
            ["Demon Linux"]="https://demonlinux.com/"
            ["DRBL"]="https://sourceforge.net/projects/drbl/files/latest/download"
            ["EASEUS Disk Copy"]="https://download.easeus.com/free/EaseUS_DiskCopy_Home.exe"
            ["Finnix"]="https://www.finnix.org/Download"
            ["G4L"]="https://sourceforge.net/projects/g4l/files/latest/download"
            ["GParted"]="https://sourceforge.net/projects/gparted/files/latest"
            ["GRML"]="https://grml.org/download/"
            ["Kali"]="https://www.kali.org/downloads/"
            ["Memtest86"]="https://www.memtest86.com/download.htm"
            ["Memtest86+"]="https://www.memtest.org/download/5.31b/memtest86+-5.31b.bin.zip"
            ["Matriux"]="https://sourceforge.net/projects/matriux/files/latest/download"
            ["Ophcrack"]="https://sourceforge.net/projects/ophcrack/files/ophcrack-livecd/3.6.0/"
            ["Rescatux"]="https://sourceforge.net/projects/rescatux/files/latest/download"
            ["Rescuezilla"]="https://rescuezilla.com/download.html"
            ["Redo Backup And Recovery"]="https://sourceforge.net/projects/redobackup/files/latest/download"
            ["Rip Linux"]="https://sourceforge.net/projects/riplinuxmeta4s/files/latest/download"
            ["System Rescue"]="https://sourceforge.net/projects/systemrescuecd/files/latest/download"
            ["Trinity Rescue Kit"]="https://trinityhome.org/trinity_rescue_kit_download/"
            ["Ultimate Boot CD"]="http://www.ultimatebootcd.com/download/redirect.php"
            ["Wifislax"]="https://www.wifislax.com/category/download/"
            ["Falcon 4 Boot CD"]="NONE"
            ["Hiren's Boot CD"]="NONE"
            ["Hiren's BootCD PE"]="https://www.hirensbootcd.org/download/"
            ["LinuxCNC"]="https://linuxcnc.org/downloads/"
    )
    PS3="Please select a distribution: "
    select distro in "${!distros[@]}"; do
        if [ -n "$distro" ]; then
            echo -e "${CYAN}You have selected: $distro${NC}"
            break
        else
            echo -e "${CYAN}Invalid selection. Please select a valid option.${NC}"
        fi
    done
    iso_url="${distros[$distro]}"
    iso_path="/iso_storage/$distro.iso"
    echo -e "${CYAN}Preparing to download $distro:${NC}"
    echo -e "${CYAN}Download URL: $iso_url${NC}"
    echo -e "${CYAN}Storing at: $iso_path${NC}"
}

# --- // DIR_CHECK:
ensure_directory_exists() {
    local storage_dir=$(dirname "$iso_path")
    if [ ! -d "$storage_dir" ]; then
        echo -e "${CYAN}Storage directory $storage_dir does not exist. Creating...${NC}"
        mkdir -p "$storage_dir"
        if [ $? -ne 0 ]; then
            echo -e "${CYAN}Failed to create storage directory. Exiting.${NC}"
            exit 1
        fi
        echo -e "${CYAN}Directory created successfully.${NC}"
    fi
}

# --- // DL_ISO:
download_iso() {
    if ! wget -O "$iso_path" "$iso_url"; then
        echo -e "${CYAN}Download failed. Exiting.${NC}"
        rm -f "$iso_path"
        exit 2
    fi
    echo -e "${CYAN}Download complete.${NC}"
}

# --- // IDEMPOTENCY:
check_iso_existence() {
    if [ -f "$iso_path" ]; then
        echo -e "${CYAN}ISO for $distro already exists. Skipping download.${NC}"
    else
        ensure_directory_exists
        download_iso
    fi
}

# --- // CONFIG:
configure_bootloader() {
    case $bootloader in
        "grub")
            echo -e "${CYAN}Adding GRUB entry for $distro...${NC}"
            configure_grub
            ;;
        "systemd")
            echo -e "${CYAN}Adding systemd-boot entry for $distro...${NC}"
            configure_systemd_boot
            ;;
    esac
}

# --- // MAIN_LOGIC_LOOP:
escalate
dependencies
filesystem_type
setup_variables
check_bootloader
distrolist
check_iso_existence
configure_bootloader

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Operation completed successfully. Please reboot to use the new ISO boot option.${NC}"
fi
```

ChatGPT:
Below is the detailed comparative analysis of the two codebases. In the header, you’ll find the total line counts and function inventories. Each table lists the API (i.e. function name, description, parameters, and outcome) for its respective codebase. Finally, a side-by-side comparative table (with numbered rows) shows our analysis and the recommended selections. You can then simply reply with the number(s) corresponding to your choices.

---

## Revision Overview

- LUSC – Linux UEFI STUB Creator (Codebase 1)
  - Line Count: \~180 lines
  - Total Functions: 1

- liveiso\_boot\_entry.sh (Codebase 2)
  - Line Count: \~150 lines (estimated)
  - Total Functions: 11

- Combined Total Functions: 12

---

## Table 1: API List for LUSC – Linux UEFI STUB Creator (Codebase 1)

| # | Function Name | Task Description                                                       | Parameters | Return / Outcome                                          |
| - | ------------- | ---------------------------------------------------------------------- | ---------- | --------------------------------------------------------- |
| 1 | `usage`       | Displays help and usage instructions for generating UEFI boot entries. | None       | Outputs usage message via a heredoc and exits if invoked. |

---

## Table 2: API List for liveiso\_boot\_entry.sh (Codebase 2)

| #  | Function Name             | Task Description                                                                                                                                    | Parameters                             | Return / Outcome                                                                            |
| -- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------- |
| 1  | `cleanup`                 | Handles script termination and cleanup upon receiving SIGINT, SIGTERM, or EXIT signals.                                                             | None                                   | Prints cleanup messages and exits with status 1.                                            |
| 2  | `escalate`                | Ensures the script is running with root privileges; re-invokes the script with sudo if not.                                                         | `"$@"` (all arguments)                 | Re-executes script as superuser, preserving arguments.                                      |
| 3  | `dependencies`            | Verifies that all required commands (e.g., curl, grep, sed, etc.) are available; exits if any command is missing.                                   | None                                   | Checks for each dependency and exits with an error if any are not found.                    |
| 4  | `filesystem_type`         | Prompts the user to select the filesystem type (ext4 or btrfs) for operations and validates the input.                                              | None                                   | Returns the selected filesystem type or exits if an unsupported type is entered.            |
| 5  | `setup_variables`         | Initializes key variables such as subvolume name, folder path, root drive, and root UUID.                                                           | None                                   | Sets environment variables used later in the boot entry configuration process.              |
| 6  | `check_bootloader`        | Determines which bootloader is in use (systemd-boot or GRUB) by checking specific directory existence.                                              | None                                   | Sets a bootloader variable; prints bootloader type or exits if none is supported.           |
| 7  | `distrolist`              | Presents an associative array of distributions with download URLs; prompts the user to select one and sets ISO download variables accordingly.      | None                                   | Sets `iso_url` and `iso_path` based on user selection and informs the user of their choice. |
| 8  | `ensure_directory_exists` | Verifies that the directory for storing the ISO exists; creates it if it does not exist.                                                            | None (uses `iso_path`)                 | Creates the required storage directory (or exits on failure) and prints a status message.   |
| 9  | `download_iso`            | Downloads the selected ISO using wget; cleans up (removes partial file) if the download fails.                                                      | None (uses `iso_url`, `iso_path`)      | Attempts ISO download; prints completion message or error and removes the file on failure.  |
| 10 | `check_iso_existence`     | Checks if the ISO file already exists; if not, it calls the directory check and download functions to ensure idempotency in the download process.   | None                                   | Either confirms the ISO’s existence or triggers its download process.                       |
| 11 | `configure_bootloader`    | Configures the bootloader (GRUB or systemd-boot) for the new ISO boot entry by calling the appropriate bootloader-specific configuration functions. | None (relies on `bootloader` variable) | Calls either `configure_grub` or `configure_systemd_boot` and prints status messages.       |

---

## Comparative Analysis Table (Side-by-Side)

Each row below corresponds to one function (or a functionality block) from the combined total of 12 functions. For functions that exist only in one codebase, we note that the implementation is unique to that codebase. Your choices below will confirm which implementation to include in the final merged revision.

| Row | LUSC – Linux UEFI STUB Creator (Codebase 1) | liveiso\_boot\_entry.sh (Codebase 2) | Comparison & Decision                                                                                                         |
| --- | ------------------------------------------- | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| 1   | `usage`                                     | No equivalent                        | Decision: Use Codebase 1’s `usage` for help/usage info. It is the sole implementation for usage messaging.                    |
| 2   | Not Applicable                              | `cleanup`                            | Decision: Use Codebase 2’s `cleanup` for handling termination and cleanup (critical for robust script operation).             |
| 3   | Not Applicable                              | `escalate`                           | Decision: Use Codebase 2’s `escalate` to ensure proper root privileges are enforced.                                          |
| 4   | Not Applicable                              | `dependencies`                       | Decision: Adopt Codebase 2’s `dependencies` to verify required commands before proceeding.                                    |
| 5   | Not Applicable                              | `filesystem_type`                    | Decision: Adopt Codebase 2’s `filesystem_type` to prompt and validate filesystem type, ensuring correct user input.           |
| 6   | Not Applicable                              | `setup_variables`                    | Decision: Use Codebase 2’s `setup_variables` to initialize key variables (e.g., root UUID) for further operations.            |
| 7   | Not Applicable                              | `check_bootloader`                   | Decision: Adopt Codebase 2’s `check_bootloader` for bootloader detection; essential for boot entry configuration.             |
| 8   | Not Applicable                              | `distrolist`                         | Decision: Use Codebase 2’s `distrolist` to provide a user-friendly selection of distributions and set ISO download variables. |
| 9   | Not Applicable                              | `ensure_directory_exists`            | Decision: Adopt Codebase 2’s `ensure_directory_exists` to guarantee the ISO storage directory exists.                         |
| 10  | Not Applicable                              | `download_iso`                       | Decision: Use Codebase 2’s `download_iso` for the robust handling of ISO downloads, including failure cleanup.                |
| 11  | Not Applicable                              | `check_iso_existence`                | Decision: Adopt Codebase 2’s `check_iso_existence` for idempotency in ISO downloads, avoiding redundant operations.           |
| 12  | Not Applicable                              | `configure_bootloader`               | Decision: Use Codebase 2’s `configure_bootloader` to automatically integrate the ISO boot entry with the active bootloader.   |

---

## Final Selections & Next Steps

Below is the numerical list correlating to each row of the comparative analysis. Simply reply with the row numbers (or a shorthand response) to signify your choices or request further discussion on specific rows.

1. Row 1: Use `usage` (Codebase 1) for help/usage messaging.
2. Row 2: Use `cleanup` (Codebase 2).
3. Row 3: Use `escalate` (Codebase 2).
4. Row 4: Use `dependencies` (Codebase 2).
5. Row 5: Use `filesystem_type` (Codebase 2).
6. Row 6: Use `setup_variables` (Codebase 2).
7. Row 7: Use `check_bootloader` (Codebase 2).
8. Row 8: Use `distrolist` (Codebase 2).
9. Row 9: Use `ensure_directory_exists` (Codebase 2).
10. Row 10: Use `download_iso` (Codebase 2).
11. Row 11: Use `check_iso_existence` (Codebase 2).
12. Row 12: Use `configure_bootloader` (Codebase 2).

---

Please review the above analysis and reply with your selections (e.g., “1, 2, 3, …” or any comments regarding specific rows) so that we can proceed to produce the final merged and production-ready revision.
