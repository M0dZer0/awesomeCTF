<?php
if(isset($_GET["filename"])){
    $filename = "";
    if(is_array($_GET["filename"])){
        foreach($_GET["filename"] as $str){
            $filename .= str_replace("..", "", $str);
        }
    }
    else $filename = str_replace("..", "", $_GET["filename"]);
    $mime = mime_content_type("./images/".$filename);
    header("Content-Type: ".$mime);
    include("./images/".$filename);
}
else echo "<script>alert('filename is empty.')</script><meta http-equiv=\"refresh\" content=\"0;url=/list.php\" />";
?>