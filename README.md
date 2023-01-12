# Blender Rhubarb 2D Lipsync

[Get the Latest Release on Gumroad](https://tinynick.gumroad.com/l/uvsnj?layout=profile)

[Get the Latest Release Directly Here](https://github.com/NickTiny/blender-rhubarb-2d-lipsync/releases/tag/4.0.0)


[Rhubarb Lip Sync](https://github.com/DanielSWolf/rhubarb-lip-sync) is a command-line tool created by Daniel S. Wolf that automatically creates mouth animation from voice recordings. You can use it for characters in computer games, in animated cartoons, or in any other project that requires animating mouths based on existing recordings.

Blender Rhubarb Lipsync is an addon for Blender that integrates Rhubarb Lip Sync and uses it to generate mouth-shape keyframes from a pose library.

For support using this addon in Blender, please report an issue at 
https://github.com/NickTiny/blender-rhubarb-2d-lipsync/issues

# Video Tutorial

[![Rhubarb 2D Blender Tutorial by Tiny_Nick](https://i9.ytimg.com/vi_webp/Anltf1_ufLQ/mqdefault.webp?v=63bdfe31&sqp=CLipgJ4G&rs=AOn4CLDh1Amryu112tMECvsZnqFURhQqVQ)](https://www.youtube.com/watch?v=Anltf1_ufLQ)

# Installation
Download a release from https://github.com/NickTiny/blender-rhubarb-2d-lipsync/releases. If you download or clone the repository, the Rhubarb Lip Sync executable and data files will be missing - they can be downloaded separately from the Rhubarb Lip Sync repository, and set up as described below under Usage.



Use version `4.0.0` with `Blender 3.0+`.

Do not unzip the file.

In Blender, open Blender Preferences Edit -> Preferences select Add-ons and choose Install.... In the file dialog, select the .zip file. Once installed, enable the add-on with the checkbox.

# Usage: 

![time_offset_demo](https://user-images.githubusercontent.com/86638335/208316400-8b3fd323-1936-4a85-909d-82fdf4af38d3.gif)


**Set Up Object**

For Time Offset types. Create a grease pencil object with the mouth shapes described in the Rhubarb Lip Sync documentation. You can set your poses on whatever frame you like. Add a Time Offset Modifier in Fixed mode to your grease pencil object.


**Set Executable**

Blender Rhubarb Lipsync includes the Rhubarb Lip Sync executable, but if you want to use a different executable, you can choose it in user preferences.

You can also set the recognizer here. PocketSphinx is recommended for English language, phonetic may give better results for other languages.

![image](https://user-images.githubusercontent.com/86638335/208315480-a42398e9-e0e2-4417-b5b8-14f2eed6b149.png)

**Select a Target Type** 

 - Object will keyframe an integer/float property on the Object's Data. 
  - Time Offset will directly keyframe a Time Offset Modifier's Frame Offset. 
 - Bone will keyframe an interger or float property on the active Pose Bone.

![image](https://user-images.githubusercontent.com/86638335/208315884-ff24dcd6-a558-4084-a57f-ebb63755d2fe.png)


**Set Target's Property**

Select the name of your Grease Pencil's Time Offset Modifier under Properties. Or the name of an integer/float property on the object/bone.

![image](https://user-images.githubusercontent.com/86638335/208316229-bff658a7-fdec-40e6-b501-8572d6bf4a13.png)

**Assign Mouth Values**

 Set integers to match Rhubarb Lip Sync mouth shapes. Select your sound file, and dialog file (optional), and the start frame where your sound begins.

![image](https://user-images.githubusercontent.com/86638335/208316842-d28c383c-5115-4ede-9a79-682456620f4c.png)


**Run Rhubarb LipSync**

Click the Rhubarb LipSync button and wait for the process to complete. The mouse cursor will change to a progress indicator, and your keyframes will appear when the process is complete.


# Troubleshooting
This software is pre-release and provided without support. In the event of problems, you can use the system console (Window->Toggle System Console on Windows, or start Blender from a command line on Mac/Linux) to get more info on progress and error messages. When reporting an issue, please include any errors reported here.

[Test-Assets.zip](https://github.com/NickTiny/blender-rhubarb-2d-lipsync/files/10374071/Test-Assets.zip)


------------------
This is a fork of "Blender Rhubarb Lip Sync". Find [the original repo here](https://github.com/scaredyfish/blender-rhubarb-lipsync)
