### Forensics

##### information

We can use command `strings` or exiftool to get detailed information about the image.In this problem,we can use exiftool on your Operation System(on my Mac, it can be installed by `brew install exiftool`) to analyse this image.



<img src="./assets/information.png" alt="information" style="zoom:50%;" />

We can find the license field is suspicious. It turned out to be our flag after base64 encoding, so we can decode this string and get flag.

##### Matryoshka doll

To figure out whether this image contains other file, we can use 010editor or Winhex to review its string information.We can use `binwalk dolls.jpg -e` to extract the other files.After 4 executions, we can get the `flag.txt` after extracting `4_c.jpg`.

