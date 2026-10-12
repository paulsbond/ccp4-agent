# Setting up CCP4

## When to use

Before the first CCP4 command in a session. CCP4 programs need the environment set by CCP4's setup file.

## Steps

1. Check whether CCP4 is already set up: in PowerShell run `$env:CCP4`, in bash run `echo $CCP4`. If it prints a folder, that is the CCP4 folder: run CCP4 commands as they are, and go to step 4. _Why:_ the user may have ordered their PATH on purpose, and loading the setup again would undo that.
2. Find the CCP4 installations, as in "Finding CCP4" below.
3. If there is one, use it. If there are several, list them with their versions and ask the user which to use.
4. Check the paths, as in "Paths" below.
5. Record the CCP4 folder in `journal.md`.

## Finding CCP4

### Windows

This command checks common locations, the user's home folder, for example `C:\Users\<name>\CCP4-9\CCP4`, and directly under `C:\`, and follows the CCP4 icons in the Start menu and on the desktop, including desktop folders such as `CCP4-9`. The CCP4 folder holds `ccp4.setup.bat`. In PowerShell:

```
$s = New-Object -ComObject WScript.Shell; $d = @(Get-ChildItem "$HOME\*\ccp4.setup.bat", "$HOME\*\*\ccp4.setup.bat", "C:\*\ccp4.setup.bat", "C:\*\*\ccp4.setup.bat" -ErrorAction SilentlyContinue | ForEach-Object DirectoryName); @(Get-ChildItem "$env:APPDATA\Microsoft\Windows\Start Menu", "$env:ProgramData\Microsoft\Windows\Start Menu" -Recurse -Filter *.lnk -ErrorAction SilentlyContinue) + @(Get-ChildItem "$([Environment]::GetFolderPath("Desktop"))\*.lnk", "$([Environment]::GetFolderPath("Desktop"))\*\*.lnk", "$env:PUBLIC\Desktop\*.lnk", "$env:PUBLIC\Desktop\*\*.lnk" -ErrorAction SilentlyContinue) | ForEach-Object { $t = $s.CreateShortcut($_.FullName).TargetPath; if ($t) { $d += Split-Path (Split-Path $t) } }; $d | Where-Object { Test-Path "$_\ccp4.setup.bat" } | Sort-Object -Unique | ForEach-Object { "$_\ccp4.setup.bat  $(Get-Content "$_\lib\ccp4\MAJOR_MINOR" -ErrorAction SilentlyContinue)" }
```

In bash, run the same command as `powershell -NoProfile -Command '<command>'`.

Each line is a setup file and its version, for example:

```
C:\Users\jo\CCP4-9\CCP4\ccp4.setup.bat  9.0.017
```

### Linux and macOS

Ask the user how they set up CCP4 in a terminal, and follow that.

## Running a command

If CCP4 was already set up in step 1, run commands as they are. Otherwise your shell keeps no environment between commands, so put the setup file in front of every CCP4 command. Replace `<setup>` with the full path of the setup file and `<command>` with the CCP4 command and its arguments, and keep the quotes exactly as shown:

- Windows, PowerShell: `cmd /c 'call "<setup>" >nul && <command>'`
- Windows, bash: `cmd //c call "<setup>" '>nul' '&&' <command>`

For example, in PowerShell:

```
cmd /c 'call "C:\Users\jo\CCP4-9\CCP4\ccp4.setup.bat" >nul && dials.version'
```

## Paths

Check the full path of the CCP4 folder and of your working directory. Each should contain only letters, digits, `-`, `_`, `.`, and the separators `\`, `/` and `:`. _Why:_ many CCP4 programs fail on paths with spaces or other characters, and Windows paths often contain them through the user name.

- If the working directory's path has other characters, tell the user and ask them for a working directory without them, for example `C:\xtal\<project>`. Copy or move the data there only if the user agrees.
- If the CCP4 folder's path has other characters, tell the user that CCP4 programs may fail and that reinstalling CCP4 in such a folder avoids it. Continue only if the user asks you to.

## If it fails

If no installation is found, ask the user which folder they installed CCP4 in. If CCP4 is not installed, tell the user to install it from https://www.ccp4.ac.uk and stop.
