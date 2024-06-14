<?php
session_start();
if(isset($_SESSION["username"])){
    session_destroy();
}
?>
<meta http-equiv="refresh" content="0;url=/" />