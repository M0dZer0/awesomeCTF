<?php
highlight_file(__FILE__);
system("ls");
$mode = 0;
if (isset($_GET['file'])) {
    if(isset($_GET['mode'])) {
        echo '1';
        $mode = $_GET['mode'];
        $file = $_GET['file'];
        include($file.'.php');
    }else {
    echo '0';
    $file = $_GET['file'];
    include($file);
}
}
?>