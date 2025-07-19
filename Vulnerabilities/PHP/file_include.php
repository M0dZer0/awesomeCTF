<?php
highlight_file(__FILE__);
if (isset($_GET['file'])) {
    $file = $_GET['file'];
    include($file);
    if (file_exists($file)) {
        include($file);
    } else {
        echo "File does not exist.";
    }
} else {
    echo "No file specified.";
}
?>