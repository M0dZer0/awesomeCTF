<?php
highlight_file(__FILE__);
if (isset($_GET['a']) && isset($_GET['b'])) {
    $a = $_GET['a'];
    $b = $_GET['b'];
    if (md5($a) === md5($b) && $a !== $b) {
        echo '2';
        if (isset($_POST['passwd']) && isset($_POST['num'])) {
            $passwd = $_POST['passwd'];
            $num = $_POST['num'];
            echo '3';
            if (!is_numeric($passwd)) {
                echo '4';
                if ($passwd == "123456a") {
                    echo '5';
                    if ($num == 100000000) {
                        echo '6';
                        if (strlen($num) < 5) {
                            echo file_get_contents('./testflag');
                        } else {
                            die("num太长啦");
                        }
                    }
                }
            } else {
                die("passwd不能为纯数字");
            }
        }
    }
}
?>
